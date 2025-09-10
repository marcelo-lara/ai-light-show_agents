import json
from typing import Dict, Any
from flask_socketio import emit
from backend.models.app_data import AppData

def get_app_state() -> Dict[str, Any]:
    """
    Return the initial state of the App
    """
    app_data = AppData()
    
    # Get current song name, default to a known song if no song is loaded
    current_song = None
    current_song = app_data.song_name
    
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

def handle_play_audio():
    """
    Handle play audio command from frontend
    """
    app_data = AppData()
    app_data.is_playing = True
    
    # Emit updated state to all clients
    app_state = get_app_state()
    emit('app_state', app_state, broadcast=True)
    print(f"🎵 Audio playback started")

def handle_pause_audio():
    """
    Handle pause audio command from frontend
    """
    app_data = AppData()
    app_data.is_playing = False
    
    # Emit updated state to all clients
    app_state = get_app_state()
    emit('app_state', app_state, broadcast=True)
    print(f"⏸️ Audio playback paused")

def handle_stop_audio():
    """
    Handle stop audio command from frontend
    """
    app_data = AppData()
    app_data.is_playing = False
    app_data.current_time = 0.0
    
    # Emit updated state to all clients
    app_state = get_app_state()
    emit('app_state', app_state, broadcast=True)
    print(f"⏹️ Audio playback stopped")

def handle_seek_audio(params: Dict[str, Any]):
    """
    Handle seek audio command from frontend
    """
    time = params.get('time', 0.0)
    app_data = AppData()
    app_data.current_time = float(time)
    
    # Emit updated state to all clients
    app_state = get_app_state()
    emit('app_state', app_state, broadcast=True)
    print(f"⏭️ Audio seeked to {time:.2f}s")

# Example schema for reference:
# {
#  "type": "app_state",
#  "data": {
#    "current_song": "born_slippy",  # from app_data.song_name
#    "is_playing": false,           # from app_data.is_playing
#    "current_time": 0.0            # from app_data.current_time (in seconds)
#  }
# }