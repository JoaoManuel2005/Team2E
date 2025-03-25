/**
 * Adds event listeners to all delete buttons
 * Prompts user for confirmation before deleting a review
 */
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const reviewId = this.getAttribute('data-review-id');
            if (confirm('Are you sure you want to delete this review? This action cannot be undone.')) {
                deleteReview(reviewId);
            }
        });
    });

    /**
     * Sends a request to delete a review by its ID
     * If successful, removes the review card from the page
     * 
     * @param {string} reviewId - The ID of the review to delete
     */
    function deleteReview(reviewId) {
        fetch('/romaccom/delete_review/', {
            method: 'POST',
            body: JSON.stringify({
                review_id: reviewId
            }),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const reviewCard = document.querySelector(`.review-card[data-review-id="${reviewId}"]`);
                reviewCard.style.opacity = '0';
                setTimeout(() => {
                    reviewCard.remove();
                    
                    if (document.querySelectorAll('.review-card').length === 0) {
                        const reviewsList = document.querySelector('.reviews-list');
                        reviewsList.innerHTML = '<div class="no-reviews"><p>You haven\'t written any reviews yet.</p><p>Share your experiences with accommodations and help other students make informed decisions!</p><a href="/" class="browse-btn"><span class="material-icons">search</span>Find your next accommodation</a></div>';
                    }
                }, 300);
            } else {
                alert('Error deleting review: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting the review.');
        });
    }

    /**
     * Retrieves the value of a specified cookie.
     * 
     * @param {string} name - The name of the cookie to retrieve
     * @returns {string|null} The value of the cookie, or null if not found
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