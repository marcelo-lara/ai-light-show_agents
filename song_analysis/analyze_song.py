from __future__ import annotations
import argparse
import json
import os
import sys
from typing import Dict, Any

def _import_funcs():
    # Absolute imports assuming package installed / run from project root
    from song_analysis.audio_io import load_audio  # type: ignore
    from song_analysis.stems import ensure_stems  # type: ignore
    from song_analysis.rhythm import estimate_tempo_and_beats, detect_percussive_onsets  # type: ignore
    from song_analysis.harmony import estimate_key  # type: ignore
    from song_analysis.vocals import detect_vocals_activity  # type: ignore
    from song_analysis.energy import compute_energy_curve  # type: ignore
    from song_analysis.structure import segment_structure  # type: ignore
    from song_analysis.events import detect_events  # type: ignore
    from song_analysis.schema import SectionEntry, EventEntry  # type: ignore
    return locals()

def analyze(mp3_path: str, stems_folder: str, out_path: str) -> Dict[str, Any]:
    funcs = _import_funcs()
    funcs['ensure_stems'](mp3_path, stems_folder)
    y, sr = funcs['load_audio'](mp3_path)
    tempo, beats = funcs['estimate_tempo_and_beats'](y, sr)
    key = funcs['estimate_key'](y, sr)
    energy_curve = funcs['compute_energy_curve'](y, sr)
    sections = funcs['segment_structure'](y, sr)
    drums_info = funcs['detect_percussive_onsets'](y, sr, os.path.join(stems_folder, 'drums.wav'))
    vocal_sections, pitch_contour = funcs['detect_vocals_activity'](os.path.join(stems_folder, 'vocals.wav'))
    events = funcs['detect_events'](energy_curve, beats, sr)
    data: Dict[str, Any] = {
        'tempo': round(tempo) if tempo else 0,
        'key': key,
        'structure': [s.to_dict() for s in sections],
        'beats': beats,
        'drums': drums_info,
        'vocals': {
            'active_sections': vocal_sections,
            'pitch_contour': pitch_contour
        },
        'energy_curve': energy_curve,
        'events': [e.to_dict() for e in events]
    }
    with open(out_path, 'w') as f:
        json.dump(data, f, indent=2)
    return data

def main(argv=None):
    parser = argparse.ArgumentParser(description='Analyze song and extract features for light show generation.')
    parser.add_argument('--song', required=True)
    parser.add_argument('--stems', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--no-split', action='store_true')
    parser.add_argument('--stems-model', choices=['2stems','4stems'], default='4stems')
    args = parser.parse_args(argv)
    # Configure stems flags
    from song_analysis import stems as _stems_mod  # type: ignore
    _stems_mod.AUTO_SPLIT_ENABLED = not args.no_split
    _stems_mod.STEMS_MODEL = args.stems_model
    result = analyze(args.song, args.stems, args.out)
    print(json.dumps(result, indent=2)[:2000])

if __name__ == '__main__':  # pragma: no cover
    result = analyze(
        mp3_path="/home/darkangel/ai-light-show_agents/songs/born_slippy.mp3",
        stems_folder="/home/darkangel/ai-light-show_agents/stems",
        out_path="/home/darkangel/ai-light-show_agents/data/born_slippy.analysis.json"
    )
    print(json.dumps(result['events'], indent=2)[:2000])
