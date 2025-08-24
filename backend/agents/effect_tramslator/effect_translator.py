import re
from ...models.app_data import AppData
from ..agent import Agent
from ...models.lighting.plan import PlanEntry
from ...models.lighting.action_list import ActionEntry
from ...utils import write_file

class EffectTranslator(Agent):
    def __init__(self, model:str = "cogito:8b"):
        self._model = model
        super().__init__(model=self._model)

    def parse_plan_entry(self, plan_entry:PlanEntry):
        user_prompt = plan_entry.description
        beats_array = self.app_data.song.get_beats_array(plan_entry.start, plan_entry.end)
        actions_reference = {action.name: action for fixture in self.app_data.fixtures for action in fixture.actions}
        self.parse_context(
            beats=beats_array,
            actions_reference=actions_reference,
            user_prompt=user_prompt
        )

        write_file(str(self.app_data.logs_folder / "effect_translator.context.txt"), self._context)
        
    def parse_response(self):
        """Parse the last response and extract action commands."""
        
        if not self._last_response:
            print("⚠️ No response to parse")
            return
            
        # Extract actions block from the response
        actions_match = re.search(r'```actions\s*\n(.*?)\n```', self._last_response, re.DOTALL)
        if not actions_match:
            print("⚠️ No actions block found in response")
            return
            
        actions_text = actions_match.group(1).strip()
        if not actions_text:
            print("⚠️ Empty actions block")
            return
            
        action_lines = [line.strip() for line in actions_text.split('\n') if line.strip()]
        
        if not action_lines:
            print("⚠️ No action commands found")
            return
            
        # Find time range to clear existing actions
        times = []
        for line in action_lines:
            time_match = re.search(r'at\s+([\d.]+)', line)
            if time_match:
                times.append(float(time_match.group(1)))
                
        if times:
            min_time = min(times)
            max_time = max(times)
            # Clear existing actions in this time range
            self.app_data.action_list.clear_range(min_time, max_time + 0.001)  # Add small buffer for end time
            
        # Parse each action line
        for line in action_lines:
            try:
                action_entry = self._parse_action_line(line)
                if action_entry:
                    self.app_data.action_list.add_action(action_entry)
            except Exception as e:
                print(f"⚠️ EffectTranslator.parse_response -> Error parsing action line '{line}': {e}")
                
        # Save the updated action list
        self.app_data.action_list.save()
        
    def _parse_action_line(self, line: str) -> ActionEntry:
        """Parse a single action command line into an ActionEntry."""
        # Pattern to match: action_name fixture_id at time [for duration] [parameters...]
        # Examples:
        # flash parcan_pl at 0.371 channels=[blue] initial_value=1.0 end_value=0.0 duration=2.5
        # fade_channel parcan_l at 0.720 for 3.0 channel=[blue] start_value=1.0 end_value=0.0
        
        # Basic pattern: action fixture at time
        basic_match = re.match(r'(\w+)\s+(\w+)\s+at\s+([\d.]+)', line)
        if not basic_match:
            raise ValueError(f"Invalid action format: {line}")
            
        action_name = basic_match.group(1)
        fixture_id = basic_match.group(2)
        start_time = float(basic_match.group(3))
        
        # Extract duration - either "for X" or "duration=X"
        duration = 0.0
        duration_match = re.search(r'for\s+([\d.]+)', line)
        if duration_match:
            duration = float(duration_match.group(1))
        else:
            duration_param_match = re.search(r'duration=([\d.]+)', line)
            if duration_param_match:
                duration = float(duration_param_match.group(1))
                
        # Extract all parameters
        parameters = {}
        
        # Extract channel/channels parameter
        channels_match = re.search(r'channels?=\[([^\]]+)\]', line)
        if channels_match:
            channels_str = channels_match.group(1)
            # Remove quotes and split by comma
            channels = [ch.strip().strip('"\'') for ch in channels_str.split(',')]
            parameters['channel'] = channels
            
        # Extract other numeric parameters
        param_patterns = [
            r'(\w+)=([\d.]+)',  # numeric parameters like value=1.0
        ]
        
        for pattern in param_patterns:
            for match in re.finditer(pattern, line):
                param_name = match.group(1)
                param_value = float(match.group(2))
                # Skip already processed parameters
                if param_name not in ['duration']:
                    parameters[param_name] = param_value
                    
        return ActionEntry(start_time, action_name, duration, fixture_id, parameters)