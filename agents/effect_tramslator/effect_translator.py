from models.app_data import AppData
from models.agent.agent import Agent

class EffectTranslator(Agent):
    def __init__(self):
        super().__init__(model="gpt-4o-mini")

