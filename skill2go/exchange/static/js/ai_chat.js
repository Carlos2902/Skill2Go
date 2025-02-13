document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.querySelector(".chat-box");
    const userInput = document.getElementById("user-input");
    const micButton = document.getElementById("mic-button");
    const sendButton = document.querySelector(".chat-input button:last-of-type");
    let preferredLanguage = "en"; 
    // Function to add a message to the chat box
    function addMessage(sender, text) {
        const message = document.createElement("div");
        message.classList.add("chat-message", `${sender}-message`);
        message.innerText = text;
        chatBox.appendChild(message);
        chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the latest message
    }

    // Function to fetch Text-to-Speech audio
    function fetchTextToSpeech(text) {
        fetch("/api/tts/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.json())
        .then(data => {
            if (data.audio) {
                const audioBytes = Uint8Array.from(atob(data.audio), c => c.charCodeAt(0));
                const audioBlob = new Blob([audioBytes], { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                audio.play();
            } else {
                console.error("TTS response error:", data);
            }
        })
        .catch(error => console.error("Error fetching TTS:", error));
    }

    // Request AI greeting when first visiting the AI chat
    function fetchGreeting() {
        fetch("/api/chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ message: "__GREETING__" })
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                addMessage("ai", data.response);
                preferredLanguage = data.preferred_language; 
                console.log(preferredLanguage) 
                fetchTextToSpeech(data.response);  // Speak greeting if enabled
            } else {
                console.error("AI response error:", data);
            }
        })
        .catch(error => console.error("Error fetching AI greeting:", error));
    }

    // Function to send the user's message to the backend API
    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        addMessage("user", message);

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
            } else if (data.response) {
                addMessage("ai", data.response);
                fetchTextToSpeech(data.response); 
            } else {
                console.error("Unexpected response:", data);
                addMessage("ai", "Unexpected response from AI.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            addMessage("ai", "Error communicating with AI.");
        });

        userInput.value = "";  
    }


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
        recognition.lang = preferredLanguage;  // Use the preferred language dynamically set by the backend
    
        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            sendMessage();  // Automatically send after speech recognition
        };
    
        recognition.onerror = function (event) {
            console.error("Speech recognition error:", event.error);
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

    // Fetch AI greeting when the page loads
    fetchGreeting();
});
