from __future__ import annotations
from typing import Any, Dict, List
from .meta import Meta
from .position import Position
from .action import Action
from .action_parameter import ActionParameter

class Fixture:
    def __init__(self, id: str, name: str, fixture_type: str, channels: Dict[str, int], arm: Dict[str, Any], meta: Meta, position: Position):
        self._id = id
        self._name = name
        self._type = fixture_type
        self._channels = channels
        self._arm = arm
        self._meta = meta
        self._position = position
        self._actions: List[Action] = []

        # Global actions
        self._actions.append(
            Action(name="set_channel", handler=self.set_channel, description="Set the channel value", parameters=[
                ActionParameter(name="channel", value=List[str], description="List of channel names to set"),
                ActionParameter(name="value", value=float, description="Value to set the channel to"),
                ActionParameter(name="start_time", value=float, description="Start time for the action"),
                ActionParameter(name="end_time", value=float, description="End time for the action"),
            ], hidden=False))
        self._actions.append(
            Action(name="fade_channel", handler=self.fade_channel, description="Fade the channel value", parameters=[
                ActionParameter(name="channel", value=List[str], description="List of channel names to fade"),
                ActionParameter(name="start_value", value=float, description="Starting value for the fade (0.0 - 1.0)"),
                ActionParameter(name="end_value", value=float, description="Ending value for the fade (0.0 - 1.0)"),
                ActionParameter(name="start_time", value=float, description="Start time for the fade"),
                ActionParameter(name="end_time", value=float, description="End time for the fade")
        ], hidden=False))

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
        '''DMX Channels available on this fixture (name, channel number)'''
        return self._channels

    @property
    def arm(self) -> Dict[str, int]:
        '''Channels must be set to this value to enable light output.'''
        return self._arm

    @property
    def meta(self) -> Meta:
        return self._meta

    @property
    def position(self) -> Position:
        '''XY Location of the fixture within the stage'''
        return self._position

    @property
    def actions(self) -> List[Action]:
        '''Software effects that this fixture can render in dmx-canvas'''
        return self._actions

    def set_channel(self, channel: List[str], value: float, start_time: float = 0, end_time: float = 0):
        '''Set the value of a channel during the specified time range.'''
        pass

    def fade_channel(self, channel: List[str], start_value: float = 1.0, end_value: float = 0.0, start_time: float = 0, end_time: float = 0):
        '''Fade the value of a channel from start_value to end_value over the specified time range.'''
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id='{self._id}', name='{self._name}')"
