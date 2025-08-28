"""Pitch & key related extraction."""
from __future__ import annotations
from typing import List
import numpy as np

try:
    import librosa  # type: ignore
except ImportError:  # pragma: no cover
    librosa = None  # type: ignore

try:
    import essentia  # type: ignore
    import essentia.standard as es  # type: ignore
except ImportError:  # pragma: no cover
    essentia = None  # type: ignore
    es = None  # type: ignore

def estimate_key(y: np.ndarray, sr: int) -> str:
    """Estimate musical key (rough).

    Order: Essentia KeyExtractor -> simple chroma peak -> "Unknown".
    """
    if es is not None and hasattr(es, 'KeyExtractor'):
        try:
            key_extractor = es.KeyExtractor()  # type: ignore[attr-defined]
            key, scale, _strength = key_extractor(y)  # type: ignore[misc]
            return f"{key}{'m' if scale == 'minor' else ''}"
        except Exception:  # pragma: no cover
            pass
    if librosa is not None:
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        pitch_class = chroma.mean(axis=1).argmax()
        key_map = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        return key_map[pitch_class]
    return "Unknown"

def extract_pitch_contour(y: np.ndarray, sr: int) -> List[float]:
    """Crude f0 track via librosa piptrack (peak per frame)."""
    contour: List[float] = []
    if librosa is None:
        return contour
    pitches, mags = librosa.piptrack(y=y, sr=sr)
    for frame in range(pitches.shape[1]):
        idx = mags[:, frame].argmax()
        f0 = pitches[idx, frame]
        if f0 > 0:
            contour.append(float(f0))
    return contour
