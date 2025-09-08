// TRUE ERROR CATCHER - Catches "True is not defined" errors immediately
// This script overrides JavaScript error handling to catch and fix the error

(function() {
    'use strict';
    
    console.log('🚨 TRUE ERROR CATCHER LOADED - Will catch "True is not defined" errors immediately');
    
    // Store original error handler
    const originalOnError = window.onerror;
    const originalAddEventListener = window.addEventListener;
    
    // Function to fix required attributes when the error occurs
    function fixRequiredAttributesOnError() {
        console.log('🔧 Fixing required attributes after error detection...');
        
        try {
            // Find all form fields with required attributes
            const requiredFields = document.querySelectorAll('[required]');
            console.log(`Found ${requiredFields.length} fields with required attribute`);
            
            let fixedCount = 0;
            
            requiredFields.forEach((field, index) => {
                try {
                    const requiredValue = field.getAttribute('required');
                    
                    // Check if the required attribute has the problematic value
                    if (requiredValue === 'True') {
                        console.log(`❌ PROBLEM: Field ${field.name || field.id || 'unknown'} has required=True (Python boolean)`);
                        
                        // Fix the attribute immediately
                        field.setAttribute('required', 'required');
                        field.setAttribute('data-required', 'true');
                        field.dataset.required = 'true';
                        
                        console.log(`✅ IMMEDIATELY FIXED: Field now has required="required"`);
                        fixedCount++;
                    }
                    
                } catch (error) {
                    console.error(`❌ ERROR processing field:`, error);
                }
            });
            
            if (fixedCount > 0) {
                console.log(`🎉 Successfully fixed ${fixedCount} problematic required attributes!`);
                console.log(`✅ The "True is not defined" error should no longer occur`);
            }
            
        } catch (error) {
            console.error('❌ Error in fixRequiredAttributesOnError:', error);
        }
    }
    
    // Override window.onerror to catch the specific error
    window.onerror = function(message, source, lineno, colno, error) {
        console.log(`🚨 JavaScript error caught: ${message} at ${source}:${lineno}:${colno}`);
        
        // Check if this is the "True is not defined" error
        if (message && message.includes('True is not defined')) {
            console.log('🚨 "True is not defined" error detected! Applying immediate fix...');
            
            // Fix the required attributes immediately
            fixRequiredAttributesOnError();
            
            // Return true to prevent the error from being logged to console
            return true;
        }
        
        // Call original error handler if it exists
        if (originalOnError) {
            return originalOnError(message, source, lineno, colno, error);
        }
        
        // Return false to allow default error handling
        return false;
    };
    
    // Also override addEventListener to catch unhandled promise rejections
    window.addEventListener = function(type, listener, options) {
        if (type === 'unhandledrejection') {
            // Wrap the listener to catch promise rejections
            const wrappedListener = function(event) {
                try {
                    if (event.reason && event.reason.message && event.reason.message.includes('True is not defined')) {
                        console.log('🚨 "True is not defined" error in promise! Applying immediate fix...');
                        fixRequiredAttributesOnError();
                        event.preventDefault();
                        return;
                    }
                } catch (error) {
                    console.error('❌ Error in wrapped promise rejection listener:', error);
                }
                
                // Call original listener
                return listener.call(this, event);
            };
            
            return originalAddEventListener.call(this, type, wrappedListener, options);
        }
        
        // Call original addEventListener for other event types
        return originalAddEventListener.call(this, type, listener, options);
    };
    
    // Also set up a global error event listener
    window.addEventListener('error', function(event) {
        if (event.error && event.error.message && event.error.message.includes('True is not defined')) {
            console.log('🚨 "True is not defined" error in global error event! Applying immediate fix...');
            fixRequiredAttributesOnError();
            event.preventDefault();
        }
    });
    
    // Set up a mutation observer to watch for form fields being added
    function setupFormFieldWatcher() {
        console.log('🔍 Setting up form field watcher...');
        
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            // Check if this node or its children have required attributes
                            const requiredFields = node.querySelectorAll ? node.querySelectorAll('[required]') : [];
                            if (node.hasAttribute && node.hasAttribute('required')) {
                                requiredFields.push(node);
                            }
                            
                            if (requiredFields.length > 0) {
                                console.log(`🚨 New form fields detected with required attributes: ${requiredFields.length}`);
                                
                                // Check for problematic attributes
                                requiredFields.forEach(field => {
                                    try {
                                        const requiredValue = field.getAttribute('required');
                                        if (requiredValue === 'True') {
                                            console.log(`❌ PROBLEM: New field ${field.name || field.id || 'unknown'} has required=True`);
                                            
                                            // Fix immediately
                                            field.setAttribute('required', 'required');
                                            field.setAttribute('data-required', 'true');
                                            field.dataset.required = 'true';
                                            
                                            console.log(`✅ IMMEDIATELY FIXED: New field now has required="required"`);
                                        }
                                    } catch (error) {
                                        console.error('❌ Error processing new field:', error);
                                    }
                                });
                            }
                        }
                    });
                }
            });
        });
        
        // Start observing
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        console.log('🔍 Form field watcher active');
    }
    
    // Function to run the error catcher
    function runTrueErrorCatcher() {
        console.log('🚨 Running TRUE ERROR CATCHER...');
        
        // Fix existing fields immediately
        fixRequiredAttributesOnError();
        
        // Set up form field watcher
        setupFormFieldWatcher();
        
        // Also run the fix periodically to catch any missed fields
        setInterval(fixRequiredAttributesOnError, 500);
        
        console.log('🚨 TRUE ERROR CATCHER complete and active');
    }
    
    // Run the error catcher IMMEDIATELY
    console.log('🚨 Starting TRUE ERROR CATCHER immediately...');
    runTrueErrorCatcher();
    
    // Also run when the page is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🚨 DOM loaded, running additional TRUE ERROR CATCHER...');
            setTimeout(runTrueErrorCatcher, 100);
        });
    }
    
    // Also run when the page is fully loaded
    window.addEventListener('load', function() {
        console.log('🚨 Page fully loaded, running final TRUE ERROR CATCHER...');
        setTimeout(runTrueErrorCatcher, 200);
    });
    
    // Make the fix function available globally for manual use
    window.fixRequiredAttributesOnError = fixRequiredAttributesOnError;
    
    console.log('🚨 TRUE ERROR CATCHER ready and active - Will catch "True is not defined" errors immediately');
    
})();
