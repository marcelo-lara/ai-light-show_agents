from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class ActionParameter:
    name: str
    type: Any
    description: str
    optional: bool = False
    def __str__(self) -> str:
        return f"{'(optional)' if self.optional else ''} {self.name}: {self.type} | {self.description}"

    def __repr__(self) -> str:
        return f"ActionParameter(name={self.name}, value={self.type}, description={self.description}, optional={self.optional})"
