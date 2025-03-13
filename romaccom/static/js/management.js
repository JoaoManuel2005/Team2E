document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('confirm-modal');
    const modalClose = document.getElementById('modal-close');
    const cancelDelete = document.getElementById('cancel-delete');
    const confirmDelete = document.getElementById('confirm-delete');
    const accommodationNameElement = document.getElementById('accommodation-name');
    
    let currentAccommodationId = null;
    
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
});