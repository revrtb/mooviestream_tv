/**
 * Main JavaScript file for Movie Streaming Website
 * This file contains all the JavaScript functionality for the website
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Movie Streaming Website JavaScript loaded');
    
    // Initialize components
    initializeNavigation();
    initializeMovieCards();
    initializeTrailerModals();
    initializeContactForm();
    initializeMovieCarousel();
    initializeInfiniteScroll();
    initializeHorizontalScroll();
    
    // Initialize lazy loading for images
    if ('loading' in HTMLImageElement.prototype) {
        const images = document.querySelectorAll('img[loading="lazy"]');
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    } else {
        // Fallback for browsers that don't support lazy loading
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/lazysizes/5.3.2/lazysizes.min.js';
        document.body.appendChild(script);
    }
});
/**
 * Initialize infinite scrolling for trending and popular pages
 */
function initializeInfiniteScroll() {
    const container = document.getElementById('infinite-scroll-container');
    
    if (!container) return; // Exit if container doesn't exist
    
    // Get movie grid early to avoid undefined reference
    const movieGrid = document.getElementById('movie-grid');
    if (!movieGrid) return; // Exit if movie grid doesn't exist
    
    // Get data attributes
    const pageType = container.dataset.pageType;
    const mediaType = container.dataset.mediaType;
    const timeWindow = container.dataset.timeWindow;
    const query = container.dataset.query;
    const genreId = container.dataset.genreId;
    let currentPage = parseInt(container.dataset.currentPage, 10) || 1;
    let hasMore = container.dataset.hasMore === 'true' || container.dataset.hasMore === true;
    let nextPage = parseInt(container.dataset.nextPage, 10);
    if (isNaN(nextPage) || nextPage < 1) nextPage = 2;
    
    // Track loaded item IDs to prevent duplicates
    const loadedItemIds = new Set();
    
    // Initialize the Set with IDs of items already on the page (from data-detail-href or a[href])
    const existingCards = movieGrid.querySelectorAll('.movie-card');
    
    function getIdFromCard(card) {
        const href = card.getAttribute('data-detail-href') || card.getAttribute('href') || (card.querySelector('a[href]') && card.querySelector('a[href]').getAttribute('href'));
        if (!href) return null;
        const matches = href.match(/\/(movie|tv|actor)\/(\d+)/);
        return matches && matches[2] ? matches[2] : null;
    }
    
    existingCards.forEach(card => {
        const id = getIdFromCard(card);
        if (id) loadedItemIds.add(id);
    });
    
    // Debug information about container data attributes
    console.log('Infinite Scroll Container Data Attributes:');
    console.log('Page Type:', pageType);
    console.log('Media Type:', mediaType);
    console.log('Current Page:', currentPage);
    console.log('Has More:', hasMore);
    console.log('Next Page:', nextPage);
    console.log('Time Window:', timeWindow);
    console.log('Query:', query);
    console.log('Genre ID:', genreId);
    
    // Flag to prevent multiple simultaneous requests
    let isLoading = false;
    
    // Get loading indicator
    const loadingIndicator = document.getElementById('loading-indicator');
    
    // Function to check if user has scrolled to the bottom
    function isScrolledToBottom() {
        return window.innerHeight + window.scrollY >= document.body.offsetHeight - 500;
    }
    
    // Function to load more content
    function loadMoreContent() {
        if (isLoading || !hasMore) return;
        
        isLoading = true;
        
        // Show loading indicator
        if (loadingIndicator) {
            loadingIndicator.style.display = 'block';
        }
        
        // Debug information
        console.log('Loading more content:');
        console.log('Page Type:', pageType);
        console.log('Media Type:', mediaType);
        console.log('Current Page:', currentPage);
        console.log('Next Page:', nextPage);
        console.log('Has More:', hasMore);
        
        // Construct URL based on page type
        let url;
        if (pageType === 'trending') {
            url = mediaType === 'tv' ? 
                `/tv/trending?page=${nextPage}&time_window=${timeWindow}&ajax=1` : 
                `/trending?page=${nextPage}&time_window=${timeWindow}&ajax=1`;
        } else if (pageType === 'popular') {
            url = mediaType === 'tv' ? 
                `/tv/popular?page=${nextPage}&ajax=1` : 
                `/popular?page=${nextPage}&ajax=1`;
        } else if (pageType === 'top_rated') {
            url = mediaType === 'tv' ? 
                `/tv/top_rated?page=${nextPage}&ajax=1` : 
                `/top_rated?page=${nextPage}&ajax=1`;
        } else if (pageType === 'recent') {
            url = mediaType === 'tv' ? 
                `/tv/recent?page=${nextPage}&ajax=1` : 
                `/recent?page=${nextPage}&ajax=1`;
        } else if (pageType === 'search') {
            if (mediaType === 'tv') {
                url = `/search/tv?query=${query}&page=${nextPage}&ajax=1`;
            } else if (mediaType === 'person') {
                url = `/search?query=${query}&media_type=person&page=${nextPage}&ajax=1`;
            } else if (mediaType === 'all') {
                url = `/search?query=${query}&media_type=all&page=${nextPage}&ajax=1`;
            } else {
                url = `/search?query=${query}&media_type=movie&page=${nextPage}&ajax=1`;
            }
        } else if (pageType === 'genre') {
            url = mediaType === 'tv' ? 
                `/tv/genre/${genreId}?page=${nextPage}&ajax=1` : 
                `/genre/${genreId}?page=${nextPage}&ajax=1`;
        }
        
        if (!url) {
            isLoading = false;
            if (loadingIndicator) loadingIndicator.style.display = 'none';
            return;
        }
        
        // Make AJAX request
        fetch(url)
            .then(response => {
                console.log('Response status:', response.status);
                return response.json();
            })
            .then(data => {
                // Debug AJAX response
                console.log('AJAX Response Data:', data);
                console.log('Has HTML:', !!data.html);
                console.log('Has Results:', !!data.results);
                console.log('Has More:', data.has_more);
                console.log('Next Page:', data.next_page);
                
                // Append new content
                if (movieGrid) {
                    // Check if we have HTML content or raw results
                    if (data.html) {
                        console.log('Using HTML content approach');
                        // Legacy approach - using pre-rendered HTML
                        const tempDiv = document.createElement('div');
                        tempDiv.innerHTML = data.html;
                        
                        // Get all movie cards from the response
                        const movieCards = tempDiv.querySelectorAll('.movie-card');
                        console.log('Found movie cards:', movieCards.length);
                        
                        let uniqueCardsCount = 0;
                        
                        // Append each movie card to the movie grid if it's not a duplicate
                        movieCards.forEach(card => {
                            const itemId = getIdFromCard(card);
                            if (itemId && !loadedItemIds.has(itemId)) {
                                movieGrid.appendChild(card);
                                loadedItemIds.add(itemId);
                                uniqueCardsCount++;
                            }
                        });
                        
                        console.log('Added unique movie cards:', uniqueCardsCount);
                    } else if (data.results) {
                        console.log('Using raw results approach');
                        console.log('Results count:', data.results.length);
                        
                        let uniqueItemsCount = 0;
                        
                        // New approach - create HTML from raw data
                        data.results.forEach(item => {
                            // Skip if this item has already been loaded
                            if (loadedItemIds.has(item.id.toString())) {
                                return;
                            }
                            
                            // Add this item's ID to the set of loaded items
                            loadedItemIds.add(item.id.toString());
                            uniqueItemsCount++;
                            
                            const movieCard = document.createElement('a');
                            movieCard.className = 'movie-card';
                            movieCard.setAttribute('tabindex', '0');
                            
                            // Determine the item's media type
                            const itemMediaType = item.media_type || mediaType;
                            
                            // Create HTML content based on media type
                            if (itemMediaType === 'person') {
                                movieCard.setAttribute('href', `/actor/${item.id}`);
                                movieCard.innerHTML = `
                                    <div class="movie-poster">
                                        ${item.profile_url ? 
                                            `<img src="${item.profile_url}" alt="${item.name} Photo">` : 
                                            '<div class="no-poster">No Photo Available</div>'}
                                    </div>
                                    <div class="movie-info">
                                        <h4>${item.name}</h4>
                                        ${item.known_for_titles && item.known_for_titles.length > 0 ? 
                                            `<p class="known-for">Known for: ${item.known_for_titles.join(', ')}</p>` : 
                                            ''}
                                    </div>
                                `;
                            } else if (itemMediaType === 'tv') {
                                movieCard.setAttribute('href', `/tv/${item.id}`);
                                movieCard.innerHTML = `
                                    <div class="movie-poster">
                                        ${item.poster_url ? 
                                            `<img src="${item.poster_url}" alt="${item.name} Poster">` : 
                                            '<div class="no-poster">No Poster Available</div>'}
                                    </div>
                                    <div class="movie-info">
                                        <h4>${item.name}</h4>
                                        <p class="movie-year">${item.first_air_date ? item.first_air_date.substring(0, 4) : 'N/A'}</p>
                                        <p class="movie-rating">
                                            <i class="fas fa-star"></i> ${Math.round(item.vote_average * 10) / 10}
                                        </p>
                                    </div>
                                `;
                            } else {
                                movieCard.setAttribute('href', `/movie/${item.id}`);
                                movieCard.innerHTML = `
                                    <div class="movie-poster">
                                        ${item.poster_url ? 
                                            `<img src="${item.poster_url}" alt="${item.title} Poster">` : 
                                            '<div class="no-poster">No Poster Available</div>'}
                                    </div>
                                    <div class="movie-info">
                                        <h4>${item.title}</h4>
                                        <p class="movie-year">${item.release_date ? item.release_date.substring(0, 4) : 'N/A'}</p>
                                        <p class="movie-rating">
                                            <i class="fas fa-star"></i> ${Math.round(item.vote_average * 10) / 10}
                                        </p>
                                    </div>
                                `;
                            }
                            
                            // Append to movie grid
                            movieGrid.appendChild(movieCard);
                        });
                        
                        console.log('Added unique items:', uniqueItemsCount);
                    }
                    
                    // Initialize movie cards for the new content
                    initializeMovieCards();
                }
                
                // Update data attributes
                currentPage = nextPage;
                hasMore = data.has_more === true || data.has_more === 'true';
                const nextPageVal = data.next_page;
                nextPage = (nextPageVal != null && nextPageVal !== '') ? parseInt(nextPageVal, 10) : 0;
                if (isNaN(nextPage)) nextPage = 0;
                
                container.dataset.currentPage = String(currentPage);
                container.dataset.hasMore = hasMore ? 'true' : 'false';
                container.dataset.nextPage = String(nextPage);
                
                // Hide loading indicator
                if (loadingIndicator) {
                    loadingIndicator.style.display = 'none';
                }
                
                isLoading = false;
            })
            .catch(error => {
                console.error('Error loading more content:', error);
                
                // Hide loading indicator
                if (loadingIndicator) {
                    loadingIndicator.style.display = 'none';
                }
                
                isLoading = false;
            });
    }
    
    // Add scroll event listener
    window.addEventListener('scroll', function() {
        if (isScrolledToBottom()) {
            console.log('Scrolled to bottom, loading more content...');
            loadMoreContent();
        }
    });
    
    // Also trigger when within 1000px of the bottom
    window.addEventListener('scroll', function() {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
            loadMoreContent();
        }
    });
}
/**
 * Initialize navigation components
 */
