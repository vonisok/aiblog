/**
 * AI Blog Theme JavaScript
 * Handles dark mode, mobile menu, reading progress, and other interactive features
 */

class BlogTheme {
    constructor() {
        this.init();
    }

    init() {
        this.initDarkMode();
        this.initMobileMenu();
        this.initReadingProgress();
        this.initScrollToTop();
    }

    /**
     * Dark Mode Toggle
     */
    initDarkMode() {
        const themeToggle = document.getElementById('theme-toggle');
        const mobileThemeToggle = document.getElementById('mobile-theme-toggle');
        const darkIcon = document.getElementById('theme-toggle-dark-icon');
        const lightIcon = document.getElementById('theme-toggle-light-icon');

        // Set initial theme icons based on current state
        this.updateThemeIcons();

        // Toggle theme on button click
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        }

        if (mobileThemeToggle) {
            mobileThemeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        }

        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                this.setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    setTheme(theme) {
        const html = document.documentElement;

        if (theme === 'dark') {
            html.classList.add('dark');
        } else {
            html.classList.remove('dark');
        }

        localStorage.setItem('theme', theme);
        this.updateThemeIcons();
    }

    updateThemeIcons() {
        const darkIcon = document.getElementById('theme-toggle-dark-icon');
        const lightIcon = document.getElementById('theme-toggle-light-icon');
        const isDark = document.documentElement.classList.contains('dark');

        if (isDark) {
            if (darkIcon) darkIcon.classList.add('hidden');
            if (lightIcon) lightIcon.classList.remove('hidden');
        } else {
            if (darkIcon) darkIcon.classList.remove('hidden');
            if (lightIcon) lightIcon.classList.add('hidden');
        }
    }

    toggleTheme() {
        const currentTheme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
        this.setTheme(currentTheme === 'dark' ? 'light' : 'dark');
    }

    /**
     * Mobile Menu Toggle
     */
    initMobileMenu() {
        const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
        const mobileMenu = document.getElementById('mobile-menu');
        const openIcon = document.getElementById('mobile-menu-open');
        const closeIcon = document.getElementById('mobile-menu-close');

        if (mobileMenuToggle && mobileMenu) {
            mobileMenuToggle.addEventListener('click', () => {
                const isHidden = mobileMenu.classList.contains('hidden');
                
                if (isHidden) {
                    mobileMenu.classList.remove('hidden');
                    openIcon?.classList.add('hidden');
                    closeIcon?.classList.remove('hidden');
                } else {
                    mobileMenu.classList.add('hidden');
                    openIcon?.classList.remove('hidden');
                    closeIcon?.classList.add('hidden');
                }
            });

            // Close mobile menu when clicking outside
            document.addEventListener('click', (e) => {
                if (!mobileMenuToggle.contains(e.target) && !mobileMenu.contains(e.target)) {
                    mobileMenu.classList.add('hidden');
                    openIcon?.classList.remove('hidden');
                    closeIcon?.classList.add('hidden');
                }
            });
        }
    }

    /**
     * Reading Progress Bar
     */
    initReadingProgress() {
        const progressBar = document.querySelector('.reading-progress');
        
        if (progressBar) {
            const updateProgress = () => {
                const article = document.querySelector('article');
                if (!article) return;

                const articleTop = article.offsetTop;
                const articleHeight = article.offsetHeight;
                const windowHeight = window.innerHeight;
                const scrollTop = window.pageYOffset;

                const startReading = articleTop - windowHeight / 3;
                const finishReading = articleTop + articleHeight - windowHeight / 3;
                const totalReadingArea = finishReading - startReading;

                if (scrollTop < startReading) {
                    progressBar.style.width = '0%';
                } else if (scrollTop > finishReading) {
                    progressBar.style.width = '100%';
                } else {
                    const progress = ((scrollTop - startReading) / totalReadingArea) * 100;
                    progressBar.style.width = `${Math.min(100, Math.max(0, progress))}%`;
                }
            };

            window.addEventListener('scroll', updateProgress);
            window.addEventListener('resize', updateProgress);
            updateProgress(); // Initial call
        }
    }

    /**
     * Scroll to Top Button
     */
    initScrollToTop() {
        // Create scroll to top button
        const scrollButton = document.createElement('button');
        scrollButton.innerHTML = `
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"></path>
            </svg>
        `;
        scrollButton.className = 'fixed bottom-6 right-6 z-50 p-3 bg-primary-600 hover:bg-primary-700 text-white rounded-full shadow-lg transition-all duration-300 opacity-0 translate-y-4 pointer-events-none';
        scrollButton.setAttribute('aria-label', 'Scroll to top');
        document.body.appendChild(scrollButton);

        const toggleScrollButton = () => {
            if (window.pageYOffset > 300) {
                scrollButton.classList.remove('opacity-0', 'translate-y-4', 'pointer-events-none');
            } else {
                scrollButton.classList.add('opacity-0', 'translate-y-4', 'pointer-events-none');
            }
        };

        scrollButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        window.addEventListener('scroll', toggleScrollButton);
    }
}

/**
 * Utility Functions
 */

// Copy to clipboard function
window.copyToClipboard = function(text) {
    navigator.clipboard.writeText(text).then(function() {
        // Show temporary feedback
        const button = event.target.closest('button');
        if (button) {
            const originalHTML = button.innerHTML;
            button.innerHTML = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>';
            setTimeout(() => {
                button.innerHTML = originalHTML;
            }, 2000);
        }
    }).catch(function() {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
    });
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new BlogTheme();
});

// Performance monitoring
if ('PerformanceObserver' in window) {
    // Monitor Largest Contentful Paint
    const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        console.log('LCP:', lastEntry.startTime);
    });
    observer.observe({ entryTypes: ['largest-contentful-paint'] });
}
