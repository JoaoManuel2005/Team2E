// Add JavaScript to handle the toggle switch
document.addEventListener('DOMContentLoaded', function() {
    const privacyToggle = document.getElementById('privacy-toggle');
    
    privacyToggle.addEventListener('change', function() {
        // Send AJAX request to update privacy setting
        fetch('{% url "update-privacy" %}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({
                'private': this.checked
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the visibility indicator
                location.reload();
            } else {
                alert('Failed to update privacy settings');
                // Revert the toggle if update failed
                this.checked = !this.checked;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating privacy settings');
            // Revert the toggle if update failed
            this.checked = !this.checked;
        });
    });
});