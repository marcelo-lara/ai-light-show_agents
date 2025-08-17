from models.app_data import AppData
from agents.agent import Agent
from models.lighting.plan import PlanEntry
from utils import write_file

class EffectTranslator(Agent):
    def __init__(self, model:str = "cogito:8b"):
        self._model = model
        super().__init__(model=self._model)

    def get_actions_reference(self):
        actions_reference = {}
        for fixture in self.app_data.fixtures:
            for action in fixture.actions:
                actions_reference[action.name] = action
        return actions_reference

    def parse_plan_entry(self, plan_entry:PlanEntry):
        
        user_prompt = plan_entry.description
        beats_array = self.app_data.song.get_beats_array(plan_entry.start, plan_entry.end)
        actions_reference = self.get_actions_reference()
        self.parse_context(
            beats=beats_array,
            actions_reference=actions_reference,
            user_prompt=user_prompt
        )

        write_file(str(self.app_data.logs_folder / "effect_translator.context.txt"), self._context)