from __future__ import annotations

class Constraint:
    def __init__(self, min: int, max: int):
        self.min = min
        self.max = max

    def __repr__(self) -> str:
        return f"Constraint(min={self.min}, max={self.max})"
