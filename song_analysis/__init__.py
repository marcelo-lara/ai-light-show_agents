"""Song analysis package.

Provides modular feature extraction to build an LLM‑ready JSON summary
for driving automated lighting design. See `analyze_song.py` for the
CLI entrypoint and `README.md` for schema details.
"""

from . import audio_io, rhythm, harmony, vocals, energy, structure, events, stems, schema  # noqa: F401

__all__ = ['audio_io', 'rhythm', 'harmony', 'vocals', 'energy', 'structure', 'events', 'stems', 'schema']
