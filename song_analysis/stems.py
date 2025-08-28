"""Stem management & (optional) Spleeter separation."""
from __future__ import annotations
import os
from typing import List

try:
    from spleeter.separator import Separator  # type: ignore
except ImportError:  # pragma: no cover
    Separator = None  # type: ignore

AUTO_SPLIT_ENABLED = True
STEMS_MODEL = '4stems'

def ensure_stems(song_path: str, stems_folder: str, required: List[str] | None = None) -> None:
    """Generate required stems if missing.

    Args:
        song_path: Original mixed audio file path.
        stems_folder: Destination folder containing (or to contain) stems.
        required: Filenames we need to exist (defaults minimal set).
    Notes:
        - Silent no-op if splitting disabled or Spleeter missing.
        - Stems exported directly into stems_folder.
    """
    if required is None:
        required = ['vocals.wav', 'drums.wav']
    os.makedirs(stems_folder, exist_ok=True)
    missing = [f for f in required if not os.path.exists(os.path.join(stems_folder, f))]
    if not missing or not AUTO_SPLIT_ENABLED or Separator is None:
        return
    model = 'spleeter:' + ('4stems' if STEMS_MODEL == '4stems' else '2stems')
    try:
        separator = Separator(model)
        separator.separate_to_file(song_path, stems_folder, filename_format='{filename}/{instrument}.wav')
        base = os.path.splitext(os.path.basename(song_path))[0]
        produced_dir = os.path.join(stems_folder, base)
        if os.path.isdir(produced_dir):
            mapping = {
                '4stems': {
                    'vocals.wav': 'vocals.wav',
                    'drums.wav': 'drums.wav',
                    'bass.wav': 'bass.wav',
                    'other.wav': 'other.wav'
                },
                '2stems': {
                    'vocals.wav': 'vocals.wav',
                    'other.wav': 'accompaniment.wav'
                }
            }[STEMS_MODEL]
            for target, source in mapping.items():
                src = os.path.join(produced_dir, source)
                dst = os.path.join(stems_folder, target)
                if os.path.exists(src):
                    try:
                        if os.path.exists(dst):
                            os.remove(dst)
                        os.replace(src, dst)
                    except Exception:  # pragma: no cover
                        pass
            try:
                if not os.listdir(produced_dir):
                    os.rmdir(produced_dir)
            except Exception:  # pragma: no cover
                pass
    except Exception:  # pragma: no cover
        return
