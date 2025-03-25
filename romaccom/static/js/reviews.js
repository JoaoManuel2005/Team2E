/**
 * Opens the image modal and displays the selected image
 * 
 * @param {string} imageUrl - The URL of the image to display in the modal
 */
function openImageModal(imageUrl) {
    document.getElementById('modalImage').src = imageUrl;
    document.getElementById('imageModal').style.display = 'flex';
    document.body.style.overflow = 'hidden'; // Prevent scrolling when modal is open
}

/**
 * Closes the image modal and restores scrolling on the page
 */
function closeImageModal() {
    document.getElementById('imageModal').style.display = 'none';
    document.body.style.overflow = 'auto'; // Restore scrolling
}

/**
 * Adds an event listener to close the modal when the user clicks outside the image
 */
document.getElementById('imageModal').addEventListener('click', function(event) {
    if (event.target === this) {
        closeImageModal();
    }
});

/**
 * Adds an event listener to close the modal when the Escape key is pressed
 */
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeImageModal();
    }
});