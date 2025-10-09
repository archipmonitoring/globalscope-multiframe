// HoloMesh Performance Optimization Utilities
// Provides performance enhancements for ultra-fast chip optimization experience

class HoloMeshPerformance {
    constructor() {
        this.init();
    }
    
    init() {
        // Initialize performance optimization features
        this.setupResourcePrefetching();
        this.setupLazyLoading();
        this.setupAnimationOptimization();
        this.setupMemoryManagement();
        this.setupNetworkOptimization();
        this.setupCaching();
    }
    
    // Setup resource prefetching for faster navigation
    setupResourcePrefetching() {
        // Prefetch critical resources
        const resourcesToPrefetch = [
            '/dashboard',
            '/static/js/threejs_visualization.js',
            '/static/js/accessibility.js'
        ];
        
        // Use Intersection Observer to prefetch when user shows intent
        const prefetchObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const link = entry.target;
                    const href = link.getAttribute('href');
                    
                    // Prefetch the resource
                    if (href) {
                        const prefetchLink = document.createElement('link');
                        prefetchLink.rel = 'prefetch';
                        prefetchLink.href = href;
                        document.head.appendChild(prefetchLink);
                        
                        // Stop observing this element
                        prefetchObserver.unobserve(link);
                    }
                }
            });
        }, {
            threshold: 0.5 // Trigger when 50% visible
        });
        
        // Observe navigation links
        document.addEventListener('DOMContentLoaded', () => {
            const navLinks = document.querySelectorAll('a[href]');
            navLinks.forEach(link => {
                prefetchObserver.observe(link);
            });
        });
    }
    
    // Setup lazy loading for better initial load performance
    setupLazyLoading() {
        // Lazy load images
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        const src = img.dataset.src;
                        
                        if (src) {
                            img.src = src;
                            img.classList.remove('lazy');
                            observer.unobserve(img);
                        }
                    }
                });
            });
            
            const lazyImages = document.querySelectorAll('img[data-src]');
            lazyImages.forEach(img => imageObserver.observe(img));
        }
        
        // Lazy load 3D visualization container
        const visualizationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const container = entry.target;
                    container.classList.add('visible');
                    
                    // Initialize 3D visualization only when visible
                    if (typeof window.initialize3DVisualization === 'function') {
                        window.initialize3DVisualization();
                    }
                    
                    visualizationObserver.unobserve(container);
                }
            });
        }, {
            threshold: 0.1
        });
        
        const visualizationContainer = document.getElementById('visualizationContainer');
        if (visualizationContainer) {
            visualizationObserver.observe(visualizationContainer);
        }
    }
    
    // Setup animation optimization for smooth performance
    setupAnimationOptimization() {
        // Use requestAnimationFrame for smooth animations
        this.rafCallbacks = new Set();
        
        const animate = () => {
            this.rafCallbacks.forEach(callback => {
                callback();
            });
            requestAnimationFrame(animate);
        };
        
        requestAnimationFrame(animate);
        
        // Throttle expensive operations
        this.throttle = (func, limit) => {
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
        };
        
        // Debounce for resize events
        this.debounce = (func, delay) => {
            let timeoutId;
            return function() {
                const context = this;
                const args = arguments;
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => func.apply(context, args), delay);
            };
        };
        
        // Optimize resize handling
        const handleResize = this.debounce(() => {
            // Handle resize efficiently
            this.handleWindowResize();
        }, 250);
        
        window.addEventListener('resize', handleResize);
    }
    
    // Handle window resize efficiently
    handleWindowResize() {
        // Notify components about resize
        window.dispatchEvent(new CustomEvent('optimizedResize'));
        
        // Update visualization if needed
        if (window.visualizer) {
            window.visualizer.onWindowResize();
        }
    }
    
    // Setup memory management to prevent leaks
    setupMemoryManagement() {
        // Clean up resources when navigating away
        window.addEventListener('beforeunload', () => {
            // Dispose Three.js resources
            if (window.visualizer) {
                window.visualizer.dispose();
            }
            
            // Clean up event listeners
            this.cleanupEventListeners();
        });
        
        // Periodic garbage collection hints
        if (window.requestIdleCallback) {
            setInterval(() => {
                window.requestIdleCallback(() => {
                    // Perform non-critical cleanup
                    if (window.gc) {
                        window.gc();
                    }
                });
            }, 30000); // Every 30 seconds
        }
    }
    
    // Clean up event listeners to prevent memory leaks
    cleanupEventListeners() {
        // Remove all registered RAF callbacks
        this.rafCallbacks.clear();
        
        // Additional cleanup can be added here
    }
    
    // Setup network optimization
    setupNetworkOptimization() {
        // Detect network conditions
        if ('connection' in navigator) {
            const connection = navigator.connection;
            
            // Adjust quality based on network
            if (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g') {
                document.body.classList.add('low-bandwidth');
                this.reduceQuality();
            }
            
            // Monitor network changes
            connection.addEventListener('change', () => {
                if (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g') {
                    document.body.classList.add('low-bandwidth');
                    this.reduceQuality();
                } else {
                    document.body.classList.remove('low-bandwidth');
                    this.restoreQuality();
                }
            });
        }
        
        // Setup fetch optimization
        const originalFetch = window.fetch;
        window.fetch = (...args) => {
            // Add performance headers
            const [url, options = {}] = args;
            options.headers = {
                ...options.headers,
                'X-Performance': 'optimized'
            };
            
            // Add timeout
            if (!options.signal) {
                const controller = new AbortController();
                options.signal = controller.signal;
                setTimeout(() => controller.abort(), 10000); // 10 second timeout
            }
            
            return originalFetch(...args);
        };
    }
    
    // Reduce quality for low bandwidth
    reduceQuality() {
        // Reduce 3D visualization quality
        if (window.visualizer) {
            window.visualizer.reduceQuality();
        }
        
        // Load lower quality images
        const images = document.querySelectorAll('img[data-src-low]');
        images.forEach(img => {
            const lowSrc = img.dataset.srcLow;
            if (lowSrc) {
                img.src = lowSrc;
            }
        });
    }
    
    // Restore quality
    restoreQuality() {
        // Restore 3D visualization quality
        if (window.visualizer) {
            window.visualizer.restoreQuality();
        }
        
        // Load high quality images
        const images = document.querySelectorAll('img[data-src]');
        images.forEach(img => {
            const src = img.dataset.src;
            if (src) {
                img.src = src;
            }
        });
    }
    
    // Setup intelligent caching
    setupCaching() {
        // Setup localStorage caching for API responses
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
        
        // Wrap fetch with caching
        const originalFetch = window.fetch;
        window.fetch = (url, options = {}) => {
            // Only cache GET requests
            if (options.method && options.method !== 'GET') {
                return originalFetch(url, options);
            }
            
            const cacheKey = url;
            const cached = this.cache.get(cacheKey);
            
            // Return cached response if still valid
            if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
                return Promise.resolve(new Response(JSON.stringify(cached.data), {
                    status: 200,
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Cached': 'true'
                    }
                }));
            }
            
            // Fetch and cache the response
            return originalFetch(url, options).then(response => {
                // Only cache successful JSON responses
                if (response.ok && response.headers.get('Content-Type')?.includes('application/json')) {
                    return response.clone().json().then(data => {
                        this.cache.set(cacheKey, {
                            data: data,
                            timestamp: Date.now()
                        });
                        return response;
                    });
                }
                return response;
            });
        };
    }
    
    // Add callback to RAF loop
    addRafCallback(callback) {
        this.rafCallbacks.add(callback);
    }
    
    // Remove callback from RAF loop
    removeRafCallback(callback) {
        this.rafCallbacks.delete(callback);
    }
    
    // Measure performance of a function
    measurePerformance(name, func) {
        return (...args) => {
            const start = performance.now();
            const result = func(...args);
            const end = performance.now();
            
            console.log(`[Performance] ${name}: ${end - start}ms`);
            
            // Send to analytics if available
            if (window.gtag) {
                window.gtag('event', 'performance', {
                    'event_category': 'timing',
                    'event_label': name,
                    'value': Math.round(end - start)
                });
            }
            
            return result;
        };
    }
    
    // Preload critical resources
    preloadCriticalResources() {
        const criticalResources = [
            '/static/styles.css',
            '/static/js/threejs_visualization.js'
        ];
        
        criticalResources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = resource.endsWith('.css') ? 'style' : 'script';
            link.href = resource;
            document.head.appendChild(link);
        });
    }
}

// Initialize performance optimization when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.holomeshPerformance = new HoloMeshPerformance();
    
    // Preload critical resources
    window.holomeshPerformance.preloadCriticalResources();
});

// Export for use in other modules
export { HoloMeshPerformance };