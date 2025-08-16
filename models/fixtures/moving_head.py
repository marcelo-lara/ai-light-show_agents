from __future__ import annotations
from typing import Any, Dict
from .fixture import Fixture
from .meta import Meta
from .position import Position

class MovingHead(Fixture):
    def __init__(self, id: str, name: str, fixture_type: str, channels: Dict[str, int], arm: Dict[str, Any], meta: Meta, position: Position):
        
        

        super().__init__(id, name, fixture_type, channels, arm, meta, position)
