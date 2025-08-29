// Modern JavaScript for Droid Rooter Website
// Enhanced with error handling, performance optimizations, and accessibility features

document.addEventListener('DOMContentLoaded', function() {
    try {
        // Initialize all components
        initNavigation();
        initAnimations();
        initSmoothScrolling();
        initPerformanceOptimizations();
        initAccessibilityFeatures();
        initBackToTop();
        initCookieConsent();
        
        console.log('✅ Droid Rooter website initialized successfully');
    } catch (error) {
        console.error('❌ Error initializing website:', error);
    }
});

// Navigation functionality with error handling
function initNavigation() {
    try {
        const navbar = document.querySelector('header');
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');
        
        if (!navbar) {
            console.warn('⚠️ Navbar element not found');
            return;
        }

        // Navbar scroll effect
        let ticking = false;
        function updateNavbar() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
                navbar.style.backgroundColor = 'rgba(31, 41, 55, 0.98)';
            } else {
                navbar.classList.remove('scrolled');
                navbar.style.backgroundColor = 'rgba(31, 41, 55, 0.95)';
            }
            ticking = false;
        }

        window.addEventListener('scroll', function() {
            if (!ticking) {
                requestAnimationFrame(updateNavbar);
                ticking = true;
            }
        });

        // Mobile menu functionality
        if (mobileMenuBtn && mobileMenu) {
            mobileMenuBtn.addEventListener('click', function() {
                try {
                    const isExpanded = mobileMenuBtn.getAttribute('aria-expanded') === 'true';
                    
                    mobileMenuBtn.setAttribute('aria-expanded', !isExpanded);
                    mobileMenuBtn.classList.toggle('active');
                    mobileMenu.classList.toggle('hidden');
                    
                    // Prevent body scroll when menu is open
                    document.body.style.overflow = isExpanded ? 'auto' : 'hidden';
                } catch (error) {
                    console.error('❌ Error toggling mobile menu:', error);
                }
            });

            // Close mobile menu when clicking on links
            const mobileLinks = mobileMenu.querySelectorAll('a');
            mobileLinks.forEach(link => {
                link.addEventListener('click', () => {
                    try {
                        mobileMenuBtn.setAttribute('aria-expanded', 'false');
                        mobileMenuBtn.classList.remove('active');
                        mobileMenu.classList.add('hidden');
                        document.body.style.overflow = 'auto';
                    } catch (error) {
                        console.error('❌ Error closing mobile menu:', error);
                    }
                });
            });

            // Close mobile menu on escape key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && !mobileMenu.classList.contains('hidden')) {
                    mobileMenuBtn.click();
                }
            });
        }

        console.log('✅ Navigation initialized');
    } catch (error) {
        console.error('❌ Error initializing navigation:', error);
    }
}

// Smooth scrolling for anchor links
function initSmoothScrolling() {
    try {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                try {
                    e.preventDefault();
                    
                    const targetId = this.getAttribute('href');
                    const targetSection = document.querySelector(targetId);
                    
                    if (targetSection) {
                        const offsetTop = targetSection.offsetTop - 80; // Account for fixed navbar
                        
                        window.scrollTo({
                            top: offsetTop,
                            behavior: 'smooth'
                        });

                        // Update focus for accessibility
                        targetSection.focus();
                    }
                } catch (error) {
                    console.error('❌ Error with smooth scrolling:', error);
                }
            });
        });

        console.log('✅ Smooth scrolling initialized');
    } catch (error) {
        console.error('❌ Error initializing smooth scrolling:', error);
    }
}

// Intersection Observer for animations
function initAnimations() {
    try {
        // Check if Intersection Observer is supported
        if (!('IntersectionObserver' in window)) {
            console.warn('⚠️ Intersection Observer not supported, skipping animations');
            return;
        }

        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                try {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('in-view');
                        
                        // Add staggered animation delay for multiple elements
                        const delay = Array.from(entry.target.parentNode.children).indexOf(entry.target) * 100;
                        entry.target.style.transitionDelay = `${delay}ms`;
                        
                        observer.unobserve(entry.target);
                    }
                } catch (error) {
                    console.error('❌ Error in intersection observer:', error);
                }
            });
        }, observerOptions);
        
        // Observe elements for animation
        const animateElements = document.querySelectorAll('.service-card, article, .text-center > div, section > div > div');
        animateElements.forEach(el => {
            el.classList.add('animate-on-scroll');
            observer.observe(el);
        });

        console.log(`✅ Animation observer initialized for ${animateElements.length} elements`);
    } catch (error) {
        console.error('❌ Error initializing animations:', error);
    }
}

