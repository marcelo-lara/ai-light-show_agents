from __future__ import annotations
from typing import Dict, Optional
from .position_constraints import PositionConstraints

class Meta:
    def __init__(self, channel_types: Dict[str, str], value_mappings: Optional[Dict[str, Dict[str, str]]] = None, position_constraints: Optional[PositionConstraints] = None):
        self.channel_types = channel_types
        self.value_mappings = value_mappings
        self.position_constraints = position_constraints

    def __repr__(self) -> str:
        return f"Meta(channel_types={self.channel_types}, value_mappings={self.value_mappings}, position_constraints={self.position_constraints})"
