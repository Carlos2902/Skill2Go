document.addEventListener("DOMContentLoaded", function () {
    // Handle Accept button click
    const acceptButtons = document.querySelectorAll('.accept-btn');
    acceptButtons.forEach(button => {
      button.addEventListener('click', function() {
        const exchangeId = this.getAttribute('data-exchange-id');
  
        // Send an AJAX request to accept the skill exchange request
        fetch(`/accept_skill_exchange/${exchangeId}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
          },
          body: JSON.stringify({ status: 'Completed' })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert('Skill exchange accepted!');
            location.reload();  
          } else {
            alert('Failed to accept the request.');
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
      });
    });
  });
  