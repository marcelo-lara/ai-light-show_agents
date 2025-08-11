from __future__ import annotations
from typing import Any, Dict, List
from .meta import Meta
from .position import Position
from .action_model import ActionModel

class Fixture:
    def __init__(self, id: str, name: str, fixture_type: str, channels: Dict[str, int], arm: Dict[str, Any], meta: Meta, position: Position):
        self.id = id
        self.name = name
        self.type = fixture_type
        self.channels = channels
        self.arm = arm
        self.meta = meta
        self.position = position
        self.actions: List[ActionModel] = []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id='{self.id}', name='{self.name}')"
