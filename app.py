from models.app_data import app_data
song_name = "born_slippy"

print(f"Using base folder: {app_data.base_folder}\n")

# list fixtures
print("## fixtures")
for fixture in app_data.fixtures:
    print(f" - {fixture.name} ({fixture.type})")

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
for plan_entry in app_data.plan:
    print(f" - {plan_entry.name} ({plan_entry.start} - {plan_entry.end})")
    print(f"   {plan_entry.description}")
    print(f"   {app_data.song.get_beats_array(plan_entry.start, plan_entry.end)}")

####################################################################################################################################


# 3. Translate Effects into Actionrs
