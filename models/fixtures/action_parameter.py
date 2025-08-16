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

    def __repr__(self) -> str:
        return f"ActionParameter(name={self.name}, value={self.value}, description={self.description})"
