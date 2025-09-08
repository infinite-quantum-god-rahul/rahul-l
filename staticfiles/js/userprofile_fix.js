// UserProfile Modal Fix - Minimal Safe Version
// This file ensures UserProfile works properly without breaking the website

(function() {
    'use strict';
    
    console.log('UserProfile fix loaded - Minimal Safe version');
    
    // Global flag to track if UserProfile fix is active
    window.USERPROFILE_FIX_ACTIVE = true;
    
    // Simple function to fix UserProfile form rendering
    function fixUserProfileForm() {
        try {
            console.log('Checking for UserProfile form...');
            
            // Check if we have a UserProfile modal open
            const modal = document.getElementById('entity-modal');
            if (!modal) {
                return;
            }
            
            const form = document.getElementById('entity-form');
            if (!form) {
                return;
            }
            
            const entity = form.getAttribute('data-entity');
            if (!entity || entity.toLowerCase() !== 'userprofile') {
                return;
            }
            
            console.log('Found UserProfile form, applying minimal fixes...');
            
            // 1. Ensure modal is visible
            modal.style.display = 'flex';
            modal.style.visibility = 'visible';
            modal.style.opacity = '1';
            
            // 2. Ensure form is visible
            form.style.display = 'block';
            form.style.visibility = 'visible';
            
            // 3. Make sure all form fields are visible
            const allFormElements = form.querySelectorAll('input, select, textarea, label, .form-group, .mb-3, .col-md-6');
            allFormElements.forEach(function(element) {
                element.style.display = 'block';
                element.style.visibility = 'visible';
            });
            
            // 4. Fix close button functionality
            const closeBtn = modal.querySelector('.close-btn');
            if (closeBtn) {
                closeBtn.onclick = function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('Closing UserProfile modal');
                    modal.style.display = 'none';
                    if (typeof window.closeEntityModal === 'function') {
                        window.closeEntityModal();
                    }
                };
            }
            
            console.log('UserProfile form fixed successfully');
        } catch (error) {
            console.error('Error in fixUserProfileForm:', error);
        }
    }
    
    // Override modal functions to ensure UserProfile works
    function overrideModalFunctions() {
        try {
            // Override openEntityModal for UserProfile
            const originalOpenEntityModal = window.openEntityModal;
            if (typeof originalOpenEntityModal === 'function') {
                window.openEntityModal = function(entity) {
                    if (entity && entity.toLowerCase() === 'userprofile') {
                        console.log('Opening UserProfile modal...');
                        const result = originalOpenEntityModal.call(this, entity);
                        // Fix the form after it loads
                        setTimeout(fixUserProfileForm, 500);
                        return result;
                    }
                    return originalOpenEntityModal.apply(this, arguments);
                };
            }
            
            // Override editEntity for UserProfile
            const originalEditEntity = window.editEntity;
            if (typeof originalEditEntity === 'function') {
                window.editEntity = function(entity, id) {
                    if (entity && entity.toLowerCase() === 'userprofile') {
                        console.log('Editing UserProfile...');
                        const result = originalEditEntity.call(this, entity, id);
                        // Fix the form after it loads
                        setTimeout(fixUserProfileForm, 500);
                        return result;
                    }
                    return originalEditEntity.apply(this, arguments);
                };
            }
        } catch (error) {
            console.error('Error in overrideModalFunctions:', error);
        }
    }
    
    // Main initialization
    function init() {
        try {
            console.log('UserProfile fix initializing...');
            
            // Override modal functions
            overrideModalFunctions();
            
            // Fix any existing UserProfile forms
            fixUserProfileForm();
            
            // Set up observer for dynamic content
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.addedNodes.length > 0) {
                        // Check if a UserProfile form was added
                        setTimeout(fixUserProfileForm, 100);
                    }
                });
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
            
            console.log('UserProfile fix initialized');
        } catch (error) {
            console.error('Error in init:', error);
        }
    }
    
    // Run immediately if DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Also run on window load
    window.addEventListener('load', function() {
        console.log('UserProfile fix - window loaded');
        setTimeout(fixUserProfileForm, 1000);
    });
    
    // Export for debugging
    window.userProfileFix = {
        fixUserProfileForm: fixUserProfileForm,
        init: init
    };
    
})();
