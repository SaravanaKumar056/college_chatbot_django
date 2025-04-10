document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("chat-form");
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const typingIndicator = document.getElementById("typing-indicator");


  chatBox.scrollTop = chatBox.scrollHeight;

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const userMessage = input.value.trim();
    if (userMessage === "") return;

    appendMessage("You", userMessage, "user-message");
    input.value = "";

    showTyping();

    try {
      const response = await fetch("/chatbot/get_response/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ message: userMessage }),
      });

      const data = await response.json();
      const botReply = data.response || "Sorry, I didn't get that.";
      appendMessage("Bot", botReply, "bot-message");
    } catch (error) {
      console.error("Error:", error);
      appendMessage("Bot", "Something went wrong!", "bot-message");
    } finally {
      hideTyping();
    }
  });

  function appendMessage(sender, message, className) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add(className);
    msgDiv.textContent = `${sender === "Bot" ? "Bot: " : ""}${message}`;
    chatBox.insertBefore(msgDiv, typingIndicator);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function resetBot() {
    document.querySelector('.typing-indicator').classList.add('hidden');
    // reset chat box if needed
  }
  

  function showTyping() {
    typingIndicator.style.display = "block";
    typingIndicator.classList.remove("hidden");
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function hideTyping() {
    typingIndicator.style.display = "none";
    typingIndicator.classList.add("hidden");
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
// Show typing indicator
document.querySelector('.typing-indicator').classList.remove('hidden');

// After response is shown
setTimeout(() => {
  document.querySelector('.typing-indicator').classList.add('hidden');
}, 1000); // hide after 1 second or when the bot is done
