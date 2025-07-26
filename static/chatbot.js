async function sendMessage() {
  // Obtener el valor del input del usuario
  const input = document.getElementById("userInput");
  // Obtener el contenedor del chat donde se mostrarán los mensajes
  const chatbox = document.getElementById("chat");
  // Guardar el mensaje que escribió el usuario
  const message = input.value;

  // Mostrar el mensaje del usuario en la interfaz del chat
  chatbox.innerHTML += `<p><strong>Tú:</strong> ${message}</p>`;
  // Limpiar el campo de entrada después de enviar
  input.value = "";

  // Enviar el mensaje al servidor usando fetch (POST a la ruta /chat)
  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message }) // Convertir el mensaje a JSON
  });

  // Esperar la respuesta del servidor y convertirla a JSON
  const data = await response.json();
  // Mostrar la respuesta del bot en la interfaz del chat
  chatbox.innerHTML += `<p><strong>Bot:</strong> ${data.reply}</p>`;
  // Hacer scroll automáticamente hacia el último mensaje
  chatbox.scrollTop = chatbox.scrollHeight;
}
