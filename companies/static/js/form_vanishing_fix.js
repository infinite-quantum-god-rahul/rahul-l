// Form Vanishing Fix - Prevent modal from disappearing when clicking form inputs
(function() {
    console.log('=== FORM VANISHING FIX LOADING ===');
    
    // Store original event handlers
    const originalHandlers = new Map();
    
    // Function to safely remove event listeners
    function removeEventListenerSafely(element, eventType, handler) {
        try {
            element.removeEventListener(eventType, handler);
        } catch (e) {
            console.log('Could not remove event listener:', e);
        }
    }
    
    // Function to disable problematic click handlers
    function disableProblematicClickHandlers() {
        console.log('Disabling problematic click handlers...');
        
        // Override the problematic handlers in modal_core.js and modal_hotfix.js
        // by replacing them with safer versions
        
        // Store original handlers
        if (!window._originalClickHandlers) {
            window._originalClickHandlers = new Map();
        }
        
        // Override the global click handler that closes modal
        const originalAddEventListener = document.addEventListener;
        document.addEventListener = function(type, handler, options) {
            // Check if this is the problematic click handler
            if (type === 'click' && handler.toString().includes('closest') && 
                (handler.toString().includes('teardownModal') || handler.toString().includes('kill()'))) {
                
                console.log('🚫 BLOCKED problematic click handler:', handler.toString().slice(0, 100) + '...');
                
                // Replace with a safer version
                const safeHandler = function(e) {
                    // Only close modal if clicking on actual navigation elements
                    var t = e.target.closest('a[href], button[type="button"]:not([data-toggle]), [data-nav], [data-entity]:not([data-entity=""]), [data-action]');
                    
                    // Don't close if clicking inside the modal form
                    if (e.target.closest('#entity-modal')) return;
                    
                    // Don't close if clicking on form inputs
                    if (e.target.matches('input, select, textarea, label')) return;
                    
                    // Don't close if clicking on form elements
                    if (e.target.closest('form, .form-group, .mb-3')) return;
                    
                    // Only close if it's a real navigation element
                    if (t && !t.closest('#entity-modal')) {
                        console.log('Closing modal due to navigation click on:', t);
                        if (typeof window.closeEntityModal === 'function') {
                            window.closeEntityModal();
                        }
                    }
                };
                
                // Store the original handler
                window._originalClickHandlers.set(handler, safeHandler);
                
                // Call the original addEventListener with the safe handler
                return originalAddEventListener.call(this, type, safeHandler, options);
            }
            
            // For all other event listeners, proceed normally
            return originalAddEventListener.call(this, type, handler, options);
        };
        
        console.log('Problematic click handlers disabled');
    }
    
    // Function to ensure modal stays open when clicking form inputs
    function ensureModalStaysOpen() {
        console.log('Ensuring modal stays open...');
        
        const modal = document.getElementById('entity-modal');
        if (!modal) return;
        
        // Add event listeners to prevent modal closing on form input clicks
        const form = modal.querySelector('#entity-form');
        if (form) {
            // Prevent any clicks inside the form from closing the modal
            form.addEventListener('click', function(e) {
                e.stopPropagation();
                console.log('Form click prevented from bubbling up');
            }, true);
            
            // Prevent any clicks on form inputs from closing the modal
            const inputs = form.querySelectorAll('input, select, textarea, label');
            inputs.forEach(input => {
                input.addEventListener('click', function(e) {
                    e.stopPropagation();
                    console.log('Input click prevented from bubbling up:', input.name || input.id);
                }, true);
                
                input.addEventListener('focus', function(e) {
                    e.stopPropagation();
                    console.log('Input focus prevented from bubbling up:', input.name || input.id);
                }, true);
            });
        }
        
        console.log('Modal stay-open protection installed');
    }
    
    // Function to monitor and prevent modal closing
    function monitorModalClosing() {
        console.log('Monitoring modal closing...');
        
        // Override closeEntityModal to add logging
        const originalCloseEntityModal = window.closeEntityModal;
        window.closeEntityModal = function(forceRefresh) {
            console.log('🔍 closeEntityModal called - checking if it should be prevented');
            
            // Check if we're in the middle of a form interaction
            const activeElement = document.activeElement;
            if (activeElement && activeElement.closest('#entity-modal')) {
                console.log('⚠️ Attempting to close modal while form input is focused - preventing');
                return; // Prevent closing
            }
            
            // Check if there's an ongoing form interaction
            const modal = document.getElementById('entity-modal');
            if (modal && modal.querySelector('input:focus, select:focus, textarea:focus')) {
                console.log('⚠️ Attempting to close modal while form input is focused - preventing');
                return; // Prevent closing
            }
            
            console.log('✅ Allowing modal to close');
            if (typeof originalCloseEntityModal === 'function') {
                originalCloseEntityModal(forceRefresh);
            }
        };
        
        console.log('Modal closing monitor installed');
    }
    
    // Main initialization function
    function initializeFormVanishingFix() {
        console.log('Initializing form vanishing fix...');
        
        // Disable problematic handlers first
        disableProblematicClickHandlers();
        
        // Monitor modal closing
        monitorModalClosing();
        
        // Wait for modal to be available and apply fixes
        const checkModal = setInterval(function() {
            const modal = document.getElementById('entity-modal');
            if (modal) {
                clearInterval(checkModal);
                ensureModalStaysOpen();
                console.log('Form vanishing fix initialized successfully');
            }
        }, 100);
        
        // Also run when modal is shown
        const originalOpenEntityModal = window.openEntityModal;
        window.openEntityModal = function(entity) {
            if (typeof originalOpenEntityModal === 'function') {
                originalOpenEntityModal(entity);
            }
            
            // Apply fixes after modal opens
            setTimeout(function() {
                ensureModalStaysOpen();
            }, 100);
        };
        
        const originalEditEntity = window.editEntity;
        window.editEntity = function(entity, id) {
            if (typeof originalEditEntity === 'function') {
                originalEditEntity(entity, id);
            }
            
            // Apply fixes after modal opens
            setTimeout(function() {
                ensureModalStaysOpen();
            }, 100);
        };
    }
    
    // Run initialization
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeFormVanishingFix);
    } else {
        initializeFormVanishingFix();
    }
    
    console.log('=== FORM VANISHING FIX LOADED ===');
})();





