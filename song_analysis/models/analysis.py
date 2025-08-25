import os
from pathlib import Path

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
        self._initialized = True
        self._stems_files = {}

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