import { useWebSocket } from '../hooks/useWebSocket';

export function AssistantChat() {
  const { currentSong, isConnected, sendMessage } = useWebSocket();

  const handleSendMessage = () => {
    if (isConnected) {
      sendMessage('chat_message', { message: 'Hello from frontend!' });
    }
  };

  return (
    <div class="card">
      <h3>Assistant Chat</h3>
      {currentSong && (
        <div class="current-song-info">
          <small class="muted">Working with: {currentSong}</small>
        </div>
      )}
      <div class="chat-window">
        <div class="message user">Hello</div>
        <div class="message assistant">Hi, how can I help you with your light show?</div>
        {currentSong && (
          <div class="message assistant">
            I can see you're working with "{currentSong}". What would you like to do?
          </div>
        )}
      </div>
      <div class="chat-input-section">
        <input type="text" placeholder="Type a message..." />
        <button onClick={handleSendMessage} disabled={!isConnected}>
          Send
        </button>
      </div>
    </div>
  );
}
