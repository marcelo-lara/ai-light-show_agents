
from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
import os
import sys
import json
import asyncio
import eventlet
from typing import Dict, Any

# Patch eventlet for better async support with gunicorn
eventlet.monkey_patch()

# Add project root to path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models.app_data import AppData
from backend.services.websocket_manager import handle_new_connection

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'dist'), static_url_path='')
socketio = SocketIO(app, cors_allowed_origins="*")

# Global app_data instance
app_data = AppData()

# Initialize with a default song
try:
    app_data.load_song("born_slippy")
    print("Loaded default song: born_slippy")
except Exception as e:
    print(f"Warning: Could not load default song - {e}")
    print("App will start without a song loaded")

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/songs/<path:filename>')
def serve_song(filename):
    songs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'songs')
    return send_from_directory(songs_dir, filename)

@socketio.on('connect')
def handle_connect():
    """Handle new WebSocket connections"""
    print("New WebSocket connection established")
    handle_new_connection()

@socketio.on('message')
def handle_message(data):
    try:
        message = json.loads(data) if isinstance(data, str) else data
        action = message.get('action')
        params = message.get('params', {})
    except (json.JSONDecodeError, AttributeError):
        emit('error', {'error': 'Invalid message format'})
        return
    
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
