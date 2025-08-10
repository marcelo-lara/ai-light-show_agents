from dataclasses import dataclass, field
from typing import List, Optional
import os

from .beat import Beat
from .chord import Chord
from .key_moment import KeyMoment
from .section import Section

class Song:
    name: str
    genre: str
    duration: float
    bpm: float
    mp3_file: str
    sections: List[Section] = []
    key_moments: List[KeyMoment] = []
    chords: List[Chord] = []
    beats: List[Beat] = []

    def __init__(self, name: str, base_folder: Optional[str] = None):
        self.name = name
        self.base_folder = base_folder

        # check if base folder exists
        if not base_folder:
            self.base_folder = os.path.join(os.getcwd())
        
        if base_folder and not os.path.exists(base_folder):
            raise ValueError(f"Base folder '{base_folder}' does not exist")

        if not self.base_folder:
            raise ValueError("Base could not be determined")

    def _load_meta(self):
        # load metadata from files in the data folder(or create an empty one)
        pass

