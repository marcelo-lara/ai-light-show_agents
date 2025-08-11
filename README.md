# AI Light Show Agents

## Overview

AI Light Show Agents is a modular Python application for generating, planning, and controlling lighting effects for music tracks. It leverages song structure, beat analysis, and fixture metadata to create synchronized lighting plans and DMX commands for live shows or simulations.

## Features

- **Song Analysis**: Loads song metadata, sections, beats, and key moments from JSON files.
- **Lighting Plan**: Associates lighting effects and timings with song sections and beats.
- **Fixture Management**: Supports multiple fixture types (e.g., moving heads, parcans) with detailed channel and action definitions.
- **Prompt-based Agents**: Uses Jinja2 templates for context building, effect translation, and direct command generation.
- **Extensible Models**: Modular Python classes for fixtures, lighting, and song data.

## Project Structure

```
.
├── app.py                # Main entry point: loads song, fixtures, and prints plan info
├── agents/               # Agent logic and prompt templates
│   ├── effect_tramslator/
│   │   └── effect_translator.py
│   └── prompts/          # Jinja2 templates for agents
├── data/                 # Song metadata, beats, plans, and analysis
├── fixtures/             # Fixture definitions (JSON)
├── models/               # Core Python models for fixtures, lighting, and songs
│   ├── fixtures/
│   ├── lighting/
│   └── song/
├── songs/                # MP3 files
```

## How It Works

1. **Fixtures**: Defined in `fixtures/fixtures.json` and loaded via `models/fixtures/fixture_list.py`.
2. **Songs**: Metadata, beats, and plans are loaded from `data/` (e.g., `born_slippy.meta.json`, `born_slippy.beats.json`).
3. **Lighting Plan**: Defined in `data/{song}.plan.json` and managed by `models/lighting/plan.py`.
4. **Agents**: Jinja2 templates in `agents/prompts/` generate context, translate effects, and provide direct commands for DMX control.
5. **Main App**: `app.py` demonstrates loading a song, listing fixtures, and printing the lighting plan.

## Example Usage

Run the main app to see loaded fixtures, song info, and lighting plan:

```bash
python app.py
```

## Data Files

- `data/born_slippy.meta.json`: Song metadata (title, genre, bpm, sections, etc.)
- `data/born_slippy.beats.json`: Array of beat times and features
- `data/born_slippy.plan.json`: Lighting plan entries (timed effects)
- `fixtures/fixtures.json`: List of available lighting fixtures and their DMX channels

## Extending

- **Add new fixtures**: Edit `fixtures/fixtures.json` and update models if needed.
- **Add new songs**: Place MP3 in `songs/`, add metadata and beats in `data/`.
- **Customize prompts**: Edit or add Jinja2 templates in `agents/prompts/`.
