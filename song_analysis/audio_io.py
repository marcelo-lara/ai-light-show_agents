"""Audio loading helpers.

Abstraction layer around librosa / soundfile so higher‑level modules
can stay focused on DSP / feature extraction logic.
"""
from __future__ import annotations
import os
from typing import Tuple
import numpy as np

try:  # Optional dependencies
    import librosa  # type: ignore
except ImportError:  # pragma: no cover - environment dependent
    librosa = None  # type: ignore

try:
    import soundfile as sf  # type: ignore
except ImportError:  # pragma: no cover
    sf = None  # type: ignore

def load_audio(path: str, sr: int = 44100) -> Tuple[np.ndarray, int]:
    """Load an audio file as mono float32 array.

    Args:
        path: Path to audio file.
        sr: Desired sample rate (only enforced if librosa present).
    Returns:
        (audio, sample_rate)
    Raises:
        FileNotFoundError: If the file does not exist.
        RuntimeError: If no backend is available.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    if librosa is not None:
        y, sr_loaded = librosa.load(path, sr=sr, mono=True)
        return y, int(sr_loaded)
    if sf is not None:  # fallback backend
        y, sr_read = sf.read(path)
        if isinstance(y, np.ndarray) and y.ndim > 1:
            y = y.mean(axis=1)
        return y.astype('float32'), int(sr_read)
    raise RuntimeError("Need librosa or soundfile installed to load audio")
