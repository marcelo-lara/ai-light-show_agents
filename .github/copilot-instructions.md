# Copilot instructions for ai-light_show_agents

Purpose
-------
Provide an automated contributor/agent guide with minimal, concrete steps to be productive in this repository.

High-level architecture
-----------------------
- `app.py` is a small CLI-style example that wires core pieces (AppData, Agent, EffectTranslator, DMXCanvas) and demonstrates repository usage.
- `models/` contains domain models: `app_data.py` (singleton AppData), `song/`, `lighting/` (Plan/PlanEntry), and fixtures. Data lives in `data/` and `songs/`.
- `agents/` contains AI-facing classes and Jinja prompts: `agents/agent.py` (base Agent), `agents/effect_tramslator/effect_translator.py` (EffectTranslator), and `agents/prompts/*.j2` templates used to build prompts.
- `models/dmx/dmx_canvas.py` holds the DMX frame buffer used to render lighting output (512-channel bytearrays keyed by time).
- Integration with an LLM service (configured via Docker Compose as `llm-service`) is expected at `http://localhost:11434`.

Key files to inspect
--------------------
- `app.py` — canonical usage: load song, print fixtures, create Agent and EffectTranslator, render the DMX canvas, and run an example flow.
- `models/app_data.py` — the AppData singleton. Preferred access point for data folders, fixtures, loaded `Song`, `Plan`, `ActionList`, and `DMXCanvas` instances.
- `agents/agent.py` — base Agent implementation: builds prompt context from Jinja templates and calls the LLM (Ollama) streaming API. Inspect `parse_context()` and `run_async()`.
- `agents/effect_tramslator/effect_translator.py` — translates plan entries into action commands. Uses `get_actions_reference()` and `parse_plan_entry()` to prepare prompts.
- `agents/prompts/*.j2` — edit these to control how agents reason. Template variables: `agent`, `song`, `fixtures`, plus any extras passed by callers.
- `models/dmx/dmx_canvas.py` — DMX canvas logic: 512 channels, FPS default 50, frames keyed to rounded floats. Rendering helpers and frame accessors are here.

Conventions and important rules
-----------------------------
- Template naming: `Agent.parse_context` converts a class name to snake_case and appends `.j2`. Example: `EffectTranslator` -> `effect_translator.j2`.
- Template variables: `agent` is always available. `parse_context()` will inject `song` and `fixtures` unless callers provide alternatives.
- Persistence: action lists are stored as JSON files named `{song_name}.actions.json` under the AppData `data_folder`.
- DO NOT read JSON files directly in code — use AppData helpers and public properties (`AppData().data_folder`, `AppData().song`, etc.).
- DMX frames are 0-indexed in code (512 channels). Confirm external hardware expectations before changing indexing.
- DO NOT keep backward compatibility in mind when making changes.
- DO NOT introduce fallback variants unless explicitly requested.

Developer workflows (concrete commands)
--------------------------------------
- Start the LLM service used by the agents (Ollama):
  - From the repo root run: `docker-compose up -d llm-service`
- Verify available models: call `Agent().get_models()` in a short script, or GET `http://localhost:11434/api/tags`.
- Run the example CLI: `python app.py` (ensure your Python environment has required libs such as `jinja2` and `aiohttp`).

Where outputs are written
------------------------
- Generated logs: `logs/` (examples include `effect_translator.context.txt` and `EffectTranslator.response.txt`).
- Persistent action lists: `data/{song_name}.actions.json`.

Integration points & external dependencies
-----------------------------------------
- Ollama LLM service (docker image `ollama/ollama`) — configured in `docker-compose.yml`, exposed on port 11434. The repo expects this to be available locally for agent runs.
- Local content: `data/*.json|.pkl` (plan/beat/chord/meta), `songs/*.mp3`, and `fixtures/fixtures.json` drive prompt construction and rendering.

Quick tips for safe changes
--------------------------
- To modify agent prompts, edit `agents/prompts/<template>.j2` and test via `EffectTranslator().parse_plan_entry(...)` followed by `EffectTranslator().run()`.
- Respect DMX channel indexing and 512-channel frame size when producing frames.
- To add a new Agent subclass, follow the naming convention and add a corresponding prompt template in `agents/prompts/`.

Troubleshooting notes
---------------------
- If `python app.py` fails with `ModuleNotFoundError` for `aiohttp`, install dependencies in your virtualenv (`pip install aiohttp jinja2`) or use the project's recommended environment.
- If the Ollama server is unreachable, ensure Docker is running and `docker-compose up -d llm-service` completed successfully.

If anything here is unclear or you want the file tuned (more examples, troubleshooting steps, or CI/test instructions), tell me which area to expand and I will iterate.
