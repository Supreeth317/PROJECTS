document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const typingIndicator = document.getElementById("typing-indicator");

    chatForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const userMessage = userInput.value.trim();

        if (userMessage === "") return;

        appendMessage("You", userMessage, "user");
        userInput.value = "";

        typingIndicator.style.display = "block"; // Show typing indicator

        fetch("/get_response", {
            method: "POST",
            body: JSON.stringify({ message: userMessage }),
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            typingIndicator.style.display = "none"; // Hide typing indicator
            appendMessage("Chatbot", data.response, "bot");
        });
    });

    function appendMessage(sender, message, senderClass) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", senderClass);
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
