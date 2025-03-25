document.addEventListener("DOMContentLoaded", function() {
    const searchForm = document.getElementById("search-form");
    const queryInput = document.getElementById("query-input");
    const postcodeDropdown = document.getElementById("postcode-dropdown");
    const resultsContainer = document.querySelector(".results-list");

    const searchUrl = searchForm.getAttribute("data-search-url");

    /**
     * Fetches search results from the server based on user input
     * Constructs a search query using the input value and selected postcode,
     * then updates the results container with the returned HTML
     */
    function fetchResults() {
        let query = queryInput.value.trim();
        let postcode = postcodeDropdown.value;
        let url = `${searchUrl}?query=${encodeURIComponent(query)}&postcode=${encodeURIComponent(postcode)}`;

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

    let debounceTimer;
    const debounceDelay = 300; // milliseconds

    /**
     * Listens for input in the search field and triggers the search with debouncing
     * This prevents excessive API calls while typing
     */
    queryInput.addEventListener("input", function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(fetchResults, debounceDelay);
    });

    /**
     * Triggers a new search when the postcode dropdown value changes
     */
    postcodeDropdown.addEventListener("change", fetchResults);

    /**
     * Prevents form submission if the search query is empty
     * Ensures users do not submit blank searches
     */
    searchForm.addEventListener("submit", function(e) {
        if (queryInput.value.trim().length < 1) {
            e.preventDefault();
        }
    });
});