function initializeNavigation() {
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (mobileMenuToggle && mainNav) {
        mobileMenuToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
        });
    }
    
    // Dropdown menu toggle
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            this.parentNode.classList.toggle('active');
            
            // Close other dropdowns
            dropdownToggles.forEach(otherToggle => {
                if (otherToggle !== toggle) {
                    otherToggle.parentNode.classList.remove('active');
                }
            });
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown').forEach(dropdown => {
                dropdown.classList.remove('active');
            });
        }
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Adjust for header height
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Initialize movie card interactions
 */
function initializeMovieCards() {
    // Add hover effect for movie actions
    const movieCards = document.querySelectorAll('.movie-card');
    
    movieCards.forEach(card => {
        const poster = card.querySelector('.movie-poster');
        const actions = card.querySelector('.movie-actions');
        
        if (poster && actions) {
            // Touch device support
            poster.addEventListener('touchstart', function() {
                actions.style.opacity = '1';
            }, { passive: true });
            
            card.addEventListener('mouseleave', function() {
                actions.style.opacity = '';
            });
        }
    });
}

/**
 * Initialize trailer modal functionality
 */
function initializeTrailerModals() {
    const trailerBtn = document.querySelector('.btn-trailer');
    const trailerModal = document.getElementById('trailer-modal');
    const closeModal = document.querySelector('.close-modal');
    const trailerIframe = document.getElementById('trailer-iframe');
    
    if (trailerBtn && trailerModal && closeModal && trailerIframe) {
        trailerBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const trailerKey = this.getAttribute('data-trailer');
            
            if (trailerKey) {
                trailerIframe.src = `https://www.youtube.com/embed/${trailerKey}?autoplay=1`;
                trailerModal.style.display = 'block';
                document.body.style.overflow = 'hidden'; // Prevent scrolling
            } else {
                showNotification('No trailer available for this movie.', 'info');
            }
        });
        
        closeModal.addEventListener('click', function() {
            trailerModal.style.display = 'none';
            trailerIframe.src = '';
            document.body.style.overflow = ''; // Restore scrolling
        });
        
        window.addEventListener('click', function(e) {
            if (e.target === trailerModal) {
                trailerModal.style.display = 'none';
                trailerIframe.src = '';
                document.body.style.overflow = ''; // Restore scrolling
            }
        });
        
        // Close on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && trailerModal.style.display === 'block') {
                trailerModal.style.display = 'none';
                trailerIframe.src = '';
                document.body.style.overflow = ''; // Restore scrolling
            }
        });
    }
}

