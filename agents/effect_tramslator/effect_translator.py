from models.app_data import AppData
from models.agent.agent import Agent

class EffectTranslator(Agent):
    def __init__(self, model:str = "qwen3:8b"):
        self._model = model
        super().__init__(model=self._model)

