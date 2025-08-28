"""Rhythm and percussion feature extraction.

Includes:
    - Tempo & beat tracking
    - Kick / snare onset heuristics
"""
from __future__ import annotations
from typing import List, Dict, Tuple
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

def estimate_tempo_and_beats(y: np.ndarray, sr: int) -> Tuple[float, List[float]]:
    """Estimate tempo (BPM) and beat timestamps.

    Priority: librosa -> Essentia -> fallback (0, []).
    """
    if librosa is not None:
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, trim=False)
        beats = librosa.frames_to_time(beat_frames, sr=sr).tolist()
        return float(tempo), beats
    if es is not None and hasattr(es, 'RhythmExtractor'):
        try:
            rhythm_extractor = es.RhythmExtractor(method='multifeature')  # type: ignore[attr-defined]
            bpm, beats, _conf = rhythm_extractor(y)  # type: ignore[misc]
            return float(bpm), list(map(float, beats))
        except Exception:  # pragma: no cover
            pass
    return 0.0, []

def detect_percussive_onsets(y: np.ndarray, sr: int) -> Dict[str, List[float]]:
    """Heuristic kick/snare onset classifier.

    Strategy:
        1. Use global onset detection (librosa onset strength) for candidate times.
        2. Classify each onset via low vs mid band energy ratio.
    Returns:
        { 'kick_onsets': [...], 'snare_onsets': [...] }
    Limitations:
        Not a drum transcription model; it's a quick heuristic.
    """
    results = {"kick_onsets": [], "snare_onsets": []}
    if librosa is None:
        return results
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
    onsets = librosa.frames_to_time(onset_frames, sr=sr)
    S = np.abs(librosa.stft(y))
    freqs = librosa.fft_frequencies(sr=sr)
    kick_band = (freqs >= 40) & (freqs <= 120)
    snare_band = (freqs >= 150) & (freqs <= 2500)
    kick_energy = S[kick_band].mean(axis=0)
    snare_energy = S[snare_band].mean(axis=0)
    for t in onsets:
        frame = librosa.time_to_frames([t], sr=sr)[0]
        ke = kick_energy[frame] if frame < len(kick_energy) else 0
        se = snare_energy[frame] if frame < len(snare_energy) else 0
        if ke > se * 0.9:
            results['kick_onsets'].append(float(t))
        elif se > ke * 1.1:
            results['snare_onsets'].append(float(t))
        else:
            (results['kick_onsets'] if ke >= se else results['snare_onsets']).append(float(t))
    return results
