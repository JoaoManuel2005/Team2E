document.addEventListener('DOMContentLoaded', function() {
    // Edit Profile functionality
    const editProfileCard = document.getElementById('edit-profile-trigger');
    const editProfileModal = document.querySelector('.edit-profile-modal');
    const editProfileForm = document.getElementById('edit-profile-form');
    const cancelBtn = document.querySelector('.btn-cancel');
    
    if (editProfileCard && editProfileModal) {
        // Show modal when the entire card is clicked
        editProfileCard.addEventListener('click', function() {
            editProfileModal.style.display = 'flex';
        });

        // Hide modal when cancel button is clicked
        cancelBtn.addEventListener('click', function() {
            editProfileModal.style.display = 'none';
        });

        // Handle form submission
        editProfileForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData();
            formData.append('username', document.getElementById('username').value);
            
            const profilePicture = document.getElementById('profile-picture').files[0];
            if (profilePicture) {
                formData.append('profile_picture', profilePicture);
            }
            
            fetch('/romaccom/api/user/update-profile/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Update profile information on the page
                    if (data.username) {
                        document.querySelector('.profile-username').textContent = data.username;
                    }
                    if (data.profile_picture_url) {
                        const profileAvatar = document.querySelector('.profile-avatar');
                        if (profileAvatar.querySelector('img')) {
                            profileAvatar.querySelector('img').src = data.profile_picture_url;
                        } else {
                            const img = document.createElement('img');
                            img.src = data.profile_picture_url;
                            img.alt = 'Profile Picture';
                            profileAvatar.innerHTML = '';
                            profileAvatar.appendChild(img);
                        }
                    }
                    editProfileModal.style.display = 'none';
                    alert('Profile updated successfully');
                } else {
                    throw new Error(data.error || 'Failed to update profile');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert(error.message || 'An error occurred while updating your profile');
            });
        });
    }

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
