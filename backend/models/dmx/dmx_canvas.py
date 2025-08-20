import inspect
from typing import Callable, Dict, Optional

class DMXCanvas:
    """
    Singleton DMX canvas.
    A Dictionary containing DMX frames.
    Each frame is a key-value pair of time and bytearray of 512 channel values.
    Lights values are pre-rendered values to be sent to the DMX controller (like a light-painted canvas).
    """
    _instance = None

    def __new__(cls, duration: float = 0, fps: int = 50):
        # Return the single instance if it exists, otherwise create it.
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, duration: float = 0, fps: int = 50):
        # Initialize only once. Subsequent constructor calls return the same instance
        # and won't reinitialize internal state.
        if getattr(self, "_initialized", False):
            return
        self._duration = duration
        self._fps = fps
        self.init_canvas()
        self._initialized = True
        
    @property
    def duration(self) -> float:
        """Return the duration of the DMX canvas."""
        return self._duration

    @property
    def frames(self) -> dict[float, bytearray]:
        """Return all DMX frames"""
        return self._frames

    def init_canvas(self, duration: Optional[float] = None, fps: Optional[int] = None):
        """Initialize the DMX canvas with default frames.
        Use None as the default to mean "leave current value unchanged".
        If a value is provided, update the instance and use it to build frames.
        """
        self._duration = duration if duration is not None else self._duration
        self._fps = fps if fps is not None else self._fps

        _frame_length = 1.0 / self._fps
        self._frames: Dict[float, bytearray] = {}
        for i in range(int(self._duration * self._fps)):
            frame_time = round(i * _frame_length, 2)
            # Initialize with a default DMX frame
            self._frames[frame_time] = bytearray(512)

    def get_frame(self, frame_time: float) -> bytearray:
        """Return the DMX frame at a specific or nearest time."""
        if frame_time in self._frames:
            return self._frames[frame_time]
        # If exact frame not found, return the nearest previous frame (if any).
        candidates = [t for t in self._frames if t <= frame_time]
        if not candidates:
            # No frames before requested time: return a blank default frame.
            return bytearray(512)
        nearest_time = max(candidates)
        return self._frames[nearest_time]
    
    def set_frame(self, frame_time: float, frame_data: bytearray):
        """Set the DMX frame at a specific or nearest time."""
        if frame_time in self._frames:
            self._frames[frame_time] = frame_data
        else:
            # If exact frame not found, set the nearest previous frame
            candidates = [t for t in self._frames if t <= frame_time]
            if not candidates:
                # No appropriate frame: create new entry at requested time.
                self._frames[frame_time] = frame_data
                return
            nearest_time = max(candidates)
            self._frames[nearest_time] = frame_data

    def set_frame_value(self, frame_time: float, channel: int, value: int):
        """
        Set the value of a specific channel in a DMX frame. 
        If exact frame not found, set the nearest previous frame
        """
        frame = self.get_frame(frame_time)
        if frame:
            frame[channel] = value
        else:
            # If exact frame not found, set the nearest previous frame
            candidates = [t for t in self._frames if t <= frame_time]
            if not candidates:
                # no frame exists yet; create a new blank frame at requested time then set value
                new_frame = bytearray(512)
                new_frame[channel] = value
                self._frames[frame_time] = new_frame
                return
            nearest_time = max(candidates)
            self._frames[nearest_time][channel] = value
                

    def get_canvas_log(self, start_time: float = 0, end_time: float = 0, first_channel: int = 0, last_channel: int = 255) -> str:
        """Return a log of all DMX frames and their values."""
        log = []
        for time, frame in self._frames.items():
            if start_time <= time <= end_time:
                frame_slice = frame[first_channel:last_channel + 1]
                hex_values = " ".join([f"{byte:02x}" for byte in frame_slice])
                log.append(f"{time:.2f} | {hex_values}")
        if len(log) == 0:
            log.append("No frames found in the specified range.")
        return "\n".join(log)

    def render(self, method: Callable, start_time: float = 0, duration: float = 0):
        """Render the DMX canvas as a series of frames."""
        end_time = start_time + duration
        if duration == 0:
            end_time = self.duration

        for frame_time in self._frames:
            if start_time <= frame_time <= end_time:
                params = inspect.signature(method).parameters
                if len(params) == 1:
                    method(frame_time)
                elif len(params) == 2:
                    progress = (frame_time - start_time) / duration if duration > 0 else 1.0
                    method(frame_time, progress)