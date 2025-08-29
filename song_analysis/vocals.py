"""Vocal activity detection utilities."""
from __future__ import annotations
from typing import List, Dict, Tuple
import os
import numpy as np

from song_analysis.audio_io import load_audio
from song_analysis.harmony import extract_pitch_contour

try:
    import librosa  # type: ignore
except ImportError:  # pragma: no cover
    librosa = None  # type: ignore

def detect_vocals_activity(vocals_path: str) -> Tuple[List[Dict[str, float]], List[float]]:
    """Detect vocal active segments & pitch contour.

    Heuristic approach using RMS percentile > 60 as activity threshold.
    Returns:
        (list_of_active_windows, pitch_contour)
    """
    print(f"-- vocals: {vocals_path}")
    if not os.path.exists(vocals_path):
        return [], []
    y, sr = load_audio(vocals_path)
    if librosa is None:
        return [], []
    frame_length = 4096
    hop_length = 1024
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    times = librosa.frames_to_time(range(len(rms)), sr=sr, hop_length=hop_length)
    threshold = float(np.percentile(rms, 40))
    active_mask = rms > threshold
    sections: List[Dict[str, float]] = []
    start = None
    for t, is_active in zip(times, active_mask):
        if is_active and start is None:
            start = t
        elif (not is_active) and start is not None:
            if t - start > 0.5:
                sections.append({"start": float(start), "end": float(t)})
            start = None
    if start is not None:
        sections.append({"start": float(start), "end": float(times[-1])})
    
    # Merge sections with gaps < 3.0s
    merged_sections: List[Dict[str, float]] = []
    for sec in sections:
        if not merged_sections or sec["start"] - merged_sections[-1]["end"] > 3.0:
            merged_sections.append(sec)
        else:
            merged_sections[-1]["end"] = sec["end"]
    
    sections = merged_sections
    pitch = extract_pitch_contour(y, sr)
    return sections, pitch
