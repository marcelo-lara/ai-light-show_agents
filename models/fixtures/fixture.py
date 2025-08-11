from __future__ import annotations
from typing import Any, Dict, List
from .meta import Meta
from .position import Position
from .action_model import ActionModel

class Fixture:
    def __init__(self, id: str, name: str, fixture_type: str, channels: Dict[str, int], arm: Dict[str, Any], meta: Meta, position: Position):
        self._id = id
        self._name = name
        self._type = fixture_type
        self._channels = channels
        self._arm = arm
        self._meta = meta
        self._position = position
        self._actions: List[ActionModel] = []

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def channels(self) -> Dict[str, int]:
        return self._channels

    @property
    def arm(self) -> Dict[str, Any]:
        return self._arm

    @property
    def meta(self) -> Meta:
        return self._meta

    @property
    def position(self) -> Position:
        return self._position

    @property
    def actions(self) -> List[ActionModel]:
        return self._actions

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id='{self._id}', name='{self._name}')"
