import json
from urllib import request
from models.app_data import AppData

class Agent:
    def __init__(self, model:str = "gpt-4o-mini", server_url: str = "http://localhost:11434"):
        self.app_data = AppData()
        self.model = model
        self.server_url = server_url

    def get_models(self) -> list[str]:
        '''Get a list of model names from ollama server'''
        try:
            with request.urlopen(f"{self.server_url}/api/tags") as response:
                if response.status == 200:
                    data = json.loads(response.read())
                    return [model['name'] for model in data['models']]
        except Exception as e:
            raise ValueError(f"Error fetching models from Ollama: {e}")
        return []

    def parse_context(self) -> str:
        # parse jinja template for inherited class (e.g. EffectTranslator -> effect_translator.j2)
        return ""

    def run(self):
        """Call the ollama server with the parsed context."""
        pass
