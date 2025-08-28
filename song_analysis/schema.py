"""Data schema definitions for song analysis output.

These lightweight dataclasses define the structured elements
we emit in the final JSON. Keeping them here (instead of scattering
through functional modules) makes it easy for an LLM or a developer
to discover the canonical shapes.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class SectionEntry:
    """Represents a coarse musical section.

    Attributes:
        section: Human‑readable label (e.g. "intro", "verse").
        start: Start time in seconds.
        end: End time in seconds.
    """
    section: str
    start: float
    end: float

    def to_dict(self) -> Dict[str, Any]:  # convenience for JSON serialization
        return asdict(self)

@dataclass
class EventEntry:
    """Represents a macro musical / production event.

    Examples: drop, climax, breakdown.

    Attributes:
        type: Event label.
        time: Timestamp in seconds.
    """
    type: str
    time: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
