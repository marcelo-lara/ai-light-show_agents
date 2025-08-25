
import os
from typing import List
from spleeter.separator import Separator

def split_audio_stems(audio_file: str, output_dir: str) -> dict[str, str]:
    """
    Split the audio file into separate stems and save them to the output directory.
    """

    # Using embedded configuration.
    separator = Separator('spleeter:4stems')

    # Split the audio into stems (drums, bass, vocals, other)
    separator.separate_to_file(audio_file, output_dir)
    audio_file_name = os.path.splitext(os.path.basename(audio_file))[0]

    # Return the list of stem file paths
    return {
        "drums": str(f"{output_dir}/{audio_file_name}/drums.wav"),
        "bass": str(f"{output_dir}/{audio_file_name}/bass.wav"),
        "vocals": str(f"{output_dir}/{audio_file_name}/vocals.wav"),
        "other": str(f"{output_dir}/{audio_file_name}/other.wav"),
    }


if __name__ == "__main__":
    audio_file = "/home/darkangel/ai-light-show_agents/songs/born_slippy.mp3"
    output_dir = "/home/darkangel/ai-light-show_agents/stems"
    split_audio_stems(audio_file, output_dir)