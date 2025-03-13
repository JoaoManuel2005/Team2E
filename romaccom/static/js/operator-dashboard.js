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
        formData.append('accommodation_id', '{{ accommodation.id }}');
        
        for (let i = 0; i < files.length; i++) {
            formData.append('images', files[i]);
        }
        
        // Send AJAX request to upload images
        fetch('{% url "upload_accommodation_images" %}', {
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
        
        fetch('{% url "update_accommodation" %}', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Accommodation information updated successfully!');
            } else {
                alert('Error updating accommodation: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating the accommodation information.');
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
        fetch('{% url "delete_accommodation" %}', {
            method: 'POST',
            body: JSON.stringify({
                accommodation_id: {{ accommodation.id }}
            }),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '{% url "operator_dashboard" %}';
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
            
            fetch('{% url "set_main_image" %}', {
                method: 'POST',
                body: JSON.stringify({
                    image_id: imageId,
                    accommodation_id: {{ accommodation.id }}
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
                
                fetch('{% url "delete_accommodation_image" %}', {
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