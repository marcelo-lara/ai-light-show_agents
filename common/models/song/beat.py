from dataclasses import dataclass


@dataclass
class Beat:
    time: float
    volume: float
    energy: float
