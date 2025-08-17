from models.app_data import AppData
from agents.agent import Agent

class EffectTranslator(Agent):
    def __init__(self, model:str = "cogito:8b"):
        self._model = model
        super().__init__(model=self._model)

