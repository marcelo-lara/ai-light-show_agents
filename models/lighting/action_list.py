"""Helpers for representing and persisting lighting actions/effects.

This module defines two small convenience types used by the lighting
planner and DMX rendering code:

- ActionEntry: a simple data container describing an effect for a single
  fixture at a given start time and duration.
- ActionList: an in-memory ordered collection of ActionEntry objects with
  helpers to load/save from disk (per-song JSON) and to clear ranges.

Files are persisted as JSON lists of objects matching ActionEntry.__dict__.
By default files are stored under the AppData.data_folder with the name
"{song_name}.actions.json". The module is intentionally small and has no
external dependencies beyond the repo's AppData helper.

Example:
    from models.lighting.commands import ActionEntry, ActionList
    al = ActionList()
    al.add_action(ActionEntry(1.0, 0.5, "fixture_1", {"intensity": 255}))
    al.save()
"""

from typing import Any
import json
from pathlib import Path


class ActionEntry:
    """Represents a single lighting action/effect for a fixture.
    This Action must be rendered using the fixture action handler.

    Attributes
    ----------
    start_time : float
        Time in seconds when the action starts.
    duration : float
        Duration in seconds for the action.
    fixture_id : str
        Identifier for the target fixture (matches entries in the
        fixture list used elsewhere in the application).
    parameters : dict[str, Any]
        Arbitrary key/value parameters that describe the action. Typical
        keys include things like 'intensity', 'color', 'pan', 'tilt', etc.

    Notes
    -----
    This is a plain data container used by the planner and renderer. It
    intentionally exposes attributes directly to make JSON serialization
    straightforward (ActionList.save uses entry.__dict__).
    """

    def __init__(self, start_time: float, action:str, duration: float, fixture_id: str, parameters: dict[str, Any]):
        """Initialize a new ActionEntry.

        Parameters
        ----------
        start_time:
            Start time in seconds.
        duration:
            Duration in seconds.
        fixture_id:
            Target fixture identifier.
        parameters:
            Dictionary of action-specific parameters.
        """
        self.start_time = start_time
        self.duration = duration
        self.action = action
        self.fixture_id = fixture_id
        self.parameters = parameters

    def __repr__(self) -> str:
        """Return a concise, readable representation for debugging."""
        return f"Action(start_time={self.start_time}, duration={self.duration}, fixture_id={self.fixture_id}, parameters={self.parameters})"


class ActionList:
    """Ordered collection of ActionEntry items with persistence helpers.

    The list maintains actions in memory (unsorted). Iteration and
    indexing return items sorted by their start time. Actions can be
    loaded from / saved to a per-song JSON file whose location is
    determined by AppData.song_name and AppData.data_folder unless a
    custom data_folder is provided to the constructor.

    Common usage
    ------------
    al = ActionList()
    al.add_action(ActionEntry(0.0, 1.0, 'f1', {'intensity': 1.0}))
    al.save()  # persists to {data_folder}/{song_name}.actions.json

    Edge cases
    ----------
    - Loading silently returns if the actions file doesn't exist.
    """

    def __init__(self, data_folder: str = ''):
        """Create a new ActionList.

        Parameters
        ----------
        data_folder : str, optional
            If provided, this folder is used for load/save. If empty,
            the value is taken from AppData().data_folder.
        """
        self.action_list: list[ActionEntry] = []
        self._data_folder = data_folder
        if self._data_folder == '':
            from models.app_data import AppData
            self._data_folder = AppData().data_folder

    def _actions_file(self) -> str:
        """Return the filesystem path for the current song's actions file.

        The filename is "{song_name}.actions.json" inside the configured
        data folder.
        """
        from models.app_data import AppData
        return str(Path(self._data_folder) / f"{AppData().song_name}.actions.json")

    def add_action(self, action: ActionEntry) -> None:
        """Append a new ActionEntry to the in-memory list.

        The list itself is not re-ordered on append; iteration and
        indexing provide a time-ordered view.
        """
        self.action_list.append(action)

    def clear_range(self, start_time: float, end_time: float) -> None:
        """Remove all actions that start within [start_time, end_time).

        Parameters
        ----------
        start_time, end_time : float
            Range of start times (end is exclusive).
        """
        self.action_list = [act for act in self.action_list if not (start_time <= act.start_time < end_time)]

    def clear_all(self) -> None:
        """Remove all actions from the list (in-memory only)."""
        self.action_list = []

    def load(self) -> None:
        """Load actions from the per-song JSON file into memory.

        If the file does not exist this function returns without error.
        On JSON parsing or IO errors a message is printed and loading
        stops.
        """
        actions_file = self._actions_file()
        if not Path(actions_file).exists():
            return
        self.clear_all()
        with open(actions_file, 'r') as f:
            try:
                data = json.load(f)
                for entry in data:
                    # Expect data items to match ActionEntry constructor
                    self.action_list.append(ActionEntry(**entry))
            except Exception as e:
                print(f"Failed to load actions: {e}")

    def save(self) -> None:
        """Persist current actions to the per-song JSON file.

        The file content is a JSON array where each object is the
        attribute dictionary of an ActionEntry instance.
        """
        actions_file = self._actions_file()
        with open(actions_file, 'w') as f:
            json.dump([entry.__dict__ for entry in self.action_list], f, indent=2)

    def render_to_dmxcanvas(self) -> None:
        """Render the action list to a DMX canvas (placeholder implementation)."""
        print("Rendering actions to DMX canvas (not implemented)")
        for action in sorted(self.action_list, key=lambda act: act.start_time):
            print(f"{action.start_time}: {action}")

    def __repr__(self) -> str:
        """Return a compact representation useful for debugging."""
        return f"ActionList(actions={self.action_list})"

    def __iter__(self):
        """Return an iterator over actions ordered by start time."""
        return iter(sorted(self.action_list, key=lambda act: act.start_time))

    def __getitem__(self, index):
        """Return the time-ordered action at the given index."""
        return sorted(self.action_list, key=lambda act: act.start_time)[index]
