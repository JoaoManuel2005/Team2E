document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const heroSection = document.getElementById('hero');
    const heroBackground = document.getElementById('hero-bg');
    const heroContent = document.getElementById('hero-content');
    const heroLogo = document.getElementById('hero-logo');
    const fixedHeader = document.getElementById('fixed-header');
    const scrollIndicator = document.getElementById('scroll-indicator');
    
    // Initial dimensions
    const initialLogoSize = 150; // px
    const finalLogoSize = 40; // px
    
    // Ensure scroll indicator is fully visible initially
    if (scrollIndicator) {
        // Force opacity to 1 and ensure it's visible
        scrollIndicator.style.opacity = '1';
        scrollIndicator.style.display = 'flex';
        
        // Add a pulsing effect after a short delay to draw attention
        setTimeout(() => {
            scrollIndicator.classList.add('active-pulse');
        }, 1500);
    }
    
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
      
      // Fade out scroll indicator
      if (scrollIndicator) {
        scrollIndicator.style.opacity = Math.max(0, 1 - (scrollProgress * 3));
        
        // Remove pulse effect once scrolling starts
        if (scrollProgress > 0.05) {
          scrollIndicator.classList.remove('active-pulse');
        }
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

    // Fix document height calculation
    function setPageHeight() {
        const mainContent = document.getElementById('main-content');
        if (mainContent) {
            // Get the actual content height
            const footerElement = document.querySelector('.footer');
            const footerHeight = footerElement ? footerElement.offsetHeight : 50;
            const heroHeight = window.innerHeight; // Hero is 100vh
            const mainContentHeight = mainContent.scrollHeight;
            
            // Set page height to precisely fit the content
            // No min-height, just the exact size needed
            document.body.style.height = (heroHeight + mainContentHeight + footerHeight) + 'px';
        }
    }
    
    // Apply height adjustment initially and on resize
    setPageHeight();
    window.addEventListener('resize', setPageHeight);
  });

