document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.querySelector("#search-input");
    const postcodeDropdown = document.querySelector("#postcode-select");
    const suggestionsContainer = document.querySelector("#search-suggestions");
    const searchForm = document.querySelector("#search-form");
    let debounceTimer;

    // Get the search URL from the data attribute in home.html
    const searchUrl = searchInput.getAttribute("data-search-url");

    // Function to fetch random suggestions when search is focused without text
    function fetchRandomSuggestions() {
        // Add a random parameter to indicate we want random results
        const url = `${searchUrl}?query=&postcode=&random=true`;

        fetch(url, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.html) {
                const parser = new DOMParser();
                const doc = parser.parseFromString(data.html, 'text/html');
                const accomItems = doc.querySelectorAll('.accommodation-card');
                
                suggestionsContainer.innerHTML = '';
                
                // Show header for initial suggestions
                const suggestionHeader = document.createElement('div');
                suggestionHeader.className = 'suggestion-header';
                suggestionHeader.innerHTML = 'You might like:';
                suggestionsContainer.appendChild(suggestionHeader);

                // Take first 5 items or fewer if less available
                const itemsToShow = Math.min(accomItems.length, 5);
                for (let i = 0; i < itemsToShow; i++) {
                    const item = accomItems[i];
                    const accomName = item.querySelector('.accom-name a').textContent;
                    const accomLink = item.querySelector('.accom-name a').getAttribute('href');

                    const suggestionItem = document.createElement('div');
                    suggestionItem.className = 'suggestion-item';
                    
                    suggestionItem.innerHTML = `
                        <span class="suggestion-icon material-icons">apartment</span>
                        <span class="suggestion-text">${accomName}</span>
                    `;

                    suggestionItem.addEventListener('click', (e) => {
                        e.preventDefault();
                        window.location.href = accomLink;
                    });

                    suggestionsContainer.appendChild(suggestionItem);
                }
                
                suggestionsContainer.classList.add("active");
            }
        })
        .catch(error => console.error("Error fetching random suggestions:", error));
    }

    // Function to fetch and display suggestions
    function fetchSuggestions() {
        clearTimeout(debounceTimer);

        debounceTimer = setTimeout(() => {
            const query = searchInput.value.trim();
            if (query.length < 1) {
                // When query is empty, show random suggestions instead
                fetchRandomSuggestions();
                return;
            }

            const postcode = postcodeDropdown.value;
            const url = `${searchUrl}?query=${encodeURIComponent(query)}&postcode=${encodeURIComponent(postcode)}`;

            fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(response => response.json())
            .then(data => {
                if (data.html) {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(data.html, 'text/html');
                    const accomItems = doc.querySelectorAll('.accommodation-card');

                    suggestionsContainer.innerHTML = '';

                    if (accomItems.length > 0) {
                        accomItems.forEach(item => {
                            const accomName = item.querySelector('.accom-name a').textContent;
                            const accomLink = item.querySelector('.accom-name a').getAttribute('href');

                            const suggestionItem = document.createElement('div');
                            suggestionItem.className = 'suggestion-item';

                            const regex = new RegExp(`(${query})`, 'gi');
                            const highlightedName = accomName.replace(
                                regex, 
                                '<span class="suggestion-highlight">$1</span>'
                            );

                            suggestionItem.innerHTML = `
                                <span class="suggestion-icon material-icons">apartment</span>
                                <span class="suggestion-text">${highlightedName}</span>
                            `;

                            suggestionItem.addEventListener('click', (e) => {
                                e.preventDefault();
                                window.location.href = accomLink;
                            });

                            suggestionsContainer.appendChild(suggestionItem);
                        });

                        suggestionsContainer.classList.add("active");
                    } else {
                        const noResults = document.createElement('div');
                        noResults.className = 'suggestion-item';
                        noResults.innerHTML = `
                            <span class="suggestion-icon material-icons">search_off</span>
                            <span class="suggestion-text">No results found for "${query}"</span>
                        `;
                        suggestionsContainer.appendChild(noResults);
                        suggestionsContainer.classList.add("active");
                    }
                }
            })
            .catch(error => console.error("Error fetching search suggestions:", error));
        }, 300); // 300ms debounce delay
    }

    // Event listeners
    searchInput.addEventListener("input", fetchSuggestions);
    postcodeDropdown.addEventListener("change", fetchSuggestions);

    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
            suggestionsContainer.classList.remove('active');
        }
    });

    // Show suggestions immediately on focus, even if empty
    searchInput.addEventListener('focus', function() {
        if (searchInput.value.trim().length > 0) {
            fetchSuggestions();
        } else {
            fetchRandomSuggestions();
        }
    });

    searchForm.addEventListener('submit', function(e) {
        const query = searchInput.value.trim();
        if (query.length < 1) {
            e.preventDefault();
        }
    });
});
