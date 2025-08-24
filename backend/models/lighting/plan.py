from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class PlanEntry:
    id: int
    start: float
    end: float
    name: str
    description: str

class Plan:
    def __init__(self):
        self.plans = []
        from ..app_data import AppData
        self._data_folder = AppData().data_folder
        self._plan_file = ''

    def _actions_file(self) -> str: 
        """Return the path to the actions file."""
        from ..app_data import AppData
        return str(Path(self._data_folder) / f"{AppData().song_name}.plan.json")

    def load_plan(self):
        """Load plans from data folder (e.g., data/born_slippy.plan.json) or create an empty one."""
        plan_path = self._actions_file()
        if not Path(plan_path).exists():
            self.plans = []
            return
        with open(plan_path, 'r') as f:
            try:
                data = json.load(f)
                self.plans = [PlanEntry(**entry) for entry in data]
            except Exception as e:
                print(f"Failed to load plan: {e}")

    def save_plan(self):
        """Save plan to data folder (e.g., data/born_slippy.plan.json)."""
        plan_path = self._actions_file()
        with open(plan_path, 'w') as f:
            json.dump([entry.__dict__ for entry in self.plans], f, indent=2)

    def add_plan(self, plan: PlanEntry):
        """Add a PlanEntry to the list of plans."""
        self.plans.append(plan)

    def remove_plan(self, plan: PlanEntry):
        """Remove a PlanEntry from the list of plans."""
        self.plans.remove(plan)

    def get_plans(self):
        """Return the list of all PlanEntry objects."""
        return self.plans

    def __iter__(self):
        """Iterate over the PlanEntry objects."""
        return iter(self.plans)
    
    def __getitem__(self, index):
        """Get a PlanEntry by index."""
        return self.plans[index]
