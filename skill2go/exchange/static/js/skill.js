document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.exchange-btn').forEach(button => {
        button.addEventListener('click', function () {
            const skillId = this.getAttribute('data-skill-id');
            const providerListElement = document.getElementById('providerList');
            providerListElement.innerHTML = ''; 
            // resquest for skill exchange
            fetch(`/get_skill_providers/${skillId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.providers && data.providers.length > 0) {
                        data.providers.forEach(provider => {
                            const providerItem = document.createElement('div');
                            providerItem.classList.add('provider-item', 'd-flex', 'align-items-center');
                            providerItem.innerHTML = `
                                <img src="${provider.profile_picture_url}" alt="${provider.username}" class="provider-img" style="width: 50px;">
                                <span class="provider-name">${provider.username}</span>
                                <button class="btn btn-primary request-btn" data-skill-id="${skillId}" data-provider-id="${provider.id}">Request Skill</button>
                            `;
                            providerListElement.appendChild(providerItem);
                        });
                        $('#providerModal').modal('show'); 
                    } else {
                        alert('No providers available for this skill.');
                    }
                })
                .catch(error => {
                    console.error('Error fetching providers:', error);
                });
        });
    });
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('request-btn')) {
            const skillId = event.target.getAttribute('data-skill-id');
            const providerId = event.target.getAttribute('data-provider-id');
            console.log('Skill ID:', skillId);
            console.log('Provider ID:', providerId);
            fetch('/create_skill_exchange/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()  
                },
                body: JSON.stringify({
                    skill_id: skillId,
                    provider_id: providerId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message); 
                    $('#providerModal').modal('hide'); 
                } else {
                    alert(data.message); 
                }
            })
            .catch(error => {
                console.error('Error sending skill request:', error);
            });
        }
    });   
});
function getCSRFToken() {
    const cookieValue = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}
