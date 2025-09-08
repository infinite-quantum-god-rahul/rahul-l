// Smart Form Input Fix - Works with CSS to properly handle form inputs
(function() {
    console.log('=== SMART FORM INPUT FIX LOADING ===');
    
    // Function to intelligently handle form inputs
    function smartHandleFormInputs() {
        console.log('=== SMART HANDLING FORM INPUTS ===');
        
        // Get all form inputs on the page
        var allInputs = document.querySelectorAll('input, select, textarea');
        console.log('Found', allInputs.length, 'form inputs');
        
        allInputs.forEach(function(el) {
            if (el.type === 'hidden') return; // Skip hidden inputs
            
            var fieldName = el.name || el.id || 'unknown';
            var fieldType = el.type || 'text';
            var isReadOnly = el.hasAttribute('readonly') || el.readOnly;
            
            console.log('Processing:', fieldName, 'type:', fieldType, 'readonly:', isReadOnly);
            
            if (isReadOnly) {
                // Keep readonly fields as they are - CSS will handle styling
                console.log('Keeping readonly for:', fieldName);
                el.readOnly = true;
                el.setAttribute('readonly', 'readonly');
            } else {
                // Enable non-readonly inputs
                console.log('Enabling input for:', fieldName);
                el.removeAttribute('readonly');
                el.removeAttribute('disabled');
                el.readOnly = false;
                el.disabled = false;
                
                // Remove any classes that might disable
                el.classList.remove('disabled');
            }
            
            console.log('Result for', fieldName, 'readonly:', el.readOnly, 'disabled:', el.disabled);
        });
        
        console.log('=== SMART INPUT HANDLING COMPLETE ===');
    }
    
    // Run immediately
    smartHandleFormInputs();
    
    // Run after DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', smartHandleFormInputs);
    }
    
    // Run after a delay to catch any late changes
    setTimeout(smartHandleFormInputs, 100);
    setTimeout(smartHandleFormInputs, 500);
    setTimeout(smartHandleFormInputs, 1000);
    
    // Run when any modal is shown
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1) { // Element node
                    if (node.id === 'entity-modal' || node.classList.contains('modal')) {
                        console.log('Modal detected, handling inputs...');
                        setTimeout(smartHandleFormInputs, 50);
                        setTimeout(smartHandleFormInputs, 200);
                        setTimeout(smartHandleFormInputs, 500);
                    }
                }
            });
        });
    });
    
    // Start observing
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Also run on any click event (in case modals are opened by clicks)
    document.addEventListener('click', function(e) {
        setTimeout(smartHandleFormInputs, 100);
    });
    
    // Run periodically to catch any changes
    setInterval(smartHandleFormInputs, 5000);
    
    console.log('=== SMART FORM INPUT FIX LOADED ===');
})();
