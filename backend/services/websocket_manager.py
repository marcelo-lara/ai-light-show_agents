import json
from typing import Dict, Any
from flask_socketio import emit
from backend.models.app_data import AppData

def get_app_state() -> Dict[str, Any]:
    """
    Return the initial state of the App
    """
    app_data = AppData()
    
    # Get current song name, default to None if no song is loaded
    current_song = None
    try:
        current_song = app_data.song_name
    except AttributeError:
        # No song loaded yet
        pass
    
    return {
        "type": "app_state",
        "data": {
            "current_song": current_song,
            "is_playing": app_data.is_playing,
            "current_time": app_data.current_time
        }
    }

def handle_new_connection():
    """
    Handler function for new WebSocket connections.
    Sends the current app_state to the newly connected client.
    """
    app_state = get_app_state()
    emit('app_state', app_state)
    print(f"🔗 Sent app_state to new connection: song='{app_state['data']['current_song']}', playing={app_state['data']['is_playing']}, time={app_state['data']['current_time']}s")

# Example schema for reference:
# {
#  "type": "app_state",
#  "data": {
#    "current_song": "born_slippy",  # from app_data.song_name
#    "is_playing": false,           # from app_data.is_playing
#    "current_time": 0.0            # from app_data.current_time (in seconds)
#  }
# }