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
        # Placeholder implementation
        if not self._last_response:
            print("⚠️ No response to parse")
            return
        write_file(str(self.app_data.logs_folder / "lighting_planner.response.txt"), self._last_response)

        # TODO: Implement response parsing for plan entries
        # This would extract plan entries from the LLM response
        # and add them to the plan

        print("⚠️ LightingPlanner.parse_response -> Placeholder implementation")

    def _parse_plan_line(self, line: str) -> PlanEntry:
        """Parse a single plan entry line into a PlanEntry."""
        # Placeholder implementation
        # TODO: Implement parsing logic for plan entries
        raise NotImplementedError("Plan line parsing not yet implemented")
