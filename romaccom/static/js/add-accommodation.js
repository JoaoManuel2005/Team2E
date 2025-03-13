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
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Improved validation function
    function validateForm() {
        // Reset error message
        errorMessage.style.display = 'none';
        
        // Check required fields
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
            // Show popup with missing fields
            const missingFieldsText = missingFields.join(', ');
            alert(`Please fill in all required fields: ${missingFieldsText}`);
            return false;
        }
        
        return true;
    }

    saveBtn.addEventListener('click', function() {
        // First validate the form
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
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Accommodation created successfully!');
                
                // Redirect to operator dashboard for the new accommodation
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                } else {
                    window.location.href = managementUrl;
                }
            } else {
                errorMessage.textContent = 'Error: ' + (data.error || 'Unknown error');
                errorMessage.style.display = 'block';
                // Also show a popup for more attention
                alert('Error: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorMessage.textContent = 'An error occurred while creating the accommodation: ' + error.message;
            errorMessage.style.display = 'block';
            // Also show a popup
            alert('An error occurred while creating the accommodation: ' + error.message);
        });
    });
});