/**
 * Initialize horizontal scrolling with mouse wheel
 * This allows users to scroll horizontally in movie sliders using the mouse wheel
 */
function initializeHorizontalScroll() {
    const sliders = document.querySelectorAll('.movie-slider');
    
    sliders.forEach(slider => {
        slider.addEventListener('wheel', function(e) {
            // Prevent default vertical scrolling
            e.preventDefault();
            
            // Determine scroll amount (faster scroll with shift key)
            const scrollAmount = e.shiftKey ? e.deltaY * 3 : e.deltaY;
            
            // Scroll horizontally based on the vertical scroll amount
            this.scrollLeft += scrollAmount;
        }, { passive: false }); // passive: false is required to use preventDefault
    });
}

/**
 * Initialize contact form validation and submission
 */
function initializeContactForm() {
    const contactForm = document.querySelector('.contact-form form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Simple validation
            let isValid = true;
            const requiredFields = contactForm.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });
            
            // Email validation
            const emailField = contactForm.querySelector('input[type="email"]');
            if (emailField && emailField.value.trim()) {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(emailField.value)) {
                    isValid = false;
                    emailField.classList.add('error');
                    showNotification('Please enter a valid email address.', 'error');
                }
            }
            
            if (isValid) {
                // Get form data
                const formData = new FormData(contactForm);
                const formValues = Object.fromEntries(formData.entries());
                
                console.log('Form submitted with values:', formValues);
                
                // Here you would typically send the data to a server
                // For now, we'll just show a success message
                showNotification('Thank you for your message! We will get back to you soon.', 'success');
                
                // Reset the form
                contactForm.reset();
            } else {
                showNotification('Please fill in all required fields correctly.', 'error');
            }
        });
    }
}

