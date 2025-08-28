"""Section segmentation heuristics."""
from __future__ import annotations
from typing import List
import numpy as np
from song_analysis.schema import SectionEntry

try:
    import librosa  # type: ignore
except ImportError:  # pragma: no cover
    librosa = None  # type: ignore

def segment_structure(y: np.ndarray, sr: int) -> List[SectionEntry]:
    """Generate coarse section boundaries.

    Current approach:
        1. Attempt feature extraction & agglomerative boundary guess (if available).
        2. Fallback: even division into 6 parts.
    """
    sections: List[SectionEntry] = []
    duration = len(y) / sr
    if librosa is not None:
        try:
            y_harm, _y_perc = librosa.effects.hpss(y)
            # Compute energy curve
            hop_length = int(0.2 * sr / 2)
            energy = librosa.feature.rms(y=y, frame_length=2*hop_length, hop_length=hop_length)[0]
            # If agglomerative segmentation present, attempt it; else fallback.
            if hasattr(librosa.segment, 'agglomerative'):
                # Use energy curve for segmentation; target ~8 segments.
                boundaries = librosa.segment.agglomerative(energy.reshape(1, -1), k=8)
                boundary_times = librosa.frames_to_time(boundaries, sr=sr, hop_length=hop_length)
            else:
                raise RuntimeError('agglomerative not available')
        except Exception:  # fallback evenly spaced
            step = duration / 8
            boundary_times = np.array([i * step for i in range(9)])
    else:
        step = duration / 8
        boundary_times = np.array([i * step for i in range(9)])
    labels = ["intro","verse","verse","verse","instrumental","chorus","bridge","outro"]
    for i in range(len(boundary_times) - 1):
        label = labels[i] if i < len(labels) else f"part{i}"
        sections.append(SectionEntry(label, float(boundary_times[i]), float(boundary_times[i+1])))
    return sections