// Performance optimizations
function initPerformanceOptimizations() {
    try {
        // Lazy loading for images (if any are added later)
        if ('loading' in HTMLImageElement.prototype) {
            const images = document.querySelectorAll('img[data-src]');
            images.forEach(img => {
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
            });
        } else {
            // Fallback for browsers that don't support native lazy loading
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }

        // Preload critical resources
        const criticalResources = [
            'css/style-modern.css'
        ];

        criticalResources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.href = resource;
            link.as = resource.endsWith('.css') ? 'style' : 'script';
            document.head.appendChild(link);
        });

        console.log('✅ Performance optimizations initialized');
    } catch (error) {
        console.error('❌ Error initializing performance optimizations:', error);
    }
}

// Accessibility features
function initAccessibilityFeatures() {
    try {
        // Skip link functionality
        const skipLink = document.querySelector('.skip-link');
        if (skipLink) {
            skipLink.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.focus();
                    target.scrollIntoView();
                }
            });
        }

        // Keyboard navigation for service cards
        const serviceCards = document.querySelectorAll('.service-card');
        serviceCards.forEach(card => {
            card.setAttribute('tabindex', '0');
            card.setAttribute('role', 'button');
            
            card.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    // Add click behavior if needed
                    this.click();
                }
            });
        });

        // Announce page changes for screen readers
        const announcer = document.createElement('div');
        announcer.setAttribute('aria-live', 'polite');
        announcer.setAttribute('aria-atomic', 'true');
        announcer.className = 'sr-only';
        announcer.style.cssText = 'position: absolute; left: -10000px; width: 1px; height: 1px; overflow: hidden;';
        document.body.appendChild(announcer);

        // Store announcer globally for use in other functions
        window.announceToScreenReader = function(message) {
            announcer.textContent = message;
            setTimeout(() => {
                announcer.textContent = '';
            }, 1000);
        };

        console.log('✅ Accessibility features initialized');
    } catch (error) {
        console.error('❌ Error initializing accessibility features:', error);
    }
}

// Back to top button
function initBackToTop() {
    try {
        const backToTopBtn = document.createElement('button');
        backToTopBtn.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 19V5M5 12L12 5L19 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        `;
        backToTopBtn.className = 'fixed bottom-6 right-6 bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-full shadow-lg transition-all duration-300 transform hover:scale-110 z-50 opacity-0 pointer-events-none';
        backToTopBtn.setAttribute('aria-label', 'Back to top');
        backToTopBtn.setAttribute('title', 'Back to top');
        
        document.body.appendChild(backToTopBtn);
        
        // Show/hide button based on scroll position
        let ticking = false;
        function updateBackToTop() {
            if (window.scrollY > 300) {
                backToTopBtn.style.opacity = '1';
                backToTopBtn.style.pointerEvents = 'auto';
            } else {
                backToTopBtn.style.opacity = '0';
                backToTopBtn.style.pointerEvents = 'none';
            }
            ticking = false;
        }

        window.addEventListener('scroll', function() {
            if (!ticking) {
                requestAnimationFrame(updateBackToTop);
                ticking = true;
            }
        });
        
        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
            
            // Announce to screen readers
            if (window.announceToScreenReader) {
                window.announceToScreenReader('Scrolled to top of page');
            }
        });

        console.log('✅ Back to top button initialized');
    } catch (error) {
        console.error('❌ Error initializing back to top button:', error);
    }
}

// Cookie consent (GDPR compliance)
function initCookieConsent() {
    try {
        const cookieConsent = localStorage.getItem('droidrooter_cookie_consent');
        
        if (!cookieConsent) {
            const consentBanner = document.createElement('div');
            consentBanner.className = 'fixed bottom-0 left-0 right-0 bg-gray-900 text-white p-4 shadow-lg z-50 transform translate-y-full transition-transform duration-300';
            consentBanner.setAttribute('role', 'dialog');
            consentBanner.setAttribute('aria-labelledby', 'cookie-title');
            consentBanner.setAttribute('aria-describedby', 'cookie-desc');
            
            consentBanner.innerHTML = `
                <div class="container mx-auto px-4">
                    <div class="flex flex-col md:flex-row items-center justify-between gap-4">
                        <div class="flex-1">
                            <h3 id="cookie-title" class="font-semibold mb-1">🍪 Cookie Notice</h3>
                            <p id="cookie-desc" class="text-sm text-gray-300">
                                We use cookies to enhance your experience and analyze site usage. By continuing to browse, you agree to our use of cookies.
                            </p>
                        </div>
                        <div class="flex gap-3">
                            <button id="accept-cookies" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors">
                                Accept
                            </button>
                            <button id="decline-cookies" class="border border-gray-600 hover:bg-gray-800 text-white px-6 py-2 rounded-lg font-medium transition-colors">
                                Decline
                            </button>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(consentBanner);
            
            // Show banner with animation
            setTimeout(() => {
                consentBanner.style.transform = 'translateY(0)';
            }, 1000);
            
            // Handle accept button
            document.getElementById('accept-cookies').addEventListener('click', function() {
                localStorage.setItem('droidrooter_cookie_consent', 'accepted');
                consentBanner.style.transform = 'translateY(100%)';
                setTimeout(() => {
                    consentBanner.remove();
                }, 300);
                
                if (window.announceToScreenReader) {
                    window.announceToScreenReader('Cookies accepted');
                }
            });
            
            // Handle decline button
            document.getElementById('decline-cookies').addEventListener('click', function() {
                localStorage.setItem('droidrooter_cookie_consent', 'declined');
                consentBanner.style.transform = 'translateY(100%)';
                setTimeout(() => {
                    consentBanner.remove();
                }, 300);
                
                if (window.announceToScreenReader) {
                    window.announceToScreenReader('Cookies declined');
                }
            });
        }

        console.log('✅ Cookie consent initialized');
    } catch (error) {
        console.error('❌ Error initializing cookie consent:', error);
    }
}

