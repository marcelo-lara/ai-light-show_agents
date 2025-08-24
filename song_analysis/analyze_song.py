from common.models.song.song import Song


## Setup
song_name = "born_slippy"
base_folder = "/home/darkangel/ai-light-show_agents"
song = Song(name=song_name, base_folder=base_folder)

print(f"Using base folder: {song.base_folder} -> song: {song.mp3_file}\n")


## Features Extraction #######################

# Split audio stems

# Extract beats and BPM from drums stem

# Extract spectrograms from audio stems

# Extract chroma and MFCC features from audio stems

## try https://pypi.org/project/music-mood-analysis/

## Song Analysis ##############################
#explore https://pypi.org/search/?q=audio&o=&c=Topic+%3A%3A+Multimedia+%3A%3A+Sound%2FAudio+%3A%3A+Analysis

# Find key moments in the song

# Cluster similar sections (repetitive patterns in stems)

# Analyze song structure (sections, transitions, drops, etc.)