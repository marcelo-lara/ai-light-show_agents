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
    from song_analysis.spectral import analyze_spectral_emotion  # type: ignore
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
    spectral_emotion = funcs['analyze_spectral_emotion'](y, sr, [s.to_dict() for s in sections])
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
        'events': [e.to_dict() for e in events],
        'spectral_emotion': spectral_emotion
    }
    with open(out_path, 'w') as f:
        json.dump(data, f, indent=2)
    return data

if __name__ == '__main__':  # pragma: no cover
    base_folder = "/home/darkangel/ai-light-show_agents"

    # list of available songs
    songs_folder = os.path.join(base_folder, "songs")
    available_songs = [f[:-4] for f in os.listdir(songs_folder) if f.endswith('.mp3')]
    for song in available_songs:
        mp3_path = os.path.join(songs_folder, f"{song}.mp3")
        stems_folder = os.path.join(base_folder, "stems")
        out_path = os.path.join(base_folder, "data", f"{song}.analysis.json")
        print(f"\n## {song}: {mp3_path}")
        analyze(
                mp3_path=mp3_path,
                stems_folder=stems_folder,
                out_path=out_path
            )

    # result = analyze(
    #     mp3_path=mp3_path,
    #     stems_folder=os.path.join(base_folder, "stems"),
    #     out_path=os.path.join(base_folder, "data/born_slippy.analysis.json")
    # )
    # print(json.dumps(result['events'], indent=2)[:2000])
