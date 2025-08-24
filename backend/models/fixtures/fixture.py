from __future__ import annotations
from typing import Any, Dict, List
from .meta.meta import Meta
from .meta.position import Position
from .meta.action import Action
from .meta.action_parameter import ActionParameter

class Fixture:
    def __init__(self, id: str, name: str, fixture_type: str, channels: Dict[str, int], arm: Dict[str, Any], meta: Meta, position: Position, actions: List[Action] = []):
        self._id = id
        self._name = name
        self._type = fixture_type
        self._channels = channels
        self._arm = arm
        self._meta = meta
        self._position = position
        self._actions = actions

        # Global actions
        self._actions.append(
            Action(name="set_channel", handler=self.set_channel, description="Set the channel value over the specified time range.", parameters=[
                ActionParameter(name="start_time", type=float, description="Time when the channel value will be set"),
                ActionParameter(name="duration", type=float, description="Hold the value for the specified duration (default: remain until the end)", optional=True),
                ActionParameter(name="channel", type=List[str], description="List of channel names to set"),
                ActionParameter(name="value", type=float, description="Value to set the channel to (0.0 - 1.0)"),
            ], hidden=False))
        self._actions.append(
            Action(name="fade_channel", handler=self.fade_channel, description="Fade the channel value from start_value to end_value over the specified time range.", parameters=[
                ActionParameter(name="start_time", type=float, description="Start time for the fade, channels value will be set to start_value"),
                ActionParameter(name="duration", type=float, description="Duration of the fade to get to the end value"),
                ActionParameter(name="channel", type=List[str], description="List of channel names to fade ('red', 'green', 'blue', 'white')"),
                ActionParameter(name="start_value", type=float, description="Starting value for the fade (0.0 - 1.0)"),
                ActionParameter(name="end_value", type=float, description="Ending value for the fade (0.0 - 1.0)"),
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

    def set_arm(self, arm_state: bool = True):
        '''Prepare the fixture to emit light.'''
        if arm_state:
            for arm_channel, arm_value in self._arm.items():
                self.set_channel([arm_channel], explicit_value=arm_value if arm_value else 0)

    def set_channel(self, channel: List[str], value: float = 0, start_time: float = 0, duration: float = 0, explicit_value: int = -1):
        '''
        Set the value of a channel during the specified time range.
        Args:
            channel: List of channel names to set.
            value: Value to set the channel to (0.0 - 1.0).
            start_time: Time when the channel value will be set OR beginning of the song.
            duration: Duration to hold the value (default: remain until the end of the song).
        '''
        from ..dmx.dmx_canvas import DMXCanvas
        dmx_canvas:DMXCanvas = DMXCanvas()
        channel_numbers = [self.channels[c] for c in channel]
        if explicit_value >= 0:
            value_int = explicit_value
        else:
            value_int = int(value * 255)

        def set_value(frame_time: float):
            for channel_number in channel_numbers:
                dmx_canvas.set_frame_value(frame_time, channel_number, value_int)

        dmx_canvas.render(set_value, start_time=start_time, duration=duration)


    def fade_channel(self, channel: List[str], start_value: float = 1.0, end_value: float = 0.0, start_time: float = 0, duration: float = 0):
        '''Fade the value of a channel from start_value to end_value over the specified time range.'''
        from ..dmx.dmx_canvas import DMXCanvas
        dmx_canvas:DMXCanvas = DMXCanvas()

        channel_numbers = [self.channels[c] for c in channel]
        
        start_value_int = int(start_value * 255)
        end_value_int = int(end_value * 255)

        def fade_value(frame_time: float, progress: float):
            for channel_number in channel_numbers:
                value = int(start_value_int + (end_value_int - start_value_int) * progress)
                dmx_canvas.set_frame_value(frame_time, channel_number, value)

        dmx_canvas.render(fade_value, start_time=start_time, duration=duration)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id='{self._id}', name='{self._name}')"
