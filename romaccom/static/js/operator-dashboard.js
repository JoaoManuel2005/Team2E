document.addEventListener('DOMContentLoaded', function() {
    // Image upload functionality
    const uploadTrigger = document.getElementById('upload-trigger');
    const imageUpload = document.getElementById('image-upload');
    
    uploadTrigger.addEventListener('click', function() {
        imageUpload.click();
    });
    
    imageUpload.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            uploadImages(e.target.files);
        }
    });
    
    // Drag and drop functionality
    uploadTrigger.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadTrigger.classList.add('dragging');
    });
    
    uploadTrigger.addEventListener('dragleave', function() {
        uploadTrigger.classList.remove('dragging');
    });
    
    uploadTrigger.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadTrigger.classList.remove('dragging');
        if (e.dataTransfer.files.length > 0) {
            uploadImages(e.dataTransfer.files);
        }
    });
    
    function uploadImages(files) {
        const formData = new FormData();
        formData.append('accommodation_id', accommodationId); // Use global var
        
        for (let i = 0; i < files.length; i++) {
            formData.append('images', files[i]);
        }
        
        // Send AJAX request to upload images
        fetch(uploadImageUrl, { // Use global var
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Refresh the page to show new images
                location.reload();
            } else {
                alert('Error uploading images: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while uploading images.');
        });
    }
    
    // Save changes functionality
    document.getElementById('save-changes-btn').addEventListener('click', function() {
        const form = document.getElementById('accom-info-form');
        const formData = new FormData(form);
        
        // Log form data for debugging
        console.log("Submitting form data:");
        for (let pair of formData.entries()) {
            console.log(pair[0] + ': ' + pair[1]);
        }
        
        // Use the global variable for URL
        fetch(updateAccommodationUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'same-origin' // Important for CSRF
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Show success message
                alert('Accommodation information updated successfully!');
                
                // Get the view public page link more reliably
                const publicPageLink = document.querySelector('.dashboard-actions a.btn-outline');
                
                if (publicPageLink) {
                    // Open in new tab with cache buster
                    window.open(publicPageLink.href + '?t=' + new Date().getTime(), '_blank');
                } else {
                    // Fallback - just reload the current page
                    location.reload();
                }
            } else {
                alert('Error updating accommodation: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating the accommodation information: ' + error.message);
        });
    });
    
    // Delete accommodation functionality
    const deleteButton = document.getElementById('delete-accom-btn');
    const confirmModal = document.getElementById('confirm-modal');
    const modalClose = document.getElementById('modal-close');
    const cancelDelete = document.getElementById('cancel-delete');
    const confirmDelete = document.getElementById('confirm-delete');
    
    deleteButton.addEventListener('click', function() {
        confirmModal.style.display = 'flex';
    });
    
    modalClose.addEventListener('click', function() {
        confirmModal.style.display = 'none';
    });
    
    cancelDelete.addEventListener('click', function() {
        confirmModal.style.display = 'none';
    });
    
    confirmDelete.addEventListener('click', function() {
        fetch(deleteAccommodationUrl, { // Use global var
            method: 'POST',
            body: JSON.stringify({
                accommodation_id: accommodationId // Use global var
            }),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Use the redirect URL provided by the server
                window.location.href = data.redirect_url || operatorDashboardUrl;
            } else {
                alert('Error deleting accommodation: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting the accommodation.');
        });
    });
    
    // Set main image functionality
    document.querySelectorAll('.set-main-image').forEach(button => {
        button.addEventListener('click', function() {
            const imageId = this.getAttribute('data-image-id');
            
            fetch(setMainImageUrl, { // Use global var
                method: 'POST',
                body: JSON.stringify({
                    image_id: imageId,
                    accommodation_id: accommodationId // Use global var
                }),
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error setting main image: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while setting the main image.');
            });
        });
    });
    
    // Delete image functionality
    document.querySelectorAll('.delete-image').forEach(button => {
        button.addEventListener('click', function() {
            if (confirm('Are you sure you want to delete this image?')) {
                const imageId = this.getAttribute('data-image-id');
                
                fetch(deleteImageUrl, { // Use global var
                    method: 'POST',
                    body: JSON.stringify({
                        image_id: imageId
                    }),
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Error deleting image: ' + data.error);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while deleting the image.');
                });
            }
        });
    });
    
    // Utility function to get CSRF token
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
});