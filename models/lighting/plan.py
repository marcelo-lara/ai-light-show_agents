from dataclasses import dataclass
import os


@dataclass
class PlanEntry:
    id: int
    start: float
    end: float
    name: str
    description: str

class Plan:
    def __init__(self, data_folder: str):
        self.plans = []
        self._data_folder = data_folder

    def load_plan(self, song_name: str):
        """Load plans from data folder (e.g., data/born_slippy.plan.json) or create an empty one."""
        import json
        plan_path = os.path.join(self._data_folder, f"{song_name}.plan.json")
        self.plans = []
        if os.path.exists(plan_path):
            with open(plan_path, 'r') as f:
                try:
                    data = json.load(f)
                    for entry in data:
                        self.plans.append(PlanEntry(**entry))
                except Exception as e:
                    print(f"Failed to load plan: {e}")


    def save_plan(self, song_name: str):
        """Save plan to data folder (e.g., data/born_slippy.plan.json)."""
        import json
        plan_path = os.path.join(self._data_folder, f"{song_name}.plan.json")
        os.makedirs(self._data_folder, exist_ok=True)
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
