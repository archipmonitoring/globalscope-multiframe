// HoloMesh Accessibility Utilities
// Provides accessibility enhancements for better WCAG 2.1 compliance

class HoloMeshAccessibility {
    constructor() {
        this.init();
    }
    
    init() {
        // Initialize accessibility features
        this.setupKeyboardNavigation();
        this.setupFocusManagement();
        this.setupReducedMotion();
        this.setupHighContrast();
        this.setupSkipLinks();
    }
    
    // Setup keyboard navigation enhancements
    setupKeyboardNavigation() {
        // Ensure all interactive elements are keyboard accessible
        document.addEventListener('keydown', (e) => {
            // Handle custom keyboard shortcuts
            if (e.altKey && e.key === '1') {
                // Alt+1 - Focus on main content
                const mainContent = document.getElementById('main-content');
                if (mainContent) {
                    mainContent.focus();
                    e.preventDefault();
                }
            }
            
            if (e.altKey && e.key === '2') {
                // Alt+2 - Focus on navigation
                const nav = document.querySelector('nav');
                if (nav) {
                    nav.focus();
                    e.preventDefault();
                }
            }
        });
    }
    
    // Setup focus management
    setupFocusManagement() {
        // Add focus visible class to body when tab is pressed
        let tabPressed = false;
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                tabPressed = true;
                document.body.classList.add('user-is-tabbing');
            }
        });
        
        document.addEventListener('mousedown', () => {
            tabPressed = false;
            document.body.classList.remove('user-is-tabbing');
        });
        
        // Ensure focus is visible on all focusable elements
        const focusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
        
        document.addEventListener('focusin', (e) => {
            if (tabPressed && e.target.matches(focusableElements)) {
                e.target.classList.add('keyboard-focused');
            }
        });
        
        document.addEventListener('focusout', (e) => {
            e.target.classList.remove('keyboard-focused');
        });
    }
    
    // Setup reduced motion support
    setupReducedMotion() {
        const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
        
        const handleReducedMotion = (e) => {
            if (e.matches) {
                document.body.classList.add('reduced-motion');
                // Disable animations
                this.disableAnimations();
            } else {
                document.body.classList.remove('reduced-motion');
                // Enable animations
                this.enableAnimations();
            }
        };
        
        // Initial check
        handleReducedMotion(mediaQuery);
        
        // Listen for changes
        mediaQuery.addListener(handleReducedMotion);
    }
    
    // Disable animations for reduced motion
    disableAnimations() {
        const style = document.createElement('style');
        style.textContent = `
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
            .pulse, .pulse-animation {
                animation: none !important;
            }
        `;
        document.head.appendChild(style);
    }
    
    // Enable animations
    enableAnimations() {
        const styles = document.head.querySelectorAll('style');
        styles.forEach(style => {
            if (style.textContent.includes('animation-duration: 0.01ms')) {
                style.remove();
            }
        });
    }
    
    // Setup high contrast support
    setupHighContrast() {
        const mediaQuery = window.matchMedia('(prefers-contrast: high)');
        
        const handleHighContrast = (e) => {
            if (e.matches) {
                document.body.classList.add('high-contrast');
                // Apply high contrast styles
                this.applyHighContrast();
            } else {
                document.body.classList.remove('high-contrast');
                // Remove high contrast styles
                this.removeHighContrast();
            }
        };
        
        // Initial check
        handleHighContrast(mediaQuery);
        
        // Listen for changes
        mediaQuery.addListener(handleHighContrast);
    }
    
    // Apply high contrast styles
    applyHighContrast() {
        const style = document.createElement('style');
        style.id = 'high-contrast-styles';
        style.textContent = `
            :root {
                --text-primary: #ffffff;
                --text-secondary: #e0e0e0;
                --card-bg: rgba(0, 0, 0, 0.9);
            }
            .card {
                border: 2px solid #ffffff;
            }
            .form-control, .form-select {
                border: 2px solid #ffffff;
            }
            .btn-holomesh {
                border: 2px solid #ffffff;
            }
        `;
        document.head.appendChild(style);
    }
    
    // Remove high contrast styles
    removeHighContrast() {
        const style = document.getElementById('high-contrast-styles');
        if (style) {
            style.remove();
        }
    }
    
    // Setup skip links
    setupSkipLinks() {
        // Ensure skip links are properly handled
        const skipLinks = document.querySelectorAll('.skip-link');
        
        skipLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    targetElement.setAttribute('tabindex', '-1');
                    targetElement.focus();
                    
                    // Remove tabindex after focus
                    targetElement.addEventListener('blur', () => {
                        targetElement.removeAttribute('tabindex');
                    }, { once: true });
                }
            });
        });
    }
    
    // Announce messages to screen readers
    announceMessage(message, type = 'polite') {
        // Create or reuse aria-live region
        let liveRegion = document.getElementById('screen-reader-live-region');
        
        if (!liveRegion) {
            liveRegion = document.createElement('div');
            liveRegion.id = 'screen-reader-live-region';
            liveRegion.setAttribute('aria-live', type);
            liveRegion.setAttribute('aria-atomic', 'true');
            liveRegion.style.position = 'absolute';
            liveRegion.style.left = '-10000px';
            liveRegion.style.top = 'auto';
            liveRegion.style.width = '1px';
            liveRegion.style.height = '1px';
            liveRegion.style.overflow = 'hidden';
            document.body.appendChild(liveRegion);
        }
        
        // Set the message
        liveRegion.textContent = message;
    }
    
    // Ensure sufficient color contrast
    checkColorContrast(backgroundColor, textColor) {
        // Simple contrast checking function
        // In a real implementation, this would use more sophisticated algorithms
        const bg = this.parseColor(backgroundColor);
        const text = this.parseColor(textColor);
        
        if (!bg || !text) return true; // Assume valid if we can't parse
        
        const bgLuminance = this.getLuminance(bg);
        const textLuminance = this.getLuminance(text);
        
        const contrastRatio = (Math.max(bgLuminance, textLuminance) + 0.05) / 
                             (Math.min(bgLuminance, textLuminance) + 0.05);
        
        // WCAG AA requires 4.5:1 for normal text
        return contrastRatio >= 4.5;
    }
    
    // Parse color values
    parseColor(color) {
        // Simple color parsing - in a real implementation, this would be more robust
        if (color.startsWith('#')) {
            const hex = color.substring(1);
            if (hex.length === 3) {
                return {
                    r: parseInt(hex[0] + hex[0], 16),
                    g: parseInt(hex[1] + hex[1], 16),
                    b: parseInt(hex[2] + hex[2], 16)
                };
            } else if (hex.length === 6) {
                return {
                    r: parseInt(hex.substring(0, 2), 16),
                    g: parseInt(hex.substring(2, 4), 16),
                    b: parseInt(hex.substring(4, 6), 16)
                };
            }
        }
        return null;
    }
    
    // Calculate luminance
    getLuminance(color) {
        const r = color.r / 255;
        const g = color.g / 255;
        const b = color.b / 255;
        
        const rLinear = r <= 0.03928 ? r / 12.92 : Math.pow((r + 0.055) / 1.055, 2.4);
        const gLinear = g <= 0.03928 ? g / 12.92 : Math.pow((g + 0.055) / 1.055, 2.4);
        const bLinear = b <= 0.03928 ? b / 12.92 : Math.pow((b + 0.055) / 1.055, 2.4);
        
        return 0.2126 * rLinear + 0.7152 * gLinear + 0.0722 * bLinear;
    }
}

// Initialize accessibility features when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.holomeshAccessibility = new HoloMeshAccessibility();
});

// Export for use in other modules
export { HoloMeshAccessibility };