export function AssistantChat() {
  return (
    <div class="card">
      <h3>Assistant Chat</h3>
      <div class="chat-window">
        <div class="message user">Hello</div>
        <div class="message assistant">Hi, how can I help you?</div>
      </div>
      <input type="text" placeholder="Type a message..." />
    </div>
  );
}
