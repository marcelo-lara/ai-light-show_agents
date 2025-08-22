import sys
import os

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Add the backend directory to Python path
backend_path = os.path.join(project_root, 'backend')
sys.path.insert(0, backend_path)

from models.song.song import Song


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

## Song Analysis ##############################

# Find key moments in the song

# Cluster similar sections (repetitive patterns in stems)

# Analyze song structure (sections, transitions, drops, etc.)