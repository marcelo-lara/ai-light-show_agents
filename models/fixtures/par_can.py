from __future__ import annotations
from typing import Any, Dict, List

from models.fixtures.meta.action import Action
from models.fixtures.meta.action_parameter import ActionParameter
from .fixture import Fixture
from .meta.meta import Meta
from .meta.position import Position

class RgbParCan(Fixture):
    def __init__(self, id: str, name: str, fixture_type: str, channels: Dict[str, int], arm: Dict[str, Any], meta: Meta, position: Position):


        self._actions = []
        self._actions.append(
            Action(
                name="flash", 
                handler=self.handle_flash, 
                description="Flash effect with a post fade+out effect.", 
                parameters=[
                    ActionParameter(name="start_time", type=float, description="Time when the flash effect is fired"),
                    ActionParameter(name="duration", type=List[str], description="Fade out duration (default 1 beat)", optional=True),
                    ActionParameter(name="initial_value", type=float, description="Initial brightness value (default Max = 1.0)", optional=True),
                    ActionParameter(name="channels", type=float, description="list of channels to flash (default: 'white')", optional=True),
            ], hidden=False))

        super().__init__(id, name, fixture_type, channels, arm, meta, position, actions=self._actions)

    def handle_flash(self, start_time: float, duration: float = 0.5, initial_value: float = 1.0, end_value: float = 0.0, channels: List[str] = ['white']):
        """
        Render the flash action for the RGB Par Can fixture.
        """
        
        # If no channels are specified, default to all three RGB channels
        if channels == ['white'] or channels == ['rgb']:
            channels = ['red', 'green', 'blue']

        self.fade_channel(
            channel=channels,
            start_value=initial_value,
            end_value=end_value,
            start_time=start_time,
            duration=duration
        )