// Form handling (for future contact forms)
function initContactForm() {
    try {
        const contactForms = document.querySelectorAll('.contact-form');
        
        contactForms.forEach(form => {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                handleFormSubmission(this);
            });
        });

        console.log(`✅ Contact forms initialized (${contactForms.length} forms)`);
    } catch (error) {
        console.error('❌ Error initializing contact forms:', error);
    }
}

// Form submission handler with validation
function handleFormSubmission(form) {
    try {
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn ? submitBtn.textContent : '';
        
        // Basic form validation
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('border-red-500');
                field.setAttribute('aria-invalid', 'true');
            } else {
                field.classList.remove('border-red-500');
                field.setAttribute('aria-invalid', 'false');
            }
        });
        
        if (!isValid) {
            showNotification('Please fill in all required fields.', 'error');
            return;
        }
        
        // Show loading state
        if (submitBtn) {
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;
            submitBtn.classList.add('opacity-50');
        }
        
        // Simulate form submission (replace with actual implementation)
        setTimeout(() => {
            showNotification('Message sent successfully! We\'ll get back to you soon.', 'success');
            form.reset();
            
            if (submitBtn) {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                submitBtn.classList.remove('opacity-50');
            }
            
            if (window.announceToScreenReader) {
                window.announceToScreenReader('Form submitted successfully');
            }
        }, 2000);
        
    } catch (error) {
        console.error('❌ Error handling form submission:', error);
        showNotification('An error occurred. Please try again.', 'error');
    }
}

// Notification system
function showNotification(message, type = 'info') {
    try {
        const notification = document.createElement('div');
        const typeClasses = {
            success: 'bg-green-500 border-green-600',
            error: 'bg-red-500 border-red-600',
            warning: 'bg-yellow-500 border-yellow-600',
            info: 'bg-blue-500 border-blue-600'
        };
        
        notification.className = `fixed top-20 right-4 ${typeClasses[type]} text-white p-4 rounded-lg shadow-lg z-50 max-w-sm transform translate-x-full transition-transform duration-300`;
        notification.setAttribute('role', 'alert');
        notification.setAttribute('aria-live', 'assertive');
        
        notification.innerHTML = `
            <div class="flex items-center justify-between">
                <span>${message}</span>
                <button class="ml-4 text-white hover:text-gray-200 transition-colors" aria-label="Close notification">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Auto remove after 5 seconds
        const autoRemove = setTimeout(() => {
            removeNotification(notification);
        }, 5000);
        
        // Manual close button
        const closeBtn = notification.querySelector('button');
        closeBtn.addEventListener('click', () => {
            clearTimeout(autoRemove);
            removeNotification(notification);
        });
        
        function removeNotification(notif) {
            notif.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notif.parentNode) {
                    notif.remove();
                }
            }, 300);
        }
        
    } catch (error) {
        console.error('❌ Error showing notification:', error);
    }
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Error handling for unhandled errors
window.addEventListener('error', function(e) {
    console.error('❌ Unhandled error:', e.error);
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('❌ Unhandled promise rejection:', e.reason);
});

// Make showNotification globally available
window.showNotification = showNotification;

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initNavigation,
        initAnimations,
        initSmoothScrolling,
        showNotification,
        debounce,
        throttle
    };
}

console.log('🚀 Droid Rooter Modern JavaScript loaded');
