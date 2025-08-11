from models.app_data import AppData

class Agent:
    def __init__(self, app_data: AppData, model:str = "gpt-4o-mini", server_url: str = "http://localhost:8000"):
        self.app_data = app_data
        self.model = model
        self.server_url = server_url

    def parse_context(self):
        # parse jinja template for inherited class
        pass

    def run(self):
        """Call the ollama server with the parsed context."""
        pass