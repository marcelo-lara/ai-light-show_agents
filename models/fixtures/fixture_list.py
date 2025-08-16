from __future__ import annotations
import json
from typing import List
from .fixture import Fixture
from .moving_head import MovingHead
from .par_can import RgbParCan
from .position import Position
from .meta import Meta
from .position_constraints import PositionConstraints
from .constraint import Constraint

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

    def __iter__(self):
        return iter(self._fixtures)