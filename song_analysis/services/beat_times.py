import librosa
from BeatNet.BeatNet import BeatNet
import numpy as np

def extract_beats_and_downbeats(audio_file_path):
    """
    Extracts beat and downbeat times from an audio file using BeatNet.

    Args:
        audio_file_path (str): The path to the audio file.

    Returns:
        tuple: A tuple containing two NumPy arrays:
               - beat_times (float): The beat times in seconds.
               - downbeat_times (float): The downbeat times in seconds.
    """
    # Initialize the BeatNet estimator in offline mode
    # `1` specifies a pre-trained model (1, 2, or 3)
    # `mode='offline'` is for processing a full file
    # `inference_model='PF'` uses Particle Filtering for inference
    estimator = BeatNet(1, mode='offline', inference_model='PF', plot=[], thread=False)

    try:
        # Load the audio file. BeatNet is optimized for 22050 Hz.
        # It handles the resampling internally if you provide a file path.
        output_results = estimator.process(audio_file_path)

        # The output is a NumPy array with shape (number_of_events, 2),
        # where the first column is the timestamp and the second is the event type.
        # Event type 1 is a beat, and type 2 is a downbeat.
        
        # Filter for beat times (event type 1)
        beat_times = output_results[output_results[:, 1] == 1, 0]
        
        # Filter for downbeat times (event type 2)
        downbeat_times = output_results[output_results[:, 1] == 2, 0]

        return beat_times, downbeat_times

    except Exception as e:
        print(f"An error occurred: {e}")
        return np.array([]), np.array([])

# --- Example Usage ---
if __name__ == '__main__':
    audio_file = "/home/darkangel/ai-light-show_agents/songs/born_slippy.mp3"

    print(f"Starting beat detection for: {audio_file}")
    
    # Run the function
    beats, downbeats = extract_beats_and_downbeats(audio_file)

    if beats.size > 0:
        print("\n--- Detected Beats ---")
        # Print the first 20 beat times to keep the output concise
        for i, beat_time in enumerate(beats[:20]):
            print(f"Beat {i+1}: {beat_time:.3f} seconds")
        
        print("\n--- Detected Downbeats ---")
        # Print the first 5 downbeat times
        for i, downbeat_time in enumerate(downbeats[:5]):
            print(f"Downbeat {i+1}: {downbeat_time:.3f} seconds")
        
        print(f"\nTotal beats detected: {len(beats)}")
        print(f"Total downbeats detected: {len(downbeats)}")
    else:
        print("No beats were detected or an error occurred. Check the file path and format.")