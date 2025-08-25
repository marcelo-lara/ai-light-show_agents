from common.models.song.song import Song
from song_analysis.models.analysis import Analysis

## Setup
song_name = "born_slippy"
analysis = Analysis()

song = Song(name=song_name, base_folder=str(analysis.base_folder))
print(f"Using base folder: {song.base_folder} -> song: {song.mp3_file}\n")


## Features Extraction #######################

# Split audio stems
print("\n## Splitting audio stems...")
from services.audio_stem_splitter import split_audio_stems
analysis.stems_files = split_audio_stems(song.mp3_file, str(analysis.stems_folder))

# Extract beats and BPM from drums stem
print("\n## Extracting beats from stems...")
from services.beat_times import extract_beats
drum_beats, drum_downbeats = extract_beats(analysis.stems_files["drums"])
main_beats, main_downbeats = extract_beats(song.mp3_file)

# Extract spectrograms from audio stems

# Extract chroma and MFCC features from audio stems

## try https://pypi.org/project/music-mood-analysis/

## Song Analysis ##############################
#explore https://pypi.org/search/?q=audio&o=&c=Topic+%3A%3A+Multimedia+%3A%3A+Sound%2FAudio+%3A%3A+Analysis

# Find key moments in the song

# Cluster similar sections (repetitive patterns in stems)

# Analyze song structure (sections, transitions, drops, etc.)