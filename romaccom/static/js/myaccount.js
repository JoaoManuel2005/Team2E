document.addEventListener('DOMContentLoaded', function() {
    // Privacy toggle functionality
    const privacyToggle = document.getElementById('privacy-toggle');
    if (!privacyToggle) {
        console.error("Privacy toggle not found.");
    } else {
        const updatePrivacyUrl = privacyToggle.getAttribute('data-privacy-url');
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        privacyToggle.addEventListener('change', function() {
            fetch(updatePrivacyUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
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
    }

    // Account deletion functionality
    const deleteAccountBtn = document.querySelector('.btn-delete');
    if (deleteAccountBtn) {
        // Create confirmation modal
        const modal = document.createElement('div');
        modal.className = 'delete-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h3>Delete Account</h3>
                <p>Are you sure you want to delete your account? This action cannot be undone.</p>
                <div class="modal-buttons">
                    <button class="modal-cancel">Cancel</button>
                    <button class="modal-confirm">Delete Account</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        // Show modal when delete button is clicked
        deleteAccountBtn.addEventListener('click', function(e) {
            e.preventDefault();
            modal.style.display = 'flex';
        });

        // Handle modal button clicks
        modal.addEventListener('click', function(e) {
            if (e.target.classList.contains('modal-cancel')) {
                modal.style.display = 'none';
            } else if (e.target.classList.contains('modal-confirm')) {
                deleteAccount();
            }
        });

        // Function to handle account deletion
        function deleteAccount() {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch("/romaccom/user/myaccount/delete/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = data.redirect_url || '/';
                } else {
                    alert(data.error || 'Failed to delete account');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while deleting your account');
            });
        }
    }
});
