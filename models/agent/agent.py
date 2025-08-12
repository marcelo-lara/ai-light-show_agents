from models.app_data import AppData

class Agent:
    def __init__(self, model:str = "gpt-4o-mini", server_url: str = "http://localhost:8000"):
        self.app_data = AppData()
        self.model = model
        self.server_url = server_url

    def get_models(self) -> list[str]:
        '''Get a list of model names from ollama server'''
        # get ollama list (models)
        return []

    def parse_context(self):
        # parse jinja template for inherited class (e.g. EffectTranslator -> effect_translator.j2)
        pass

    def run(self):
        """Call the ollama server with the parsed context."""
        pass