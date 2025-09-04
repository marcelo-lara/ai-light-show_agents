import { useState, useEffect, useCallback } from 'preact/hooks';
import { webSocketService } from '../WebSocket';
import type { AppState } from '../WebSocket';

export interface WebSocketHookReturn {
  isConnected: boolean;
  currentSong: string | null;
  error: string | null;
  sendMessage: (action: string, params?: any) => void;
  reconnect: () => void;
}

export function useWebSocket(): WebSocketHookReturn {
  const [isConnected, setIsConnected] = useState(false);
  const [currentSong, setCurrentSong] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Handle app state updates
  const handleAppState = useCallback((state: AppState) => {
    console.log('Hook received app state:', state);
    setCurrentSong(state.data.current_song);
    // Clear any previous errors when we get a valid state
    setError(null);
  }, []);

  // Handle errors
  const handleError = useCallback((err: any) => {
    console.error('WebSocket error in hook:', err);
    setError(err.message || 'WebSocket connection error');
  }, []);

  // Send message wrapper
  const sendMessage = useCallback((action: string, params?: any) => {
    webSocketService.sendMessage(action, params);
  }, []);

  // Reconnect function
  const reconnect = useCallback(() => {
    setError(null);
    webSocketService.disconnect();
    webSocketService.connect();
  }, []);

  useEffect(() => {
    // Set up listeners
    webSocketService.onAppState(handleAppState);
    webSocketService.onError(handleError);

    // Monitor connection state
    const checkConnection = () => {
      setIsConnected(webSocketService.isConnected);
    };

    // Check connection state every second
    const interval = setInterval(checkConnection, 1000);
    
    // Initial check
    checkConnection();

    // Cleanup
    return () => {
      clearInterval(interval);
      // Note: We don't disconnect the service here as it should persist across component mounts
    };
  }, [handleAppState, handleError]);

  return {
    isConnected,
    currentSong,
    error,
    sendMessage,
    reconnect
  };
}
