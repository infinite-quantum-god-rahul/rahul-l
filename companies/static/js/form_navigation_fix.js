// Form Navigation Fix - Comprehensive solution
(function() {
    console.log('=== FORM NAVIGATION FIX LOADING ===');
    
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
    
    // Function to disable all problematic keydown handlers temporarily
    function disableProblematicHandlers() {
        console.log('Disabling problematic event handlers...');
        
        // Disable global keydown handlers that might interfere
        const globalKeydownHandlers = document.querySelectorAll('*');
        globalKeydownHandlers.forEach(element => {
            // Store any existing keydown handlers
            if (element._keydownHandlers) {
                element._keydownHandlers.forEach(handler => {
                    removeEventListenerSafely(element, 'keydown', handler);
                });
            }
        });
        
        // Specifically target modal-related keydown handlers
        const modal = document.getElementById('entity-modal');
        if (modal) {
            // Remove any existing keydown handlers from modal
            const modalKeydownHandlers = modal.querySelectorAll('*');
            modalKeydownHandlers.forEach(element => {
                if (element._keydownHandlers) {
                    element._keydownHandlers.forEach(handler => {
                        removeEventListenerSafely(element, 'keydown', handler);
                    });
                }
            });
        }
    }
    
    // Function to enable only the correct keydown handlers
    function enableCorrectHandlers() {
        console.log('Enabling correct event handlers...');
        
        const modal = document.getElementById('entity-modal');
        if (!modal) return;
        
        const form = modal.querySelector('#entity-form');
        if (!form) return;
        
        // Add the correct keydown handler
        const correctKeydownHandler = function(e) {
            // Only handle Enter key
            if (e.key !== 'Enter') return;
            
            // Don't submit if it's a textarea (allow new lines)
            if (e.target.tagName === 'TEXTAREA') return;
            
            // Don't submit if it's a select dropdown
            if (e.target.tagName === 'SELECT') return;
            
            // Prevent default form submission
            e.preventDefault();
            e.stopPropagation();
            
            // Only submit if the form is valid and save button is enabled
            const saveBtn = document.getElementById('modal-save-btn');
            if (saveBtn && !saveBtn.disabled && typeof window._modalSave === 'function') {
                console.log('Submitting form via Enter key');
                window._modalSave();
            }
        };
        
        // Remove any existing keydown handlers from the form
        form.removeEventListener('keydown', correctKeydownHandler);
        
        // Add the correct handler
        form.addEventListener('keydown', correctKeydownHandler);
        
        // Store the handler for later removal if needed
        form._correctKeydownHandler = correctKeydownHandler;
        
        console.log('Correct keydown handler installed');
    }
    
    // Function to fix form inputs
    function fixFormInputs() {
        console.log('Fixing form inputs...');
        
        const modal = document.getElementById('entity-modal');
        if (!modal) return;
        
        const inputs = modal.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            if (input.type === 'hidden') return;
            
            // Remove any readonly/disabled attributes from non-readonly fields
            if (!input.hasAttribute('readonly') && !input.readOnly) {
                input.removeAttribute('readonly');
                input.removeAttribute('disabled');
                input.readOnly = false;
                input.disabled = false;
                
                // Ensure the input is interactive
                input.style.pointerEvents = 'auto';
                input.style.userSelect = 'auto';
                input.style.cursor = 'text';
                input.style.backgroundColor = 'white';
                input.style.color = 'black';
                input.style.opacity = '1';
            }
        });
        
        console.log('Form inputs fixed');
    }
    
    // Main initialization function
    function initializeFormNavigationFix() {
        console.log('Initializing form navigation fix...');
        
        // Wait for modal to be available
        const checkModal = setInterval(function() {
            const modal = document.getElementById('entity-modal');
            if (modal) {
                clearInterval(checkModal);
                
                // Disable problematic handlers first
                disableProblematicHandlers();
                
                // Enable correct handlers
                enableCorrectHandlers();
                
                // Fix form inputs
                fixFormInputs();
                
                console.log('Form navigation fix initialized successfully');
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
                disableProblematicHandlers();
                enableCorrectHandlers();
                fixFormInputs();
            }, 100);
        };
        
        const originalEditEntity = window.editEntity;
        window.editEntity = function(entity, id) {
            if (typeof originalEditEntity === 'function') {
                originalEditEntity(entity, id);
            }
            
            // Apply fixes after modal opens
            setTimeout(function() {
                disableProblematicHandlers();
                enableCorrectHandlers();
                fixFormInputs();
            }, 100);
        };
    }
    
    // Run initialization
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeFormNavigationFix);
    } else {
        initializeFormNavigationFix();
    }
    
    console.log('=== FORM NAVIGATION FIX LOADED ===');
})();





