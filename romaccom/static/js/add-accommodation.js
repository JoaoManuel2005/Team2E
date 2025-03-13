document.addEventListener('DOMContentLoaded', function() {
    const saveBtn = document.getElementById('save-changes-btn');
    const form = document.getElementById('accom-info-form');
    const errorMessage = document.getElementById('error-message');

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function validateForm() {
        errorMessage.style.display = 'none';

        const name = document.getElementById('accom-name').value.trim();
        const address = document.getElementById('accom-address').value.trim();
        const postcode = document.getElementById('accom-postcode').value.trim();
        const mapLink = document.getElementById('accom-map').value.trim();

        const missingFields = [];
        if (!name) missingFields.push('Accommodation Name');
        if (!address) missingFields.push('Address');
        if (!postcode) missingFields.push('Postcode');
        if (!mapLink) missingFields.push('Google Maps Embed Link');

        if (missingFields.length > 0) {
            alert(`Please fill in all required fields: ${missingFields.join(', ')}`);
            return false;
        }

        return true;
    }

    saveBtn.addEventListener('click', function() {
        if (!validateForm()) {
            return;
        }

        const formData = new FormData(form);

        fetch(createAccommodationUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'same-origin'
        })
        .then(response => response.json().then(data => ({ status: response.status, body: data }))) 
        .then(({ status, body }) => {
            if (status !== 200) {
                console.error('Error Response:', body);
                throw new Error(body.error || `Unknown error (HTTP ${status})`);
            }

            if (body.success) {
                alert('Accommodation created successfully!');
                window.location.href = body.redirect_url || managementUrl;
            } else {
                throw new Error(body.error || 'Unknown error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorMessage.textContent = 'An error occurred: ' + error.message;
            errorMessage.style.display = 'block';
            alert('An error occurred: ' + error.message);
        });
    });
});
