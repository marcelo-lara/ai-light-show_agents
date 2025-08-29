import re
from typing import Optional
from ...models.app_data import AppData
from ..agent import Agent
from ...models.lighting.plan import PlanEntry
from ...utils import write_file

class LightingPlanner(Agent):
    def __init__(self, model: str = "cogito:8b"):
        self._model = model
        super().__init__(model=self._model)

    def _extract_analysis_summary(self, start_time: float = 0, end_time: Optional[float] = None) -> dict:
        """Extract relevant analysis data for a specific time segment."""
        analysis = self.app_data.song_analysis
        
        if not analysis:
            return {}
        
        # Get segment boundaries
        if end_time is None:
            end_time = self.app_data.song.duration
        
        # Extract key musical elements
        summary = {
            "tempo": analysis.get("tempo", "Unknown"),
            "key": analysis.get("key", "Unknown"),
            "duration": self.app_data.song.duration,
            "target_segment": f"{start_time}s - {end_time}s"
        }
        
        # Get relevant structure sections
        structure = analysis.get("structure", [])
        relevant_sections = [
            section for section in structure 
            if section["end"] > start_time and section["start"] < end_time
        ]
        summary["structure"] = relevant_sections
        
        # Get beat times for the segment
        beats = analysis.get("beats", [])
        segment_beats = [beat for beat in beats if start_time <= beat <= end_time]
        summary["beat_count"] = len(segment_beats)
        summary["first_beat"] = segment_beats[0] if segment_beats else start_time
        summary["last_beat"] = segment_beats[-1] if segment_beats else end_time
        
        # Sample beats (first 10, last 10, and every 10th in between)
        if len(segment_beats) > 20:
            sampled_beats = (
                segment_beats[:10] + 
                segment_beats[10:-10:10] + 
                segment_beats[-10:]
            )
            summary["sampled_beats"] = sampled_beats
        else:
            summary["sampled_beats"] = segment_beats
        
        return summary

    def parse_song_context(self, song_name: str, start_time: float = 0, end_time: Optional[float] = None):
        """Parse song context for lighting planning with smart analysis extraction."""
        analysis_summary = self._extract_analysis_summary(start_time, end_time)
        
        user_prompt = f"Create a lighting plan for the song: {song_name}"
        if start_time > 0 or end_time:
            user_prompt += f" (focus on {start_time}s - {end_time or self.app_data.song.duration}s)"
        
        self.parse_context(
            song=self.app_data.song,
            fixtures=self.app_data.fixtures,
            analysis_summary=analysis_summary,
            user_prompt=user_prompt,
            start_time=start_time,
            end_time=end_time or self.app_data.song.duration
        )
        
        write_file(str(self.app_data.logs_folder / "lighting_planner.context.txt"), self._context)
        
    def parse_response(self):
        """Parse the last response and extract plan entries."""
        if not self._last_response:
            print("⚠️ No response to parse")
            return
            
        write_file(str(self.app_data.logs_folder / "lighting_planner.response.txt"), self._last_response)
        
        # Extract plan entries from the response
        plan_lines = [line.strip() for line in self._last_response.split('\n') if line.strip() and line.startswith('#plan add at')]
        
        if not plan_lines:
            print("⚠️ No plan entries found in response")
            return
            
        # Clear existing plan entries
        self.app_data.plan.clear_plan()
        
        # Parse each plan line and collect entries
        parsed_entries = []
        for line in plan_lines:
            try:
                plan_entry = self._parse_plan_line(line)
                if plan_entry:
                    parsed_entries.append(plan_entry)
            except Exception as e:
                print(f"⚠️ LightingPlanner.parse_response -> Error parsing plan line '{line}': {e}")
        
        # Sort entries by start time and assign IDs
        parsed_entries.sort(key=lambda x: x.start)
        
        # Calculate end times based on next entry or default duration
        for i, entry in enumerate(parsed_entries):
            if i < len(parsed_entries) - 1:
                # Set end time to next entry's start time
                entry.end = parsed_entries[i + 1].start
            else:
                # Last entry: use a default duration of 10 seconds or song end
                entry.end = min(entry.start + 10.0, self.app_data.song.duration)
            
            # Assign ID
            entry.id = i + 1
            
            # Add to plan
            self.app_data.plan.add_plan(entry)
                    
        # Save the updated plan
        self.app_data.plan.save_plan()

    def _parse_plan_line(self, line: str) -> PlanEntry:
        """Parse a single plan entry line into a PlanEntry."""
        # Pattern to match: #plan add at [time] "[label]" "[description]"
        # Example: #plan add at 0.487 "Intro start" "half intensity blue chaser from left to right at 1b intervals"
        
        pattern = r'#plan add at ([\d.]+) "([^"]+)" "([^"]+)"'
        match = re.match(pattern, line)
        
        if not match:
            raise ValueError(f"Invalid plan format: {line}")
            
        start_time = float(match.group(1))
        name = match.group(2)
        description = match.group(3)
        
        # Create PlanEntry with temporary values (id and end will be set later)
        return PlanEntry(
            id=0,  # Will be set later
            start=start_time,
            end=start_time + 1.0,  # Temporary, will be calculated later
            name=name,
            description=description
        )
