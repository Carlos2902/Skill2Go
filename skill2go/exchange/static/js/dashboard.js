document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("preferenceForm");
  const formContainer = document.getElementById("skill-preference-form");
  const postsContainer = document.getElementById("personalized-posts")

  const steps = document.querySelectorAll(".form-step");
  let currentStep = 0;

  function showStep(step) {
      steps.forEach((el, index) => {
          el.style.display = index === step ? "block" : "none";
      });
  }

  document.querySelectorAll(".next-step").forEach(button => {
      button.addEventListener("click", () => {
          if (currentStep < steps.length - 1) {
              currentStep++;
              showStep(currentStep);
          }
      });
  });

  document.querySelectorAll(".prev-step").forEach(button => {
      button.addEventListener("click", () => {
          if (currentStep > 0) {
              currentStep--;
              showStep(currentStep);
          }
      });
  });

  document.getElementById("preferenceForm").addEventListener("submit", (event) => {
      event.preventDefault();
      document.getElementById("skill-preference-form").style.display = "none";
      document.getElementById("personalized-posts").classList.remove("hidden");
  });


  showStep(currentStep);


  form.addEventListener("submit", function (event) {
      event.preventDefault();

      const skillType = document.getElementById("skillType").value;
      const frequency = document.getElementById("frequency").value;
      const personality = document.getElementById("personality").value;

      const userPreferences = { skillType, frequency, personality };
      localStorage.setItem("userPreferences", JSON.stringify(userPreferences));

      fetch("/generate-skill-posts/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify(userPreferences)
    })
    .then(response => response.json())
    .then(data => {
        if (data.posts && data.posts.length > 0) {
            const post = data.posts[0].generated_text;
            console.log('Generated Post:', post);
            updatePosts(post); 
        } else {
            console.error('No posts generated or invalid response:', data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
  });
  function updatePosts(response) {
    console.log("Raw Response:", response);
    let matches = [...response.matchAll(/\{[\s\S]*?\}/g)]; 
    if (!matches.length) {
        console.error("No valid JSON found in response.");
        return;
    }
    let posts = [];
    try {
        posts = matches.map(match => JSON.parse(match[0])); 
    } catch (error) {
        console.error("Error parsing JSON:", error);
        return;
    }

    console.log("Parsed Data:", posts);
    if (Array.isArray(posts)) {
        const container = document.getElementById("posts-container");
        container.innerHTML = "";

        posts.forEach(post => {
            const postElement = document.createElement("div");
            postElement.classList.add("post");
            postElement.innerHTML = `
                <h4>${post.title}</h4>
                <p>${post.content}</p>
            `;
            container.appendChild(postElement);
        });
    } else {
        console.error("No posts found in parsed response:", posts);
    }
}


//   function fetchUpdatedPosts() {
//       fetch("/get_latest_posts/")
//       .then(response => response.json())
//       .then(data => {
//           updatePosts(data);
//       });
//   }

//   setInterval(fetchUpdatedPosts, 60000);

  function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, "csrftoken".length + 1) === "csrftoken=") {
                cookieValue = decodeURIComponent(cookie.substring("csrftoken".length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  
});


