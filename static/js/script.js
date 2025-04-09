document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("chat-form");
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
  
    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      const userMessage = input.value.trim();
      if (userMessage === "") return;
  
      appendMessage("You", userMessage, "user-message");
  
      try {
        const response = await fetch("/chatbot/get_response/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"), // Required for Django POST
          },
          body: JSON.stringify({ message: userMessage }),
        });
  
        const data = await response.json();
        const botReply = data.response || "Sorry, I didn't get that.";
        appendMessage("Bot", botReply, "bot-message");
      } catch (error) {
        console.error("Error:", error);
        appendMessage("Bot", "Something went wrong!", "bot-message");
      }
  
      input.value = "";
    });
  
    function appendMessage(sender, message, className) {
      const msgDiv = document.createElement("div");
      msgDiv.classList.add(className);
      msgDiv.textContent = `${sender === "You" ? "" : "Bot: "}${message}`;
      chatBox.appendChild(msgDiv);
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(
              cookie.substring(name.length + 1)
            );
            break;
          }
        }
      }
      return cookieValue;
    }
  });
  