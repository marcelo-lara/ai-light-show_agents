from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class ActionParameter:
    name: str
    value: Any
    description: str
    def __str__(self) -> str:
        return f"{self.name}: {self.value} | {self.description})"
