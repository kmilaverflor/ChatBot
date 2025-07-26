async function sendMessage() {
  const input = document.getElementById("userInput");
  const chatbox = document.getElementById("chatbox");
  const message = input.value;

  chatbox.innerHTML += `<p><strong>Tú:</strong> ${message}</p>`;
  input.value = "";

  const response = await fetch("https://TU_BACKEND_URL/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message })
  });

  const data = await response.json();
  chatbox.innerHTML += `<p><strong>Bot:</strong> ${data.reply}</p>`;
  chatbox.scrollTop = chatbox.scrollHeight;
}
