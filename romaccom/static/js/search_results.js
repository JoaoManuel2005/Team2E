// Update your JavaScript (keep existing AJAX functionality)
document.addEventListener("DOMContentLoaded", function() {
    const searchForm = document.getElementById("search-form");
    const queryInput = document.getElementById("query-input");
    const postcodeDropdown = document.getElementById("postcode-dropdown");
    const resultsContainer = document.querySelector(".results-list");
    
    // For AJAX updates
    function fetchResults() {
        let query = queryInput.value.trim();
        let postcode = postcodeDropdown.value;
        let url = "{% url 'search_results' %}?query=" + encodeURIComponent(query) + "&postcode=" + encodeURIComponent(postcode);

        fetch(url, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.html) {
                resultsContainer.innerHTML = data.html;
            }
        })
        .catch(error => console.error("Error fetching search results:", error));
    }

    // Trigger AJAX on input and change but add delay
    let debounceTimer;
    const debounceDelay = 300; // milliseconds
    
    queryInput.addEventListener("input", function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(fetchResults, debounceDelay);
    });
    
    postcodeDropdown.addEventListener("change", fetchResults);
    
    // Handle form submission
    searchForm.addEventListener("submit", function(e) {
        if (queryInput.value.trim().length < 1) {
            e.preventDefault();
        }
    });
});