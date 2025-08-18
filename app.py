import asyncio
import os
import time
from typing import Dict
from models.dmx.dmx_canvas import DMXCanvas
from utils import write_file
from agents.effect_tramslator.effect_translator import EffectTranslator
from agents.agent import Agent
from models.app_data import AppData
from models.lighting.plan import PlanEntry
song_name = "born_slippy"

####################################################################################################################################
os.system('clear')
app_data = AppData()
print(f"Using base folder: {app_data.base_folder}\n")

# list fixtures
print("## fixtures")
for fixture in app_data.fixtures:
    print(f" - {fixture.name} ({fixture.type})")
    for action in fixture.actions:
        print(f"   - {action}")
        for param in action.parameters:
            print(f"     - {param}")

# Song
app_data.load_song(song_name)
print(f"\n## Song")
print(f" - Name: {app_data.song_name}")
print(f" - BPM: {app_data.song.bpm}")

print("\n### Sections")
for section in app_data.song.sections:
    print(f" - {section.name} ({section.start} - {section.end})")

print("\n### Key Moments")
for key_moment in app_data.song.key_moments:
    print(f" - {key_moment.name} ({key_moment.start} - {key_moment.end})")

print("\n## Lighting Plan")
plan_entry:PlanEntry = app_data.plan[0]
print(f" - {plan_entry.name} ({plan_entry.start} - {plan_entry.end})")
print(f"   {plan_entry.description}")
print(f"   {app_data.song.get_beats_array(plan_entry.start, plan_entry.end)}")


## Start DMX Canvas
print("\n## DMX Canvas")
dmx_canvas = app_data.dmx_canvas
print(dmx_canvas.get_canvas_log(end_time=0.1, last_channel=40))

####################################################################################################################################
# Test Fixture render
print("\n## Fixture Render")
app_data.fixtures.arm_all_fixtures()
fixture = app_data.fixtures[1]
fixture.set_channel(['blue'], 1.0, 0.0, 1.0)
fixture.fade_channel(['red'],
                        start_time=0.0,
                        duration=1.0,
                        start_value=0.1,
                        end_value=0.9
                     )
print(dmx_canvas.get_canvas_log(end_time=0.1, last_channel=40))

####################################################################################################################################
print("\n## ActionList")
action_list = app_data.action_list
for action in action_list:
    print(f" - {action}")

####################################################################################################################################
agent = Agent()
print("\n## Agents")
print(f" - Server URL: {agent.server_url}")
print(f" - Available Models:")
for model in agent.get_models():
    print(f"   - {model}")

# 3. Translate Effects into Actions
effect_translator = EffectTranslator()
print("\n## EffectTranslator")
print(f" - Model: {effect_translator.model}")
effect_translator.parse_plan_entry(plan_entry)

# asyncio.run(effect_translator.run_async())


