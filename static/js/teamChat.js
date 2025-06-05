// Make sure to set team_id from template
const socket = io();
const team_id = document.getElementById("messages").dataset.teamId;
const messages = document.getElementById("messages");
const message = document.getElementById("message");
const currentUser = messages.dataset.username;

// Join the team room
socket.emit("join", { room: `team_${team_id}`, team_id: team_id });

// Create a new message
const createMessage = (name, messageText) => {
  const messageElement = document.createElement("div");
  messageElement.classList.add("message");
  if (name === currentUser) {
    messageElement.classList.add("my-message");
  } else {
    messageElement.classList.add("other-message");
  }
  messageElement.innerHTML = `<strong>${name}:</strong> ${messageText}`;
  messages.appendChild(messageElement);
  messages.scrollTop = messages.scrollHeight; // Scroll to the bottom
};

socket.on("message", (data) => {
  createMessage(data.name, data.message);
});

const sendMessage = () => {
  const messageText = message.value.trim();
  if (messageText) {
    socket.emit("send_message", {
      room: `team_${team_id}`,
      message: messageText,
      team_id: team_id,
    });
    message.value = ""; // Clear the input field
  }
};

document.getElementById("send-btn").addEventListener("click", sendMessage);
