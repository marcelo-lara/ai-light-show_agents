from __future__ import annotations
from typing import List
from .fixture import Fixture

class FixtureList:
    def __init__(self, ):
        pass

    def load_fixtures(self, fixtures_file: str):
        #load fixtures from json file
        pass

    @property
    def fixtures(self) -> List[Fixture]:
        return self.fixtures

    def __iter__(self):
        return iter(self.fixtures)
