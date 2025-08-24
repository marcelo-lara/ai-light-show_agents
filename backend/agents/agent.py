import json
import re
import asyncio
import aiohttp
from urllib import request
from jinja2 import Environment, FileSystemLoader
from ..models.app_data import AppData
from ..utils import write_file

class Agent:
    def __init__(self, model:str = "gpt-4o-mini", server_url: str = "http://localhost:11434"):
        self.app_data = AppData()
        self.model = model
        self.server_url = server_url
        self._last_response = ''
        self._context = ''
        self._thinking = False

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

        # Add common template vars
        if 'song' not in args:
            args['song'] = self.app_data.song
        if 'fixtures' not in args:
            args['fixtures'] = self.app_data.fixtures
        
        context = template.render(agent=self, **args)
        self._context = context
        return context

    async def run_async(self):
        """Call the ollama server async with streaming and display partial results."""
        if self._context == '':
            raise ValueError("Context is empty. Please call parse_context() first.")
        
        payload = {
            "model": self.model,
            "prompt": self._context,
            "stream": True
        }
        
        print(f"🤖 AI Response ({self.model} | streaming):")
        print("-" * 50)
        print("🧠 Model is thinking...", end='', flush=True)
        
        full_response = ""
        thinking_dots = 0
        self._thinking = True  # Agent is now thinking
        
        try:
            # Set longer timeout and disable read timeout for initial connection
            timeout = aiohttp.ClientTimeout(total=None, sock_read=600)
            connector = aiohttp.TCPConnector(keepalive_timeout=600)
            
            async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
                async with session.post(
                    f"{self.server_url}/api/generate",
                    json=payload
                ) as response:
                    if response.status == 200:
                        async for line in response.content:
                            if line:
                                try:
                                    data = json.loads(line.decode('utf-8'))
                                    if 'response' in data and data['response']:
                                        if self._thinking:
                                            print("\n" + "-" * 50)
                                            self._thinking = False  # Agent has started responding
                                        
                                        chunk = data['response']
                                        print(chunk, end='', flush=True)
                                        full_response += chunk
                                        
                                    if data.get('done', False):
                                        break
                                except json.JSONDecodeError:
                                    continue
                            else:
                                # Show thinking animation while waiting
                                if self._thinking:
                                    thinking_dots = (thinking_dots + 1) % 4
                                    print('\r🧠 Model is thinking' + '.' * thinking_dots + ' ' * (3 - thinking_dots), end='', flush=True)
                                    await asyncio.sleep(0.5)
                    else:
                        error_text = await response.text()
                        raise ValueError(f"Error from Ollama server: {response.status} - {error_text}")
        except asyncio.TimeoutError:
            raise ValueError("Request to Ollama server timed out")
        except Exception as e:
            raise ValueError(f"Error calling Ollama: {e}")
        
        if not self._thinking:
            print("\n" + "-" * 50)
        else:
            print("\n❌ No response received from model")
            
        self._last_response = full_response
        
        # Write the response to a file
        write_file(str(self.app_data.logs_folder / f"{self.__class__.__name__}.response.txt"), full_response)

        return full_response

    def run(self):
        """Synchronous wrapper for async run."""
        return asyncio.run(self.run_async())
        