from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List
from .action_parameter import ActionParameter

@dataclass
class Action:
    name: str
    handler: Any #callable
    description: str
    parameters: list[ActionParameter]
    hidden: bool
    def __str__(self) -> str:
        return f"{self.name} | {self.description}"
