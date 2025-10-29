document.addEventListener("DOMContentLoaded", () => {
  const usernameInput = document.getElementById("username");
  const messageInput = document.getElementById("messageText");
  const sendButton = document.getElementById("sendBtn");
  const messagesDiv = document.getElementById("messages");

  // Get room_id from URL (example: /chat/123 -> 123)
  const roomId = window.location.pathname.split("/").pop();

  // Connect WebSocket (with username query)
  const ws = new WebSocket(
    `ws://${window.location.host}/ws/${roomId}?username=${encodeURIComponent(usernameInput.value || "Guest")}`
  );

  // ✅ Receive messages
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    displayMessage(data);
  };

  // ✅ Send message when button clicked or Enter pressed
  sendButton.onclick = sendMessage;
  messageInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  function sendMessage() {
    const username = usernameInput.value.trim();
    const message = messageInput.value.trim();
    if (!username || !message) return;

    const data = { username: username, content: message };
    ws.send(JSON.stringify(data));
    messageInput.value = "";
  }

  // ✅ Display message on screen
  function displayMessage(data) {
    const msgElement = document.createElement("div");
    msgElement.classList.add("message");

    // System (join/leave) messages
    if (data.system) {
      msgElement.innerHTML = `
        <div class="system-msg">
          ${data.content}
          <span class="msg-time">${data.timestamp}</span>
        </div>
      `;
    } 
    // Normal user messages
    else {
      msgElement.innerHTML = `
        <div class="msg-header">
          <b>${data.username}</b>
          <span class="msg-time">${data.timestamp}</span>
        </div>
        <div class="msg-content">${data.content}</div>
      `;
    }

    messagesDiv.appendChild(msgElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }
});
