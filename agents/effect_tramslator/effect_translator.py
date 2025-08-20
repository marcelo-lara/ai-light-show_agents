from models.app_data import AppData
from agents.agent import Agent
from models.lighting.plan import PlanEntry
from utils import write_file

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
        # TODO: parse each line received from the model into ActionEntry and add it to the ActionList
        # remove actions within the same time range (only if the response contains actions)
        # ```actions
        # flash parcan_pl at 0.371 channels=[blue] initial_value=1.0 end_value=0.0 duration=2.5
        # fade_channel parcan_l at 0.720 for 3.0 channel=[blue] start_value=1.0 end_value=0.0
        # flash parcan_r at 1.045 channels=[blue] initial_value=1.0 end_value=0.0 duration=1.8
        # fade_channel parcan_pl at 1.370 for 2.5 channel=[blue] start_value=1.0 end_value=0.0
        # flash parcan_pr at 1.695 channels=[blue] initial_value=1.0 end_value=0.0 duration=3.7
        # ```        
        
        pass