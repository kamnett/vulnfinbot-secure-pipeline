
const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const messages = document.getElementById("messages");
const button = document.getElementById("send-button");

function addMessage(text, sender) {
    const element = document.createElement("div");
    element.className = "message " + sender;
    element.textContent = text;
    messages.appendChild(element);
    messages.scrollTop = messages.scrollHeight;
}

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const message = input.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");
    input.value = "";
    button.disabled = true;

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        if (!response.ok) {
            addMessage(data.error || "Something went wrong.", "bot");
        } else {
            addMessage(data.response, "bot");
        }
    } catch (error) {
        addMessage("Unable to connect to the server.", "bot");
    } finally {
        button.disabled = false;
        input.focus();
    }
});
