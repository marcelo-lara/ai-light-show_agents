import os
from typing import List, Optional
from pathlib import Path

from models.fixtures.fixture_list import FixtureList
from models.lighting.plan import Plan
from models.song.song import Song

class AppData:

    def __init__(self, base_folder: Optional[str] = None):

        # determine base folder
        if not base_folder:
            self._base_folder = Path(os.path.abspath(__file__)).parent.parent
        else:
            if not Path(base_folder).exists():
                raise ValueError(f"Base folder '{base_folder}' does not exist")
        if not self._base_folder:
            raise ValueError("Base folder could not be determined")
        
        # setup folders
        self._data_folder = os.path.join(self._base_folder, "data")
        self._mp3_folder = os.path.join(self._base_folder, "songs")
        self._logs_folder = os.path.join(self._base_folder, "logs")
        self._fixtures_file = os.path.join(self._base_folder, "fixtures", "fixtures.json")

        # load fixtures
        self._fixtures = FixtureList(self._fixtures_file)
        self._plan = Plan(data_folder=str(self._data_folder))

    def load_song(self, song_name: str):
        self._song = Song(song_name, base_folder=str(self._base_folder))
        self._plan.load_plan(song_name=song_name)

    @property
    def base_folder(self) -> Path:
        return self._base_folder

    @property
    def fixtures(self) -> FixtureList:
        return self._fixtures

    @property
    def song(self) -> Song:
        return self._song

    @property
    def song_name(self) -> str:
        return self._song.name

    @property
    def plan(self) -> Plan:
        return self._plan