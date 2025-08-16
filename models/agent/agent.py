import json
import re
from urllib import request
from jinja2 import Environment, FileSystemLoader
from models.app_data import AppData

class Agent:
    def __init__(self, model:str = "gpt-4o-mini", server_url: str = "http://localhost:11434"):
        self.app_data = AppData()
        self.model = model
        self.server_url = server_url
        self._last_response = ''
        self._context = ''

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

    def parse_context(self, **args) -> str:
        # parse jinja template for inherited class (e.g. EffectTranslator -> effect_translator.j2)
        # jinja folder is app_data.prompts_folder
        class_name = self.__class__.__name__
        template_name = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower() + ".j2"
        
        env = Environment(loader=FileSystemLoader(self.app_data.prompts_folder))
        template = env.get_template(template_name)
        
        return template.render(agent=self, **args)

    def run(self):
        """Call the ollama server with the parsed context."""
        if self._context == '':
            raise ValueError("Context is empty. Please call parse_context() first.")
        