// Make sure to set team_id from template
const socket = io();
const team_id = document.getElementById("messages").dataset.teamId;
const messages = document.getElementById("messages");
const message = document.getElementById("message");
const currentUser = messages.dataset.username;
const csrf_token = messages.dataset.csrfToken;
const team_name = messages.dataset.teamName;

// Join the team room
socket.emit("join", { room: `team_${team_id}`, team_id: team_id });

let currentRoom = `team_${team_id}`;
let currentRoomType = "team";
let currentDMUser = null;

// Function to clear messages
function clearMessages() {
  messages.innerHTML = "";
}

// Function to update chat title
function updateChatTitle(title) {
  document.getElementById("chat-title").textContent = title;
}

// Handle sidebar button clicks
document.querySelectorAll(".chat-switch-btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    const room = btn.dataset.room;
    const type = btn.dataset.type;
    document
      .querySelectorAll(".chat-switch-btn")
      .forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    clearMessages();

    // Leave previous room
    socket.emit("leave", { room: currentRoom, team_id: team_id });

    if (type === "team") {
      currentRoom = room;
      currentRoomType = "team";
      updateChatTitle(`${team_name} Team Chat`);
      socket.emit("join", { room: currentRoom, team_id: team_id });
    } else if (type === "dm") {
      currentRoom = room;
      currentRoomType = "dm";
      currentDMUser = btn.dataset.user;
      updateChatTitle(`DM: ${currentDMUser}`);
      const currentUser = messages.dataset.username;
      const dmRoom = `dm_${[currentUser, currentDMUser].sort().join("_")}`;
      currentRoom = dmRoom;
      socket.emit("join_dm", { user1: currentUser, user2: currentDMUser });
    }
  });
});

// Create a new message
const createMessage = (name, messageText, timestamp) => {
  const messageElement = document.createElement("div");
  messageElement.classList.add("message");
  if (name === currentUser) {
    messageElement.classList.add("my-message");
  } else {
    messageElement.classList.add("other-message");
  }
  // Format timestamp (optional: make it prettier)
  const timeString = timestamp
    ? `<span class="msg-timestamp">${timestamp}</span>`
    : "";
  messageElement.innerHTML = `${timeString} <strong>${name}:</strong> ${messageText}`;
  messages.appendChild(messageElement);
  messages.scrollTop = messages.scrollHeight; // Scroll to the bottom
};

// Send message to current room
const sendMessage = () => {
  const messageText = message.value.trim();
  if (!messageText) return;

  if (currentRoomType === "team") {
    socket.emit("send_message", {
      room: currentRoom,
      message: messageText,
      team_id: team_id,
      csrf_token: csrf_token,
    });
  } else if (currentRoomType === "dm" && currentDMUser) {
    const currentUser = messages.dataset.username;
    socket.emit("send_private_message", {
      sender: currentUser,
      recipient: currentDMUser,
      message: messageText,
      csrf_token: csrf_token,
    });
  }
  message.value = "";
};

// Message search/filter
document
  .getElementById("message-search")
  .addEventListener("input", function () {
    const search = this.value.toLowerCase();
    document.querySelectorAll("#messages .message").forEach((msg) => {
      msg.style.display = msg.textContent.toLowerCase().includes(search)
        ? ""
        : "none";
    });
  });

document.getElementById("send-btn").addEventListener("click", sendMessage);

// Handle Enter key for sending messages
message.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    event.preventDefault(); // Prevents adding a newline
    sendMessage();
  }
});

// Listen for messages
socket.on("message", (data) => {
  createMessage(data.name, data.message, data.timestamp);
});
socket.on("private_message", (data) => {
  createMessage(data.name, data.message, data.timestamp);
});
