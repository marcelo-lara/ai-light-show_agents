from __future__ import annotations

class Position:
    def __init__(self, x: float, y: float, z: float, label: str):
        self.x = x
        self.y = y
        self.z = z
        self.label = label

    def __repr__(self) -> str:
        return f"Position(x={self.x}, y={self.y}, z={self.z}, label='{self.label}')"
