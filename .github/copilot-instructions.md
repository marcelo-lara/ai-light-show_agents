# Copilot instructions for ai-light-show_agents

Purpose: give an AI coding agent the minimal, actionable knowledge to be productive in this repo.

High-level architecture
- `app.py` is a small CLI-ish entry that wires core pieces (AppData, Agent, EffectTranslator, DMXCanvas) and demonstrates usage.
- `models/` contains domain models: `app_data.py` (singleton AppData), `song/`, `lighting/` (Plan/PlanEntry), `fixtures/` (FixtureList). Data lives in `data/` and `songs/`.
- `agents/` contains AI-facing classes and Jinja prompts: `agents/agent.py` (base Agent), `agents/effect_tramslator/effect_translator.py` (EffectTranslator), and `agents/prompts/*.j2` templates.
- `models/dmx/dmx_canvas.py` holds the DMX frame buffer used to render lighting output (512-channel bytearrays keyed by time).
- Integration: an external Ollama LLM service (docker-compose: `llm-service`) on `http://localhost:11434` is expected for inference.

Key files to inspect (examples)
- `app.py` — shows a canonical run: load song, print fixtures, create Agent and EffectTranslator, start DMXCanvas.
- `models/app_data.py` — AppData singleton: base_folder, prompts_folder, fixtures, plan, logs_folder.
- `agents/agent.py` — parse_context() template convention and `run_async()` which streams to Ollama `/api/generate`.
- `agents/effect_tramslator/effect_translator.py` — builds actions_reference from fixtures, calls parse_context, writes context to logs.
- `agents/prompts/*.j2` — edit these to change agent prompts (template variables: `agent`, `song`, `fixtures`, plus extras passed by callers).
- `models/dmx/dmx_canvas.py` — DMX frame logic: 512 channels, fps default 50, frames keyed by rounded floats.

Project-specific conventions and patterns
- Template naming: `Agent.parse_context` converts a class name into a template filename by turning CamelCase -> snake_case and appending `.j2`. Example: `EffectTranslator` -> `effect_translator.j2` (see `agents/agent.py`).
- Template vars: `agent` is always available in templates. `Agent.parse_context` injects `song` and `fixtures` unless explicitly provided.
- Logs: agents write files to `app_data.logs_folder` using `utils.write_file`. Typical filenames: `effect_translator.context.txt` and `EffectTranslator.response.txt`.
- Models/API: the agent uses Ollama endpoints: `GET /api/tags` to list models and `POST /api/generate` for streaming responses; default server_url is `http://localhost:11434` and default model used in code is `gpt-4o-mini` (EffectTranslator overrides to `cogito:8b`).
- DMX indexing: `DMXCanvas` stores frames as `bytearray(512)` and uses 0-based indexing in code. When generating DMX channel values, validate whether other systems expect 1-based channels.
- Time-keyed frames: frames keys are floats rounded to 2 decimals (see `init_canvas`), and `get_frame()` returns the nearest previous frame when an exact timestamp is missing.
- NEVER read Json files directly, always use the provided data access methods in the AppData singleton.
- ALWAYS use public properties of AppData and its contained models. Do not use internal _variables or __private_variables.

Developer workflows (concrete commands)
- Start the LLM service (uses the included compose file): run `docker-compose up -d llm-service` from the repo root to start Ollama as configured in `docker-compose.yml`.
- Verify available models: either call `Agent().get_models()` in a short script or hit `http://localhost:11434/api/tags`.
- Run the example CLI: `python app.py` (ensure your Python environment has required libs: jinja2, aiohttp).
- Where to look for outputs: generated logs go to `logs/` and example outputs referenced in `app.py` include `effect_translator.context.txt` and the DMX canvas printout.

Integration points & external deps
- Ollama LLM service (docker image `ollama/ollama`) — docker-compose file maps port 11434. Expected to be running locally.
- Local data files: `data/*.json|.pkl` (plan/beat/chord/meta), `songs/*.mp3`, and `fixtures/fixtures.json` drive behavior. Agents build prompts from those inputs.

Quick tips for making changes safely
- To change prompt structure, edit `agents/prompts/<template>.j2` and test by running the small flow in `app.py` or calling `EffectTranslator().parse_plan_entry(...)` and then `EffectTranslator().run()`.
- When producing DMX frames, respect 0-based channel indexing and the 512-channel frame size.
- Add new agent classes by subclassing `Agent` and providing a matching prompt template named with the snake_case rule.

What I looked for and merging notes
- No existing `.github/copilot-instructions.md`, `AGENT.md`, or similar agent-guides were found in the repo — this file is new.

If anything here is unclear or you want the file tuned (more examples, troubleshooting steps, or CI/test instructions), tell me which area to expand and I will iterate.
