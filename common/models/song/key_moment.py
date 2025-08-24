from dataclasses import dataclass


@dataclass
class KeyMoment:
    start: float
    end: float
    name: str
    description: str
