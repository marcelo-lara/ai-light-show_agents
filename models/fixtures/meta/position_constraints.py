from __future__ import annotations
from .constraint import Constraint

class PositionConstraints:
    def __init__(self, pan: Constraint, tilt: Constraint):
        self.pan = pan
        self.tilt = tilt

    def __repr__(self) -> str:
        return f"PositionConstraints(pan={self.pan}, tilt={self.tilt})"
