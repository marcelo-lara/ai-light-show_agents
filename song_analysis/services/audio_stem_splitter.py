
import os
from spleeter.separator import Separator

def split_audio_stems(audio_file: str, output_dir: str):
    """
    Split the audio file into separate stems and save them to the output directory.
    """

    # Using embedded configuration.
    separator = Separator('spleeter:4stems')

    # Split the audio into stems (drums, bass, vocals, other)
    separator.separate_to_file(audio_file, output_dir)

if __name__ == "__main__":
    audio_file = "/home/darkangel/ai-light-show_agents/songs/born_slippy.mp3"
    output_dir = "/home/darkangel/ai-light-show_agents/stems"
    split_audio_stems(audio_file, output_dir)