from typing import Dict

class DMXCanvas:
    """
    A Dictionary containing DMX frames.
    Each frame is a key-value pair of time and byte array of all 255 channel values.
    """
    def __init__(self, duration: float = 0, fps: int = 50):
        self.duration = duration
        self.fps = fps
        self.init_canvas()

    @property
    def frames(self) -> dict[float, bytearray]:
        """Return all DMX frames"""
        return self._frames

    def init_canvas(self):
        """Initialize the DMX canvas with default frames."""
        _frame_length = 1.0 / self.fps
        self._frames: Dict[float, bytearray] = {}
        for i in range(int(self.duration * self.fps)):
            frame_time = round(i * _frame_length, 2)
            # Initialize with a default DMX frame
            self._frames[frame_time] = bytearray(512)

    def get_frame(self, frame_time: float) -> bytearray:
        """Return the DMX frame at a specific or nearest time."""
        if frame_time in self._frames:
            return self._frames[frame_time]
        # If exact frame not found, return the nearest previous frame
        nearest_time = max(t for t in self._frames if t <= frame_time)
        return self._frames[nearest_time] if nearest_time else bytearray(255)
    
    def set_frame(self, frame_time: float, frame_data: bytearray):
        """Set the DMX frame at a specific or nearest time."""
        if frame_time in self._frames:
            self._frames[frame_time] = frame_data
        else:
            # If exact frame not found, set the nearest previous frame
            nearest_time = max(t for t in self._frames if t <= frame_time)
            if nearest_time:
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
            nearest_time = max(t for t in self._frames if t <= frame_time)
            if nearest_time:
                self._frames[nearest_time][channel] = value
                

    def get_canvas_log(self, start_time: float = 0, end_time: float = 0, first_channel: int = 0, last_channel: int = 255) -> str:
        """Return a log of all DMX frames and their values."""
        log = []
        for time, frame in self._frames.items():
            if start_time <= time <= end_time:
                frame_slice = frame[first_channel:last_channel + 1]
                hex_values = " ".join([f"{byte:02x}" for byte in frame_slice])
                log.append(f"{time:.2f} | {hex_values}")
        return "\n".join(log)
