import os
from typing import List, Optional

class AppData:

    def __init__(self, base_folder: Optional[str] = None):
        self.base_folder = base_folder

        if not self.base_folder:
            raise ValueError("Base folder could not be determined")

        # setup folders
        self._data_folder = os.path.join(self.base_folder, "data")
        self._mp3_folder = os.path.join(self.base_folder, "songs")
        self._logs_folder = os.path.join(self.base_folder, "logs")
        self._fixtures_folder = os.path.join(self.base_folder, "fixtures")

        # load fixtures

