from __future__ import annotations
import json
from typing import List

from models.lighting.action_list import ActionEntry
from .fixture import Fixture
from .moving_head import MovingHead
from .par_can import RgbParCan
from .meta.position import Position
from .meta.meta import Meta
from .meta.position_constraints import PositionConstraints
from .meta.constraint import Constraint

class FixtureList:
    def __init__(self, fixtures_file: str):
        self._fixtures: List[Fixture] = []
        self.load_fixtures(fixtures_file)

    def load_fixtures(self, fixtures_file: str):
        with open(fixtures_file, 'r') as f:
            fixtures_data = json.load(f)

        for fixture_data in fixtures_data:
            position_data = fixture_data['position']
            position = Position(**position_data)

            meta_data = fixture_data['meta']
            position_constraints_data = meta_data.get('position_constraints')
            position_constraints = None
            if position_constraints_data:
                pan_constraint_data = position_constraints_data['pan']
                tilt_constraint_data = position_constraints_data['tilt']
                pan_constraint = Constraint(**pan_constraint_data)
                tilt_constraint = Constraint(**tilt_constraint_data)
                position_constraints = PositionConstraints(pan=pan_constraint, tilt=tilt_constraint)

            meta = Meta(
                channel_types=meta_data['channel_types'],
                value_mappings=meta_data.get('value_mappings'),
                position_constraints=position_constraints
            )

            fixture_args = {
                'id': fixture_data['id'],
                'name': fixture_data['name'],
                'fixture_type': fixture_data['type'],
                'channels': fixture_data['channels'],
                'arm': fixture_data['arm'],
                'meta': meta,
                'position': position,
            }

            if fixture_data['type'] == 'moving_head':
                fixture = MovingHead(**fixture_args)
            elif fixture_data['type'] == 'rgb_parcan':
                fixture = RgbParCan(**fixture_args)
            else:
                continue

            self._fixtures.append(fixture)

    @property
    def fixtures(self) -> List[Fixture]:
        return self._fixtures

    def arm_all_fixtures(self):
        for fixture in self._fixtures:
            fixture.set_arm(True)

    def get_fixture_by_id(self, fixture_id: str) -> Fixture | None:
        return next((f for f in self._fixtures if f.id == fixture_id), None)

    def render_actions(self, action_list: List[ActionEntry]) -> bool:
        from ..app_data import AppData
        app_data = AppData()
        app_data.dmx_canvas.init_canvas()

        self.arm_all_fixtures()
        for action in action_list:
            fixture = self.get_fixture_by_id(action.fixture_id)
            if not fixture:
                print(f"❌ render_actions: Could not find fixture_id {action.fixture_id}")
                continue

            fixture_action = next((a for a in fixture.actions if a.name == action.action), None)
            if not fixture_action:
                print(f"❌ render_actions: Could not find action '{action.action}' on fixture {fixture.name}")
                continue

            _action_params = [a.name for a in fixture_action.parameters]

            _handler_params = {}
            for param in action.parameters.keys():
                if param in _action_params:
                    _handler_params[param] = action.parameters[param]
                    continue
                print(f"⚠️ render_actions: Could not find parameter '{param}' for action '{action.action}' on fixture {fixture.name}")

            fixture_action.handler(**_handler_params)

        return True

    def __iter__(self):
        return iter(self._fixtures)
    
    def __getitem__(self, index: int) -> Fixture:
        return self._fixtures[index]