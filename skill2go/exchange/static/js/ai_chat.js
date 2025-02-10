document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.querySelector(".chat-box");
    const userInput = document.getElementById("user-input");
    const micButton = document.getElementById("mic-button");
    const sendButton = document.querySelector(".chat-input button:last-of-type");


    function addMessage(sender, text) {
        const message = document.createElement("div");
        message.classList.add(sender);
        message.innerText = text;
        chatBox.appendChild(message);
        chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the latest message
    }

    function fetchTextToSpeech(text){
        fetch("/api/tts/",{
            method: "POST",
            headers:{
                "Content-Type":"application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ text: text }) 
        })
        .then(response => response.json())
        .then(data =>{
            if (data.audio){
                const audioBlob = new Blob([data.audio], {type: 'audio/wav'});
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                audio.play();
            }else {
                console.error("TTS response error:", data);
            }
        })
        .catch(error => console.error("Error fetching TTS:", error));
    }

    // requesting AI greeting when first time visitng the ai chat
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
                fetchTextToSpeech(data.response); // Speak greeting if enabled
            } else {
                console.error("AI response error:", data);
            }
        })
        .catch(error => console.error("Error fetching AI greeting:", error));
    }

    // Function to send the user message to the backend API
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
            } else if (data.response) { // Check for the 'response' property
                addMessage("ai", data.response);
                fetchTextToSpeech(data.response); // Speak response
            } else {
                console.error("Unexpected response:", data);
                addMessage("ai", "Unexpected response from AI.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            addMessage("ai", "Error communicating with AI.");
        });

        userInput.value = "";  // Clear input field
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

    // Fetch AI greeting when the page loads
    fetchGreeting();
});
