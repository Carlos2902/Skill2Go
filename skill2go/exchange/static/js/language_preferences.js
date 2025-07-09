document.addEventListener("DOMContentLoaded", function(){
    let currentSlide = 1;

    window.nextSlide = function(slideNumber){
        document.getElementById(`slide-${currentSlide}`).classList.remove('active');
        document.getElementById(`slide-${slideNumber}`).classList.add('active');
        currentSlide = slideNumber;
    };

    window.submitPreferences = function(){
        const data = {
            "preferred_language":document.getElementById('preferred_language').value,
            "skill_level":document.getElementById('skill_level').value,
            "learning_goals":document.getElementById('learning_goals').value
        };

        fetch("/preferences/", {
            method: "POST",
            headers: {
                "Content-Type" : "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body:JSON.stringify(data),
        })

        .then(response => response.json())
        .then(()=>{
            nextSlide(5);
            setTimeout(()=>{
                window.location.href = "/ai_chat/";
            } ,5000);
        })
        .catch(error => console.error('Error saving preferences:', error))
    };

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

})