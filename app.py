import os
from utils import write_file
from agents.effect_tramslator.effect_translator import EffectTranslator
from models.agent.agent import Agent
from models.app_data import app_data
from models.lighting.plan import PlanEntry
song_name = "born_slippy"

####################################################################################################################################
os.system('clear')
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

####################################################################################################################################

agent = Agent()
print("\n## Agents")
print(f" - Server URL: {agent.server_url}")
print(f" - Available Models:")
for model in agent.get_models():
    print(f"   - {model}")

# 3. Translate Effects into Actions
effect_translator = EffectTranslator()

user_prompt = plan_entry.description
beat_array = app_data.song.get_beats_array(plan_entry.start, plan_entry.end)

actions_reference = {}
for fixture in app_data.fixtures:
    for action in fixture.actions:
        actions_reference[action.name] = action
        
for action_name, action in actions_reference.items():
    print(f" - Action: {action_name}")
    for param in action.parameters:
        print(f"   - Param: {param}")

context = effect_translator.parse_context(
    song=app_data.song, 
    beats=beat_array, 
    fixtures=app_data.fixtures, 
    actions_reference=actions_reference,
    user_prompt=user_prompt)
write_file(str(app_data.logs_folder / "effect_translator.context.txt"), context)

print("\n## EffectTranslator")
print(f" - Model: {effect_translator.model}")
print(f" - Prompt: {len(context)}")

print("\n## Calling Agent")
effect_translator.run()