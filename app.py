from models.app_data import AppData

app_data = AppData()
song_name = "born_slippy"

# list fixtures
print("## fixtures")
for fixture in app_data.fixtures:
    print(f" - {fixture.name} ({fixture.type})")

# Song