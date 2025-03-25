document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.querySelector("#search-input");
    const postcodeDropdown = document.querySelector("#postcode-select");
    const suggestionsContainer = document.querySelector("#search-suggestions");
    const searchForm = document.querySelector("#search-form");
    let debounceTimer;

    const searchUrl = searchInput.getAttribute("data-search-url");

    /**
     * Fetches random accommodation suggestions when no query is provided
     */
    function fetchRandomSuggestions() {
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
                
                const suggestionHeader = document.createElement('div');
                suggestionHeader.className = 'suggestion-header';
                suggestionHeader.innerHTML = 'You might like:';
                suggestionsContainer.appendChild(suggestionHeader);

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

    /**
     * Fetches search suggestions based on user input with a debounce mechanism
     */
    function fetchSuggestions() {
        clearTimeout(debounceTimer);

        debounceTimer = setTimeout(() => {
            const query = searchInput.value.trim();
            if (query.length < 1) {
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
    /**
     * Event listener for user input in the search field
     */
    searchInput.addEventListener("input", fetchSuggestions);
    /**
     * Event listener for postcode dropdown selection changes
     */
    postcodeDropdown.addEventListener("change", fetchSuggestions);

    /**
     * Closes suggestions dropdown when clicking outside the search area
     */
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
            suggestionsContainer.classList.remove('active');
        }
    });

    /**
     * Fetches suggestions when the search input gains focus
     */
    searchInput.addEventListener('focus', function() {
        if (searchInput.value.trim().length > 0) {
            fetchSuggestions();
        } else {
            fetchRandomSuggestions();
        }
    });

    /**
     * Prevents search form submission if the input is empty
     */
    searchForm.addEventListener('submit', function(e) {
        const query = searchInput.value.trim();
        if (query.length < 1) {
            e.preventDefault();
        }
    });
});
