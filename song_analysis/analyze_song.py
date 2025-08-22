from ..backend.models.song import Song


## Setup
song_name = "born_slippy"
base_folder = "/home/darkangel/ai-light-show_agents"
song = Song(name=song_name, base_folder=base_folder)

print(f"Using base folder: {song.base_folder} -> song: {song.mp3_file}\n")

