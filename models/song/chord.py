from dataclasses import dataclass
from typing import Optional


@dataclass
class Chord:
    bar_num: int
    beat_num: int
    time: float
    chord: str
    bass: Optional[str] = None
