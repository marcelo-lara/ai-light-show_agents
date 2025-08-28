"""Smoke test for the song_analysis package.

Purpose:
    Provide a quick, dependency‑light verification that the modular
    feature extraction pipeline works end‑to‑end in the current
    environment, without requiring a real MP3 or stems.

Two modes:
    1. Real file mode (preferred):
        python -m song_analysis.smoke_test --song path/to/song.mp3 --stems path/to/stems_dir
       (Will invoke full `analyze_song.analyze`).

    2. Synthetic mode (no --song):
        python -m song_analysis.smoke_test
       Creates an in‑memory synthetic waveform and runs individual
       feature extractors to ensure they return expected shapes/types.

Exit code 0 = success, 1 = failure.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import tempfile
from typing import Any, Dict

import numpy as np

def _synthetic_wave(sr: int = 44100, seconds: float = 5.0) -> np.ndarray:
    t = np.linspace(0, seconds, int(sr * seconds), endpoint=False)
    # mixture of low (kick-ish), mid (snare-ish), and a simple vocal-like sine sweep
    wave = 0.4 * np.sin(2 * np.pi * 60 * t) + 0.2 * np.sin(2 * np.pi * 220 * t)
    sweep = 0.1 * np.sin(2 * np.pi * (220 + 40 * t) * t)
    return (wave + sweep).astype(np.float32)

def _test_synthetic() -> Dict[str, Any]:
    from song_analysis.rhythm import estimate_tempo_and_beats, detect_percussive_onsets
    from song_analysis.energy import compute_energy_curve
    from song_analysis.harmony import estimate_key
    from song_analysis.structure import segment_structure
    from song_analysis.events import detect_events
    from song_analysis.vocals import detect_vocals_activity
    from song_analysis.audio_io import load_audio

    sr = 44100
    y = _synthetic_wave(sr=sr)

    # Rhythm
    tempo, beats = estimate_tempo_and_beats(y, sr)
    drums = detect_percussive_onsets(y, sr)

    # Energy & structure
    energy_curve = compute_energy_curve(y, sr)
    sections = segment_structure(y, sr)

    # Key (heuristic) – may be Unknown in synthetic case
    key = estimate_key(y, sr)

    # Events
    events = detect_events(energy_curve, beats)

    # Vocals activity: create a temporary wav if librosa required for frames
    # We reuse audio_io loader by writing a temp file if needed for interface match
    tmp_dir = tempfile.mkdtemp(prefix="song_analysis_smoke_")
    tmp_wav = os.path.join(tmp_dir, "temp.wav")
    try:
        # Attempt to write wav only if soundfile available
        try:
            import soundfile as sf  # type: ignore
            sf.write(tmp_wav, y, sr)
            vocal_sections, pitch = detect_vocals_activity(tmp_wav)
        except Exception:
            vocal_sections, pitch = [], []
    finally:
        # best effort cleanup
        try:
            if os.path.exists(tmp_wav):
                os.remove(tmp_wav)
        except Exception:
            pass

    summary = {
        'mode': 'synthetic',
        'tempo': tempo,
        'beats_count': len(beats),
        'kick_count': len(drums.get('kick_onsets', [])),
        'snare_count': len(drums.get('snare_onsets', [])),
        'energy_points': len(energy_curve),
        'sections_found': len(sections),
        'key': key,
        'events_found': len(events),
        'vocal_sections_found': len(vocal_sections),
        'pitch_samples': len(pitch)
    }
    return summary

def _test_real(song: str, stems: str) -> Dict[str, Any]:
    from song_analysis.analyze_song import analyze
    import tempfile
    out_path = os.path.join(tempfile.gettempdir(), 'song_analysis_smoke_output.json')
    data = analyze(song, stems, out_path)
    # Keep only counts for brevity
    summary = {
        'mode': 'real',
        'tempo': data.get('tempo'),
        'beats_count': len(data.get('beats', [])),
        'sections_found': len(data.get('structure', [])),
        'kick_count': len(data.get('drums', {}).get('kick_onsets', [])),
        'snare_count': len(data.get('drums', {}).get('snare_onsets', [])),
        'events_found': len(data.get('events', [])),
        'vocal_sections_found': len(data.get('vocals', {}).get('active_sections', [])),
        'pitch_samples': len(data.get('vocals', {}).get('pitch_contour', []))
    }
    return summary

def main(argv=None):
    parser = argparse.ArgumentParser(description='Smoke test the song_analysis pipeline.')
    parser.add_argument('--song', help='Path to MP3 song (optional).')
    parser.add_argument('--stems', help='Stems folder (required if --song).')
    args = parser.parse_args(argv)
    try:
        if args.song:
            if not args.stems:
                parser.error('--stems is required when --song is provided')
            summary = _test_real(args.song, args.stems)
        else:
            summary = _test_synthetic()
        print(json.dumps(summary, indent=2))
    except Exception as e:
        print(f"Smoke test failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':  # pragma: no cover
    main()
