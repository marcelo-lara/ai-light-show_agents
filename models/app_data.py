import os
from typing import List, Optional
from pathlib import Path

from models.fixtures.fixture_list import FixtureList

class AppData:

    def __init__(self, base_folder: Optional[str] = None):

        # determine base folder
        if not base_folder:
            self.base_folder = Path(os.path.abspath(__file__)).parent.parent
        else:
            if not Path(base_folder).exists():
                raise ValueError(f"Base folder '{base_folder}' does not exist")
        if not self.base_folder:
            raise ValueError("Base folder could not be determined")
        
        print(f"Using base folder: {self.base_folder}")

        # setup folders
        self._data_folder = os.path.join(self.base_folder, "data")
        self._mp3_folder = os.path.join(self.base_folder, "songs")
        self._logs_folder = os.path.join(self.base_folder, "logs")
        self._fixtures_file = os.path.join(self.base_folder, "fixtures", "fixtures.json")

        # load fixtures
        self._fixtures = FixtureList(self._fixtures_file)


    @property
    def fixtures(self) -> FixtureList:
        return self._fixtures
