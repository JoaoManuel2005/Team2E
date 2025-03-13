document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners to all delete review buttons
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const reviewId = this.getAttribute('data-review-id');
            if (confirm('Are you sure you want to delete this review? This action cannot be undone.')) {
                deleteReview(reviewId);
            }
        });
    });
    
    function deleteReview(reviewId) {
        fetch('/delete_review/', {
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
                // Fade out and remove the review card from the DOM
                const reviewCard = document.querySelector(`.review-card[data-review-id="${reviewId}"]`);
                reviewCard.style.opacity = '0';
                setTimeout(() => {
                    reviewCard.remove();
                    
                    // If no reviews left, show a message
                    if (document.querySelectorAll('.review-card').length === 0) {
                        const reviewsList = document.querySelector('.reviews-list');
                        reviewsList.innerHTML = '<p class="no-reviews">You haven\'t written any reviews yet.</p>';
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