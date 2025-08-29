"""Rhythm and percussion feature extraction.

Includes:
    - Tempo & beat tracking
    - Kick / snare onset heuristics
"""
from __future__ import annotations
from typing import List, Dict, Tuple, Optional
import os
import numpy as np

from song_analysis.audio_io import load_audio

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

def detect_percussive_onsets(y: np.ndarray, sr: int, drums_path: Optional[str] = None) -> Dict[str, List[float]]:
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
    
    # Use drums stem if available, otherwise use full mix
    if drums_path and os.path.exists(drums_path):
        print(f"-- drums: {drums_path}")
        drums_y, drums_sr = load_audio(drums_path)
        # Resample if necessary
        if drums_sr != sr:
            drums_y = librosa.resample(drums_y, orig_sr=drums_sr, target_sr=sr)
        analysis_y = drums_y
    else:
        analysis_y = y
    
    onset_env = librosa.onset.onset_strength(y=analysis_y, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, backtrack=True, pre_max=3, post_max=3, pre_avg=3, post_avg=5, delta=0.1, wait=5)
    onsets = librosa.frames_to_time(onset_frames, sr=sr)
    S = np.abs(librosa.stft(y))
    freqs = librosa.fft_frequencies(sr=sr)
    kick_band = (freqs >= 60) & (freqs <= 100)  # Narrower kick band
    snare_band = (freqs >= 150) & (freqs <= 4000)  # Broader snare band
    kick_energy = S[kick_band].mean(axis=0)
    snare_energy = S[snare_band].mean(axis=0)
    for t in onsets:
        frame = librosa.time_to_frames([t], sr=sr)[0]
        ke = kick_energy[frame] if frame < len(kick_energy) else 0
        se = snare_energy[frame] if frame < len(snare_energy) else 0
        ratio = ke / (se + 1e-6)  # Avoid division by zero
        if ratio > 3.0 and ke > 0.01:  # Stricter for kicks
            results['kick_onsets'].append(float(t))
        elif ratio < 1.5 and se > 0.003:  # Very lenient for snares
            results['snare_onsets'].append(float(t))
        elif ke > 0.03 or se > 0.03:  # Fallback for moderate energy
            (results['kick_onsets'] if ratio >= 1.5 else results['snare_onsets']).append(float(t))
    return results
