document.addEventListener('DOMContentLoaded', function() {
    const privacyToggle = document.getElementById('privacy-toggle');

    if (!privacyToggle) {
        console.error("Privacy toggle not found.");
        return;
    }

    // Get the correct URL from the data attribute in myaccount.html
    const updatePrivacyUrl = privacyToggle.getAttribute('data-privacy-url');

    // Correctly get CSRF token from the hidden input field
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    privacyToggle.addEventListener('change', function() {
        fetch(updatePrivacyUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // Use correct CSRF token
            },
            body: JSON.stringify({
                'private': this.checked
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Failed to update privacy settings');
                this.checked = !this.checked;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating privacy settings');
            this.checked = !this.checked;
        });
    });
});
