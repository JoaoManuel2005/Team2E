document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const heroSection = document.getElementById('hero');
    const heroBackground = document.getElementById('hero-bg');
    const heroContent = document.getElementById('hero-content');
    const heroLogo = document.getElementById('hero-logo');
    const fixedHeader = document.getElementById('fixed-header');
    
    // Initial dimensions
    const initialLogoSize = 150; // px
    const finalLogoSize = 40; // px
    
    // Handle scroll events
    window.addEventListener('scroll', function() {
      const scrollPosition = window.scrollY;
      const windowHeight = window.innerHeight;
      
      // Calculate scroll progress (0 to 1)
      const scrollProgress = Math.min(1, scrollPosition / windowHeight);
      
      // Fade out hero background
      heroBackground.style.opacity = Math.max(0, 1 - (scrollProgress * 1.5));
      
      // Transform hero content (scale down and move up with scroll)
      const scale = 1 - (scrollProgress * 0.3);
      const translateY = scrollPosition * 0.5; // Move slower than scroll
      heroContent.style.transform = `scale(${scale}) translateY(${translateY}px)`;
      heroContent.style.opacity = Math.max(0, 1 - (scrollProgress * 1.5));
      
      // Resize logo
      const currentLogoSize = initialLogoSize - ((initialLogoSize - finalLogoSize) * scrollProgress);
      heroLogo.style.width = `${currentLogoSize}px`;
      heroLogo.style.height = `${currentLogoSize}px`;
      
      // Show/hide fixed header
      if (scrollProgress > 0.2) {
        fixedHeader.classList.add('visible');
      } else {
        fixedHeader.classList.remove('visible');
      }
    });
    
    // Search suggestions functionality
    const searchInput = document.getElementById('search-input');
    const searchSuggestions = document.getElementById('search-suggestions');
    
    if (searchInput && searchSuggestions) {
      searchInput.addEventListener('focus', function() {
        searchSuggestions.classList.add('active');
      });
      
      document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchSuggestions.contains(e.target)) {
          searchSuggestions.classList.remove('active');
        }
      });
    }
  });

// Limit scrolling to prevent empty space at bottom
document.addEventListener('DOMContentLoaded', function() {
    const mainContent = document.getElementById('main-content');
    
    if (mainContent) {
      // Calculate the maximum scrollable height
      const setScrollLimit = () => {
        const viewportHeight = window.innerHeight;
        const contentTop = parseFloat(getComputedStyle(mainContent).marginTop);
        const contentHeight = mainContent.scrollHeight;
        const footerHeight = 50; // Approximate footer height
        
        // Set document height to exactly match content
        document.body.style.height = (contentTop + contentHeight + footerHeight) + 'px';
      };
      
      // Apply initially and on window resize
      setScrollLimit();
      window.addEventListener('resize', setScrollLimit);
    }
  });

