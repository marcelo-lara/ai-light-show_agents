# WebSocket Best Practices Implementation

This document outlines the best practices implemented for WebSocket communication between the frontend and backend in the AI Light Show Agents application.

## Architecture Overview

### Backend (Flask-SocketIO)
- **Location**: `backend/services/websocket_manager.py` and `backend/app.py`
- **Framework**: Flask-SocketIO with eventlet
- **Auto-initialization**: Loads default song on startup
- **Connection handler**: Sends `app_state` message immediately on new connections

### Frontend (Socket.IO Client)
- **Location**: `frontend/src/WebSocket.ts`
- **Framework**: Socket.IO client with TypeScript
- **Service pattern**: Singleton WebSocket service with React hooks
- **UI Integration**: Status component and hook-based state management

## Best Practices Implemented

### 1. Connection Management
```typescript
// Automatic environment detection
const URL = window.location.hostname === 'localhost' 
  ? "http://localhost:5000" 
  : `${window.location.protocol}//${window.location.host}`;

// Robust reconnection strategy
{
  autoConnect: true,
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
  timeout: 10000,
}
```

### 2. Error Handling & Resilience
- **Graceful degradation**: App works even when WebSocket is disconnected
- **Automatic reconnection**: Configurable retry logic with exponential backoff
- **Error callbacks**: Centralized error handling with user feedback
- **Connection state monitoring**: Real-time connection status updates

### 3. Type Safety
```typescript
export interface AppState {
  type: "app_state";
  data: {
    current_song: string | null;
  };
}
```

### 4. React Integration
```typescript
// Custom hook for easy component integration
const { isConnected, currentSong, error, sendMessage } = useWebSocket();
```

### 5. Event-Driven Architecture
- **Backend**: Sends `app_state` on connection
- **Frontend**: Subscribes to specific events
- **Separation of concerns**: WebSocket service separate from UI components

## Message Flow

### Initial Connection
1. **Frontend connects** → WebSocket service establishes connection
2. **Backend receives connection** → `handle_connect()` is triggered
3. **Backend sends app_state** → `get_app_state()` returns current song info
4. **Frontend receives app_state** → Hook updates component state
5. **UI updates** → Components show current song and connection status

### Example App State Message
```json
{
  "type": "app_state",
  "data": {
    "current_song": "born_slippy"
  }
}
```

## File Structure

```
frontend/src/
├── WebSocket.ts              # Core WebSocket service
├── hooks/
│   └── useWebSocket.ts       # React hook for WebSocket state
├── components/
│   ├── WebSocketStatus.tsx   # Connection status UI
│   └── AssistantChat.tsx     # Example usage
└── app.tsx                   # Main app integration

backend/
├── services/
│   └── websocket_manager.py  # WebSocket handlers
└── app.py                    # Flask-SocketIO setup
```

## Usage Examples

### In a React Component
```typescript
import { useWebSocket } from '../hooks/useWebSocket';

export function MyComponent() {
  const { isConnected, currentSong, sendMessage } = useWebSocket();
  
  const handleAction = () => {
    if (isConnected) {
      sendMessage('my_action', { param: 'value' });
    }
  };

  return (
    <div>
      <p>Song: {currentSong || 'No song loaded'}</p>
      <button onClick={handleAction} disabled={!isConnected}>
        Send Action
      </button>
    </div>
  );
}
```

### Adding New Message Types
1. **Backend**: Add event handler in `websocket_manager.py`
2. **Frontend**: Add type definition and handler in `WebSocket.ts`
3. **Components**: Use the `sendMessage` function from the hook

## Security Considerations

- **CORS**: Configured to allow frontend origin
- **Input validation**: Messages should be validated on backend
- **Rate limiting**: Consider implementing rate limiting for production
- **Authentication**: Can be added to connection handshake

## Performance Optimizations

- **Singleton service**: Single WebSocket connection shared across app
- **Event batching**: Consider batching frequent updates
- **Selective subscriptions**: Only subscribe to needed events
- **Cleanup**: Proper cleanup on component unmount

## Monitoring & Debugging

- **Console logging**: Comprehensive logging with emojis for easy identification
- **Connection status**: Visual indicators in UI
- **Error reporting**: Centralized error handling
- **Reconnection feedback**: User awareness of connection state

This implementation provides a robust, scalable foundation for real-time communication in the AI Light Show application.
