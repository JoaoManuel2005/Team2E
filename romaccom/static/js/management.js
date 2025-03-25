document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('confirm-modal');
    const modalClose = document.getElementById('modal-close');
    const cancelDelete = document.getElementById('cancel-delete');
    const confirmDelete = document.getElementById('confirm-delete');
    const accommodationNameElement = document.getElementById('accommodation-name');
    
    let currentAccommodationId = null;

    if (modal) {
        modal.style.display = 'none';
    }
    /**
     * Opens confirmation modal for deleting an accommodation
     */
    document.querySelectorAll('.delete-accommodation').forEach(button => {
        button.addEventListener('click', function() {
            const id = this.dataset.id;
            const name = this.dataset.name;
            
            currentAccommodationId = id;
            accommodationNameElement.textContent = name;
            modal.style.display = 'flex';
        });
    });
        
    /**
     * Closes the modal and resets the current accommodation ID
     */
    function closeModal() {
        modal.style.display = 'none';
        currentAccommodationId = null;
    }

    modalClose.addEventListener('click', closeModal);
    cancelDelete.addEventListener('click', closeModal);
    /**
     * Closes the modal when clicking outside of it.
     */
    modal.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModal();
        }
    });
    /**
     * Confirms deletion of an accommodation and sends a delete request to the API
     */
    confirmDelete.addEventListener('click', function() {
        if (currentAccommodationId) {
            fetch('/api/accommodation/delete/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    accommodation_id: currentAccommodationId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Reload the page to show updated list
                    window.location.reload();
                } else {
                    alert('Error: ' + (data.error || 'Unknown error occurred'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while trying to delete the accommodation.');
            })
            .finally(() => {
                closeModal();
            });
        }
    });

    /**
     * Account deletion modal handling
     */
    const deleteAccountBtn = document.getElementById('delete-account-btn');
    const confirmDeleteAccountModal = document.getElementById('confirm-delete-modal');
    const closeDeleteAccountModal = document.getElementById('close-delete-modal');
    const cancelDeleteAccount = document.getElementById('cancel-delete-account');
    const confirmDeleteAccount = document.getElementById('confirm-delete-account');

    if (confirmDeleteAccountModal) {
        confirmDeleteAccountModal.style.display = 'none';
    }

    if (deleteAccountBtn) {
        deleteAccountBtn.addEventListener('click', function() {
            confirmDeleteAccountModal.style.display = 'flex';
        });
    }

    if (closeDeleteAccountModal) {
        closeDeleteAccountModal.addEventListener('click', function() {
            confirmDeleteAccountModal.style.display = 'none';
        });
    }

    if (cancelDeleteAccount) {
        cancelDeleteAccount.addEventListener('click', function() {
            confirmDeleteAccountModal.style.display = 'none';
        });
    }
    /**
     * Sends a request to delete the user account
     */
    if (confirmDeleteAccount) {
        confirmDeleteAccount.addEventListener('click', function() {
            fetch('/romaccom/operator/delete-account/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Your account has been deleted.');
                    window.location.href = data.redirect_url;  // Redirect to homepage
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while deleting your account.');
            });
        });
    }
    /**
     * Retrieves a specific cookie by name
     * 
     * @param {string} name - The name of the cookie to retrieve
     * @returns {string|null} - The value of the cookie or null if not found
     */
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
});