from dataclasses import dataclass, field
from typing import List, Optional
import os

from .beat import Beat
from .chord import Chord
from .key_moment import KeyMoment
from .section import Section
import json

class Song:
    def __init__(self, name: str, base_folder: str):
        self._name: str = name
        self._genre: Optional[str] = None
        self._duration: Optional[float] = None
        self._bpm: Optional[float] = None
        self._mp3_file: Optional[str] = None
        self._sections: List[Section] = []
        self._key_moments: List[KeyMoment] = []
        self._chords: List[Chord] = []
        self._beats: List[Beat] = []
        self.base_folder = base_folder

        # check if base folder exists
        if not os.path.exists(self.base_folder):
            raise ValueError(f"Base folder '{self.base_folder}' does not exist")

        # set data folder
        self._data_folder = os.path.join(self.base_folder, "data")

        # load basic metadata
        meta_file = os.path.join(self._data_folder, f"{self._name}.meta.json")
        if os.path.exists(meta_file):
            with open(meta_file, "r") as f:
                meta_data = json.load(f)
                self._genre = meta_data.get("genre")
                self._duration = meta_data.get("duration")
                self._bpm = meta_data.get("bpm")
                self._sections = [Section(**sec) for sec in meta_data.get("sections", [])]
                self._key_moments = [KeyMoment(**km) for km in meta_data.get("key_moments", [])]
        else:
            # create an empty metadata file
            with open(meta_file, "w") as f:
                json.dump({}, f)

    @property
    def name(self) -> str:
        return self._name

    @property
    def genre(self) -> Optional[str]:
        return self._genre

    @property
    def duration(self) -> Optional[float]:
        return self._duration

    @property
    def bpm(self) -> Optional[float]:
        return self._bpm

    @property
    def mp3_file(self) -> Optional[str]:
        return self._mp3_file

    @property
    def sections(self) -> List[Section]:
        return self._sections

    @property
    def key_moments(self) -> List[KeyMoment]:
        return self._key_moments

    @property
    def chords(self) -> List[Chord]:
        return self._chords

    @property
    def beats(self) -> List[Beat]:
        return self._beats

