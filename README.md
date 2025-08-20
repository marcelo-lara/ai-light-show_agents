ai-light-show_agents
=====================

Light-show planning helpers with AI-assisted effect translation.

Overview
--------
This repository provides a small toolkit for planning and rendering DMX lighting effects for songs. It combines domain models (fixtures, plan, song beats), a DMX canvas renderer, and small "agent" classes that build prompts and call a local LLM service (Ollama) to translate high-level plan descriptions into concrete lighting actions.

Key components
--------------
- `app.py` — example CLI demonstrating a canonical flow: load song, display fixtures, prepare a plan entry, create an `EffectTranslator`, and render the DMX canvas.
- `models/` — domain models for song, lighting, fixtures, DMX canvas, and action lists.
- `agents/` — AI-facing classes and Jinja prompt templates. `Agent` provides the base logic and streaming call to the Ollama server. `EffectTranslator` prepares prompts to translate plan entries into `ActionEntry` items.
- `agents/prompts/` — Jinja2 prompt templates used to build agent contexts. Editing these changes how the AI reasons about effects.
- `data/` and `songs/` — test data and audio files used by the example flow.

Quick start
-----------
Prerequisites
- Python 3.10+ (a virtualenv is recommended)
- Docker & docker-compose (for the local Ollama LLM server)

1) Start the Ollama LLM service used by agents

```bash
# from repo root
docker-compose up -d llm-service
```

2) Install Python dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install jinja2 aiohttp
```

3) Run the example flow

```bash
python app.py
```

Files and conventions
---------------------
- Prompts: agent prompt templates live at `agents/prompts/*.j2`. `Agent.parse_context()` converts a class name to a template filename using a camelCase->snake_case rule.
- Persisted actions: action lists are saved as JSON files named `{song_name}.actions.json` under the `data/` folder.
- DMX frames: `DMXCanvas` stores frames as `bytearray(512)`, keyed by float timestamps rounded to 2 decimals.

Development notes
-----------------
- When editing prompts, keep short iterative changes and re-run the example flow to inspect outputs in the `logs/` folder.
- The AI client code expects an Ollama server at `http://localhost:11434`. You can change this by passing a different `server_url` when creating an `Agent`.

Testing & sanity checks
-----------------------
- The repository has no formal unit test suite yet. Use `app.py` as the canonical smoke test.
- Before opening a PR, ensure `python app.py` imports fine in your environment (install `aiohttp` and `jinja2` if needed).

Contributing
------------
- Edit prompts under `agents/prompts/` to change agent behavior.
- Add new agent classes by subclassing `Agent` and adding a matching prompt template named with the snake_case rule.
- Use `AppData()` to access shared data and avoid direct file reads.

Contact
-------
Open issues or PRs in the repository for questions, bug reports, or feature requests.
