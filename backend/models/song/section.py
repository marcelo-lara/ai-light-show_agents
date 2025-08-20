from dataclasses import dataclass


@dataclass
class Section:
    name: str
    start: float
    end: float
    prompt: str
