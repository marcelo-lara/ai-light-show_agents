import { useWebSocket } from '../hooks/useWebSocket';

export function WebSocketStatus() {
  const { isConnected, currentSong, error, reconnect } = useWebSocket();

  return (
    <div class="websocket-status">
      <div class="connection-indicator">
        <div class={`status-dot ${isConnected ? 'connected' : 'disconnected'}`}></div>
        <span class="status-text">
          {isConnected ? 'Connected' : 'Disconnected'}
        </span>
        {!isConnected && !error && (
          <button onClick={reconnect} class="reconnect-btn">
            Reconnect
          </button>
        )}
      </div>
      
      {error && (
        <div class="error-message">
          <span class="error-text">Error: {error}</span>
          <button onClick={reconnect} class="reconnect-btn">
            Retry
          </button>
        </div>
      )}
      
      {currentSong && (
        <div class="current-song">
          <span class="song-label">Current Song:</span>
          <span class="song-name">{currentSong}</span>
        </div>
      )}
    </div>
  );
}
