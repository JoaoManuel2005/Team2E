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
    
    // Open modal when delete button is clicked
    document.querySelectorAll('.delete-accommodation').forEach(button => {
        button.addEventListener('click', function() {
            const id = this.dataset.id;
            const name = this.dataset.name;
            
            currentAccommodationId = id;
            accommodationNameElement.textContent = name;
            modal.style.display = 'flex';
        });
    });
    
    // Close modal functions
    function closeModal() {
        modal.style.display = 'none';
        currentAccommodationId = null;
    }
    
    modalClose.addEventListener('click', closeModal);
    cancelDelete.addEventListener('click', closeModal);
    
    // Handle modal background click to close
    modal.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModal();
        }
    });
    
    // Confirm delete action
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

    const deleteAccountBtn = document.getElementById('delete-account-btn');
    const confirmDeleteAccountModal = document.getElementById('confirm-delete-modal');
    const closeDeleteAccountModal = document.getElementById('close-delete-modal');
    const cancelDeleteAccount = document.getElementById('cancel-delete-account');
    const confirmDeleteAccount = document.getElementById('confirm-delete-account');

    // Ensure account deletion modal is hidden on page load
    if (confirmDeleteAccountModal) {
        confirmDeleteAccountModal.style.display = 'none';
    }

    // Show confirmation modal for account deletion when button is clicked
    if (deleteAccountBtn) {
        deleteAccountBtn.addEventListener('click', function() {
            confirmDeleteAccountModal.style.display = 'flex';
        });
    }

    // Close modal for account deletion
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

    // Confirm delete operator account
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

    // Utility function to get CSRF token
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