/**
 * Handles image upload functionality through button click or drag-and-drop
 */
document.addEventListener('DOMContentLoaded', function() {
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
        /**
     * Uploads selected images to the server
     * @param files - The files to be uploaded
     */

    function uploadImages(files) {
        const formData = new FormData();
        formData.append('accommodation_id', accommodationId); 
        
        for (let i = 0; i < files.length; i++) {
            formData.append('images', files[i]);
        }
        
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
    /**
     * Validates the accommodation form fields before submission
     * @returns {boolean} - Returns true if form is valid, false otherwise
     */

    function validateForm() {
        const name = document.getElementById('accom-name').value.trim();
        const address = document.getElementById('accom-address').value.trim();
        const postcode = document.getElementById('accom-postcode').value.trim();

        const nameRegex = /^[A-Za-z0-9\s]+$/;
        const addressRegex = /^\d+\s[A-Za-z\s]+$/;
        const postcodeRegex = /^(G1|G2|G3|G4|G5|G11|G12|G13|G14|G15|G20|G21|G22|G23|G31|G32|G33|G34|G40|G41|G42|G43|G44|G45|G46|G51|G52|G53|G61|G62|G64|G65|G66|G67|G68|G69|G70)$/;

        if (!nameRegex.test(name)) {
            alert("Invalid accommodation name. Only letters and numbers are allowed.");
            return false;
        }

        if (!addressRegex.test(address)) {
            alert("Invalid address. It must start with a number followed by a street name.");
            return false;
        }

        if (!postcodeRegex.test(postcode)) {
            alert("Invalid postcode. Only enter the first part of a Glasgow postcode (e.g., G1, G12).");
            return false;
        }

        return true;
    }


    /**
     * Handles form submission to update accommodation details
     */
    document.getElementById('save-changes-btn').addEventListener('click', function() {
        if (!validateForm()) {
            return;
        }

        const form = document.getElementById('accom-info-form');
        const formData = new FormData(form);

        fetch(updateAccommodationUrl, {
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
                throw new Error(body.error || `Unknown error (HTTP ${status})`);
            }

            if (body.success) {
                alert('Accommodation updated successfully!');
                window.location.reload();
            } else {
                throw new Error(body.error || 'Unknown error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred: ' + error.message);
        });
    });
    
    /**
     * Handles accommodation deletion confirmation and execution
     */
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
    /**
     * Sets the selected image as the main image for the accommodation
     */
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
    /**
     * Deletes an image after user confirmation
     */
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
    /**
    * Retrieves a cookie value by name
    * @param {string} name - The name of the cookie to retrieve
    * @returns {string|null} - The value of the cookie or null if not found
    */
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