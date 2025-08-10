from dataclasses import dataclass


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

    def load_plan(self, song_name: str):
        # Load plans from data folder (e.g., data/born_slippy.plan.json)
        # or create an empty one
        pass

    def save_plan(self, song_name: str):
        # Save plan to data folder (e.g., data/born_slippy.plan.json)
        pass

    def add_plan(self, plan: PlanEntry):
        self.plans.append(plan)

    def remove_plan(self, plan: PlanEntry):
        self.plans.remove(plan)

    def get_plans(self):
        return self.plans
