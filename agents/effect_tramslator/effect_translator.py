from models.app_data import AppData
from models.agent.agent import Agent

class EffectTranslator(Agent):
    def __init__(self, app_data: AppData):
        super().__init__(app_data)

