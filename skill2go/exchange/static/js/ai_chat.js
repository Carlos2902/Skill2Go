document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.querySelector(".chat-box");
    const userInput = document.getElementById("user-input");
    const micButton = document.getElementById("mic-button");
    const sendButton = document.querySelector(".chat-input button:last-of-type");

    // Function to display a message in the chat box
    function addMessage(sender, text) {
        const message = document.createElement("div");
        message.classList.add(sender);
        message.innerText = text;
        chatBox.appendChild(message);
        chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the latest message
    }

    // Function to send the user message to the backend API
    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;  // Ignore empty messages

        addMessage("user", message);  // Display user message

        fetch("/api/chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),  
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                addMessage("ai", "Oops! Something went wrong.");
            } else if (data.response) { // Check for the 'response' property
                addMessage("ai", data.response); // Display the actual text from data.response
                speakText(data.response); // Pass data.response to speakText
            } else {
              console.error("Unexpected response:", data); // Log the whole data object
              addMessage("ai", "Unexpected response from AI.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            addMessage("ai", "Error communicating with AI.");
        });

        userInput.value = "";  // Clear input field
    }

    // Function to convert AI text response into speech
    function speakText(text) {
        const utterance = new SpeechSynthesisUtterance(text);
        speechSynthesis.speak(utterance);
    }

    // Capture text input via Enter key
    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    // Send button click event
    sendButton.addEventListener("click", sendMessage);

    // Microphone button click event (Speech-to-Text)
    micButton.addEventListener("click", function () {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = "en-US";  // Adjust language dynamically if needed

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            sendMessage();  // Automatically send after speech recognition
        };

        recognition.start();
    });

    // Function to get CSRF token (required for Django)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            document.cookie.split(";").forEach(cookie => {
                let trimmedCookie = cookie.trim();
                if (trimmedCookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(trimmedCookie.substring(name.length + 1));
                }
            });
        }
        return cookieValue;
    }

});

