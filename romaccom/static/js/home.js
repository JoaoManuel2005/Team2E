document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.querySelector("#search-input");
    const postcodeDropdown = document.querySelector("#postcode-select");
    const suggestionsContainer = document.querySelector("#search-suggestions");
    const searchForm = document.querySelector("#search-form");
    let debounceTimer;
    
    // Function to fetch and display suggestions
    function fetchSuggestions() {
        clearTimeout(debounceTimer);
        
        debounceTimer = setTimeout(() => {
            const query = searchInput.value.trim();
            if (query.length < 1) {
                suggestionsContainer.classList.remove("active");
                suggestionsContainer.innerHTML = "";
                return;
            }
            
            const postcode = postcodeDropdown.value;
            const url = "{% url 'search_results' %}?query=" + encodeURIComponent(query) + 
                        "&postcode=" + encodeURIComponent(postcode);
            
            fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(response => response.json())
            .then(data => {
                if (data.html) {
                    // Extract accommodation items from the HTML response
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(data.html, 'text/html');
                    const accomItems = doc.querySelectorAll('.accommodation-card');
                    
                    suggestionsContainer.innerHTML = '';
                    
                    if (accomItems.length > 0) {
                        accomItems.forEach(item => {
                            const accomName = item.querySelector('.accom-name a').textContent;
                            const accomLink = item.querySelector('.accom-name a').getAttribute('href');
                            
                            // Create a suggestion item with highlighted matching text
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
                        // Show "No results" message
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
    
    // Close suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
            suggestionsContainer.classList.remove('active');
        }
    });
    
    // Focus input, show suggestions again if there's content
    searchInput.addEventListener('focus', function() {
        if (searchInput.value.trim().length > 0) {
            fetchSuggestions();
        }
    });
    
    // Handle form submission
    searchForm.addEventListener('submit', function(e) {
        const query = searchInput.value.trim();
        if (query.length < 1) {
            e.preventDefault();
        }
    });
    
    // Handle keyboard navigation in suggestions
    searchInput.addEventListener('keydown', function(e) {
        const items = suggestionsContainer.querySelectorAll('.suggestion-item');
        if (!items.length) return;
        
        const active = suggestionsContainer.querySelector('.suggestion-item.active');
        
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            
            if (!active) {
                items[0].classList.add('active');
            } else {
                const next = [...items].indexOf(active) + 1;
                if (next < items.length) {
                    active.classList.remove('active');
                    items[next].classList.add('active');
                }
            }
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            
            if (active) {
                const prev = [...items].indexOf(active) - 1;
                active.classList.remove('active');
                if (prev >= 0) {
                    items[prev].classList.add('active');
                }
            }
        } else if (e.key === 'Enter' && active) {
            e.preventDefault();
            const link = active.getAttribute('data-link');
            if (link) {
                window.location.href = link;
            }
        } else if (e.key === 'Escape') {
            suggestionsContainer.classList.remove('active');
        }
    });
});