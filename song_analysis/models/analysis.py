import os
from pathlib import Path
import numpy as np
import pandas as pd

class Analysis:
    """Singleton context object for song analysis.

    Uses a class-level _instance and guards __init__ so initialization runs once.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # avoid re-running initialization on subsequent constructions
        if getattr(self, "_initialized", False):
            return

        # determine base folder - go up two levels from backend/models to get to project root
        self._base_folder = Path(os.path.abspath(__file__)).parent.parent.parent
        self._song_name = ''
        self._initialized = True
        self._stems_files = {}
        self._dataframe = None

    def load_dataframe(self):
        if self._dataframe is not None:
            return self._dataframe

        if self._song_name == '':
            raise ValueError("song_name must be set before loading dataframe.")

        # Load the DataFrame from a CSV file or other source
        self._dataframe = pd.read_pickle(self.data_folder / f"{self._song_name}.pkl")
        return self._dataframe
    
    def save_dataframe(self):
        if self._song_name == '':
            raise ValueError("song_name must be set before loading dataframe.")
        
        if self._dataframe is None:
            raise ValueError("DataFrame is not loaded.")

        # Save the DataFrame to a CSV file or other destination
        self._dataframe.to_pickle(self.data_folder / f"{self._song_name}.pkl")

    @property
    def song_name(self):
        return self._song_name

    @song_name.setter
    def song_name(self, song_name):
        self._song_name = song_name

    @property
    def stems_files(self):
        return self._stems_files

    @stems_files.setter
    def stems_files(self, stems_files):
        self._stems_files = stems_files

    @property
    def base_folder(self):
        return self._base_folder

    @property
    def data_folder(self):
        return Path(self._base_folder) / "data"

    @property
    def stems_folder(self):
        return Path(self._base_folder) / "stems"