/**
 * Display a notification to the user
 * @param {string} message - The message to display
 * @param {string} type - The type of notification (success, error, info)
 */
function showNotification(message, type = 'info') {
    // Remove any existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => {
        notification.remove();
    });
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    // Add to the DOM
    document.body.appendChild(notification);
    
    // Add close button functionality
    const closeButton = notification.querySelector('.notification-close');
    if (closeButton) {
        closeButton.addEventListener('click', function() {
            notification.remove();
        });
    }
    
    // Show the notification with animation
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300); // Wait for fade out animation
    }, 5000);
}

/**
 * Utility function to format a date
 * @param {string} dateString - The date string to format
 * @returns {string} The formatted date string
 */
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    
    return date.toLocaleDateString('en-US', options);
}

/**
 * Initialize movie carousel functionality
 */
function initializeMovieCarousel() {
    const carousel = document.querySelector('.movie-carousel');
    
    if (!carousel) return; // Exit if carousel doesn't exist on the page
    
    const slides = carousel.querySelectorAll('.carousel-slide');
    const prevBtn = carousel.querySelector('.carousel-prev');
    const nextBtn = carousel.querySelector('.carousel-next');
    const indicators = carousel.querySelectorAll('.carousel-indicator');
    const progressBars = carousel.querySelectorAll('.carousel-progress');
    
    if (!slides.length) return; // Exit if no slides
    
    let currentSlide = 0;
    let slideInterval;
    const intervalTime = 5000; // 5 seconds (unused: auto-rotation disabled)
    
    // Auto-rotation disabled: main trending area does not auto-change
    // startSlideInterval();
    
    // Function to start the auto-rotation interval (currently no-op: no auto-rotation)
    function startSlideInterval() {
        if (slideInterval) {
            clearInterval(slideInterval);
            slideInterval = null;
        }
        // Progress bar sync for current slide only (no timer)
        if (progressBars.length && progressBars[currentSlide]) {
            progressBars.forEach(progress => {
                const progressBar = progress.querySelector('.carousel-progress-bar');
                if (progressBar) {
                    progressBar.style.animation = 'none';
                    progressBar.style.width = '0';
                }
            });
            progressBars[currentSlide].classList.add('active');
            const bar = progressBars[currentSlide].querySelector('.carousel-progress-bar');
            if (bar) bar.style.width = '0';
        }
        // Do not set interval: carousel changes only on user action (arrows, indicators, keyboard, swipe)
        return;
    }
    
    // Function to go to a specific slide
    function goToSlide(slideIndex) {
        // Remove active class from current slide, indicator, and progress bar
        slides[currentSlide].classList.remove('active');
        if (indicators.length && indicators[currentSlide]) {
            indicators[currentSlide].classList.remove('active');
        }
        if (progressBars.length && progressBars[currentSlide]) {
            progressBars[currentSlide].classList.remove('active');
        }
        
        // Update current slide index
        currentSlide = slideIndex;
        
        // Add active class to new slide, indicator, and progress bar
        slides[currentSlide].classList.add('active');
        if (indicators.length && indicators[currentSlide]) {
            indicators[currentSlide].classList.add('active');
        }
        if (progressBars.length && progressBars[currentSlide]) {
            progressBars[currentSlide].classList.add('active');
        }
        
        // Reset animations for content elements
        resetContentAnimations(slides[currentSlide]);
        
        // Restart the interval
        startSlideInterval();
    }
    
    // Function to reset content animations for a slide
    function resetContentAnimations(slide) {
        if (!slide) return;
        
        const title = slide.querySelector('.carousel-title');
        const overview = slide.querySelector('.carousel-overview');
        const actions = slide.querySelector('.carousel-actions');
        
        if (title) {
            title.style.animation = 'none';
            title.offsetHeight; // Trigger reflow
            title.style.animation = 'titleFadeIn 1s ease-out forwards 0.5s';
        }
        
        if (overview) {
            overview.style.animation = 'none';
            overview.offsetHeight; // Trigger reflow
            overview.style.animation = 'overviewFadeIn 1s ease-out forwards 0.7s';
        }
        
        if (actions) {
            actions.style.animation = 'none';
            actions.offsetHeight; // Trigger reflow
            actions.style.animation = 'actionsFadeIn 1s ease-out forwards 0.9s';
        }
    }
    
    // Event listeners for navigation arrows
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            const prevSlide = (currentSlide - 1 + slides.length) % slides.length;
            goToSlide(prevSlide);
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            const nextSlide = (currentSlide + 1) % slides.length;
            goToSlide(nextSlide);
        });
    }
    
    // Event listeners for indicators
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            goToSlide(index);
        });
    });
    
    // Event listeners for progress bars
    progressBars.forEach((progress, index) => {
        progress.addEventListener('click', () => {
            goToSlide(index);
        });
    });
    
    // Pause auto-rotation when hovering over the carousel
    carousel.addEventListener('mouseenter', () => {
        clearInterval(slideInterval);
        
        // Pause progress bar animation
        if (progressBars.length && progressBars[currentSlide]) {
            const progressBar = progressBars[currentSlide].querySelector('.carousel-progress-bar');
            if (progressBar) {
                const computedStyle = window.getComputedStyle(progressBar);
                const width = computedStyle.getPropertyValue('width');
                progressBar.style.animation = 'none';
                progressBar.style.width = width;
            }
        }
    });
    
    // Resume auto-rotation when mouse leaves the carousel
    carousel.addEventListener('mouseleave', () => {
        // Calculate remaining time based on progress bar width
        let remainingTime = intervalTime;
        if (progressBars.length && progressBars[currentSlide]) {
            const progressBar = progressBars[currentSlide].querySelector('.carousel-progress-bar');
            if (progressBar) {
                const computedStyle = window.getComputedStyle(progressBar);
                const width = parseFloat(computedStyle.getPropertyValue('width'));
                const totalWidth = parseFloat(window.getComputedStyle(progressBars[currentSlide]).getPropertyValue('width'));
                const progress = width / totalWidth;
                remainingTime = intervalTime * (1 - progress);
                
                // Resume animation from current position
                progressBar.style.animation = `progressAnimation ${remainingTime}ms linear forwards`;
            }
        }
        
        // Set interval with remaining time
        slideInterval = setTimeout(() => {
            goToSlide((currentSlide + 1) % slides.length);
            // After this first timeout, restart normal interval
            startSlideInterval();
        }, remainingTime);
    });
    
    // Touch events for mobile swipe
    let touchStartX = 0;
    let touchEndX = 0;
    
    carousel.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
        clearInterval(slideInterval); // Pause auto-rotation on touch
        
        // Pause progress bar animation
        if (progressBars.length && progressBars[currentSlide]) {
            const progressBar = progressBars[currentSlide].querySelector('.carousel-progress-bar');
            if (progressBar) {
                const computedStyle = window.getComputedStyle(progressBar);
                const width = computedStyle.getPropertyValue('width');
                progressBar.style.animation = 'none';
                progressBar.style.width = width;
            }
        }
    }, { passive: true });
    
    carousel.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
        startSlideInterval(); // Resume auto-rotation after touch
    }, { passive: true });
    
    function handleSwipe() {
        const swipeThreshold = 50; // Minimum distance for a swipe
        
        if (touchEndX < touchStartX - swipeThreshold) {
            // Swipe left - go to next slide
            const nextSlide = (currentSlide + 1) % slides.length;
            goToSlide(nextSlide);
        } else if (touchEndX > touchStartX + swipeThreshold) {
            // Swipe right - go to previous slide
            const prevSlide = (currentSlide - 1 + slides.length) % slides.length;
            goToSlide(prevSlide);
        }
    }
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        // Only handle keyboard navigation when carousel is in viewport
        const rect = carousel.getBoundingClientRect();
        const isInViewport = (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
        
        if (!isInViewport) return;
        
        if (e.key === 'ArrowLeft') {
            const prevSlide = (currentSlide - 1 + slides.length) % slides.length;
            goToSlide(prevSlide);
        } else if (e.key === 'ArrowRight') {
            const nextSlide = (currentSlide + 1) % slides.length;
            goToSlide(nextSlide);
        }
    });
}