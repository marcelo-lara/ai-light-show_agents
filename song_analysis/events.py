"""Derive macro musical ev            # Convert energy index to time
            event_time = float(energy_times[i])
            # align to nearest beat if available
            if beats:
                nearest_beat_idx = min(range(len(beats)), key=lambda b_idx: abs(beats[b_idx] - event_time))
                t = beats[nearest_beat_idx]drop, climax)."""
from __future__ import annotations
from typing import List
import numpy as np
from song_analysis.schema import EventEntry

def detect_events(energy_curve: List[float], beats: List[float], sr: int = 22050) -> List[EventEntry]:
    """Infer events from energy dynamics.

    Heuristics:
        - drop: sharp post-minimum rise
        - climax: earliest sample >= 95th percentile energy
    """
    events: List[EventEntry] = []
    if not energy_curve:
        return events
    ec = np.array(energy_curve)
    # Calculate time mapping for energy curve
    # Energy curve uses 0.5s windows with 50% overlap, so hop_length = 0.25s
    hop_length_s = 0.25  # 0.5s window / 2
    energy_times = np.arange(len(ec)) * hop_length_s
    
    for i in range(2, len(ec) - 2):
        window_prev = ec[i-2:i]
        window_next = ec[i+1:i+3]
        if ec[i] < window_prev.mean() * 0.8 and window_next.mean() > ec[i] * 2.2:
            # Convert energy index to time
            event_time = energy_times[i]
            # align to nearest beat if available
            if beats:
                nearest_beat_idx = min(range(len(beats)), key=lambda b: abs(beats[b] - event_time))
                t = beats[nearest_beat_idx]
            else:
                t = event_time
            events.append(EventEntry('drop', float(t)))
    threshold = float(np.percentile(ec, 95))
    climax_indices = np.where(ec >= threshold)[0]
    if climax_indices.size > 0:
        ci = climax_indices[0]
        # Convert energy index to time
        climax_time = float(energy_times[ci])
        # align to nearest beat if available
        if beats:
            nearest_beat_idx = min(range(len(beats)), key=lambda b_idx: abs(beats[b_idx] - climax_time))
            t = beats[nearest_beat_idx]
        else:
            t = climax_time
        events.append(EventEntry('climax', float(t)))
    
    # Remove duplicate events at the same time (within 0.1s tolerance)
    unique_events = []
    for event in events:
        is_duplicate = False
        for unique_event in unique_events:
            if (abs(event.time - unique_event.time) < 0.1 and 
                event.type == unique_event.type):
                is_duplicate = True
                break
        if not is_duplicate:
            unique_events.append(event)
    
    return unique_events
