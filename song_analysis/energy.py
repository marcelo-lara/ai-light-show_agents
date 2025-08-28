"""Energy curve computation."""
from __future__ import annotations
from typing import List
import numpy as np

try:
    import librosa  # type: ignore
except ImportError:  # pragma: no cover
    librosa = None  # type: ignore

def compute_energy_curve(y: np.ndarray, sr: int, window_s: float = 0.5) -> List[float]:
    """Compute RMS energy curve.

    Uses overlapping windows (50% hop) if librosa present; else manual blocks.
    """
    if librosa is not None:
        hop_length = int(window_s * sr / 2)
        rms = librosa.feature.rms(y=y, frame_length=2*hop_length, hop_length=hop_length)[0]
        return rms.astype(float).tolist()
    block = int(window_s * sr)
    return [float(np.sqrt(np.mean(y[i:i+block] ** 2))) for i in range(0, len(y), block) if len(y[i:i+block]) == block]
