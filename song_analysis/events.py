"""Derive macro musical events (drop, climax)."""
from __future__ import annotations
from typing import List
import numpy as np
from song_analysis.schema import EventEntry

def detect_events(energy_curve: List[float], beats: List[float]) -> List[EventEntry]:
    """Infer events from energy dynamics.

    Heuristics:
        - drop: sharp post-minimum rise
        - climax: earliest sample >= 95th percentile energy
    """
    events: List[EventEntry] = []
    if not energy_curve:
        return events
    ec = np.array(energy_curve)
    for i in range(2, len(ec) - 2):
        window_prev = ec[i-2:i]
        window_next = ec[i+1:i+3]
        if ec[i] < window_prev.mean() * 0.8 and window_next.mean() > ec[i] * 2.2:
            # align to nearest beat if available (by index similarity)
            if beats:
                idx = min(range(len(beats)), key=lambda b: abs(b - i))
                t = beats[idx]
            else:
                t = float(i)
            events.append(EventEntry('drop', float(t)))
    threshold = float(np.percentile(ec, 95))
    climax_idx = np.where(ec >= threshold)[0]
    if climax_idx.size > 0:
        ci = climax_idx[0]
        t = beats[min(range(len(beats)), key=lambda b: abs(beats[b] - ci))] if beats else float(ci)
        events.append(EventEntry('climax', float(t)))
    return events
