document.addEventListener('DOMContentLoaded', function() {
    const heroSection = document.getElementById('hero');
    const heroBackground = document.getElementById('hero-bg');
    const heroContent = document.getElementById('hero-content');
    const heroLogo = document.getElementById('hero-logo');
    const fixedHeader = document.getElementById('fixed-header');
    const scrollIndicator = document.getElementById('scroll-indicator');
    
    const initialLogoSize = 150; // px
    const finalLogoSize = 40; // px
    
    /**
     * Displays the scroll indicator and applies a pulsing animation after a delay
     */
    if (scrollIndicator) {
        scrollIndicator.style.opacity = '1';
        scrollIndicator.style.display = 'flex';
        
        setTimeout(() => {
            scrollIndicator.classList.add('active-pulse');
        }, 1500);
    }

    /**
     * Handles the scroll effect for the hero section, background, logo size, and header visibility
     */
    window.addEventListener('scroll', function() {
      const scrollPosition = window.scrollY;
      const windowHeight = window.innerHeight;
      
      const scrollProgress = Math.min(1, scrollPosition / windowHeight);
      
      heroBackground.style.opacity = Math.max(0, 1 - (scrollProgress * 1.5));
      
      const scale = 1 - (scrollProgress * 0.3);
      const translateY = scrollPosition * 0.5; 
      heroContent.style.transform = `scale(${scale}) translateY(${translateY}px)`;
      heroContent.style.opacity = Math.max(0, 1 - (scrollProgress * 1.5));
      
      const currentLogoSize = initialLogoSize - ((initialLogoSize - finalLogoSize) * scrollProgress);
      heroLogo.style.width = `${currentLogoSize}px`;
      heroLogo.style.height = `${currentLogoSize}px`;
      
      if (scrollProgress > 0.2) {
        fixedHeader.classList.add('visible');
      } else {
        fixedHeader.classList.remove('visible');
      }
      
      if (scrollIndicator) {
        scrollIndicator.style.opacity = Math.max(0, 1 - (scrollProgress * 3));
        
        if (scrollProgress > 0.05) {
          scrollIndicator.classList.remove('active-pulse');
        }
      }
    });
    
    const searchInput = document.getElementById('search-input');
    const searchSuggestions = document.getElementById('search-suggestions');
    
    /**
     * Handles search input focus to display suggestions.
     */
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
    /**
     * Adjusts the page height dynamically to accommodate content, including hero and footer sections
     */
    function setPageHeight() {
        const mainContent = document.getElementById('main-content');
        if (mainContent) {
            const footerElement = document.querySelector('.footer');
            const footerHeight = footerElement ? footerElement.offsetHeight : 50;
            const heroHeight = window.innerHeight; // Hero is 100vh
            const mainContentHeight = mainContent.scrollHeight;
            
            document.body.style.height = (heroHeight + mainContentHeight + footerHeight) + 'px';
        }
    }
    
    setPageHeight();
    window.addEventListener('resize', setPageHeight);
  });

