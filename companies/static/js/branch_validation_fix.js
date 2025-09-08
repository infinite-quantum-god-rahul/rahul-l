// Branch Validation Fix - Shows specific validation errors instead of generic "Validation failed"
// This file specifically targets the branch creation form to show detailed error messages

(function() {
    'use strict';

    console.log('Branch validation fix loaded');

    // Function to show detailed validation errors
    function showDetailedBranchErrors(errors) {
        let errorMessage = "Branch validation failed:\n\n";
        
        if (errors && typeof errors === 'object') {
            // Map field names to user-friendly names
            const fieldNames = {
                'code': 'Branch Code',
                'name': 'Branch Name', 
                'company': 'Company',
                'phone': 'Phone Number',
                'open_date': 'Open Date',
                'address1': 'Address',
                'district': 'District'
            };
            
            for (let field in errors) {
                const msgs = Array.isArray(errors[field]) ? errors[field].join(", ") : errors[field];
                const friendlyName = fieldNames[field] || field;
                errorMessage += `• ${friendlyName}: ${msgs}\n`;
            }
        } else {
            errorMessage += "Please check the form for specific errors.";
        }
        
        // Show detailed error message
        alert(errorMessage);
        
        // Also highlight fields in the form
        highlightInvalidFields(errors);
    }

    // Function to highlight invalid fields
    function highlightInvalidFields(errors) {
        if (!errors) return;
        
        const form = document.getElementById('entity-form');
        if (!form) return;
        
        // Clear previous highlights
        form.querySelectorAll('.is-invalid').forEach(field => {
            field.classList.remove('is-invalid');
        });
        
        // Highlight invalid fields
        for (let fieldName in errors) {
            const field = form.querySelector(`[name="${fieldName}"]`) || 
                         form.querySelector(`#id_${fieldName}`) ||
                         form.querySelector(`[id*="${fieldName}"]`);
            
            if (field) {
                field.classList.add('is-invalid');
                
                // Add error message below field
                let errorDiv = field.parentNode.querySelector('.invalid-feedback');
                if (!errorDiv) {
                    errorDiv = document.createElement('div');
                    errorDiv.className = 'invalid-feedback d-block';
                    field.parentNode.appendChild(errorDiv);
                }
                
                const msgs = Array.isArray(errors[fieldName]) ? errors[fieldName].join(", ") : errors[fieldName];
                errorDiv.textContent = msgs;
                errorDiv.style.display = 'block';
            }
        }
    }

    // Override the generic "Validation failed" message specifically for branch forms
    function overrideBranchValidationMessages() {
        // Check if we're on a branch form
        const form = document.getElementById('entity-form');
        if (!form) return;
        
        const entity = form.dataset.entity || '';
        if (entity.toLowerCase() !== 'branch') return;
        
        console.log('Branch form detected, setting up enhanced validation');
        
        // Override the showFormErrors function if it exists
        if (typeof window.showFormErrors === 'function') {
            const originalShowFormErrors = window.showFormErrors;
            window.showFormErrors = function(errors) {
                // Call original function
                originalShowFormErrors(errors);
                
                // Show detailed branch errors
                showDetailedBranchErrors(errors);
            };
        }
        
        // Also override the generic alert for validation failed
        const originalAlert = window.alert;
        window.alert = function(message) {
            if (message === "Validation failed." || 
                message === "Validation failed" ||
                message.includes("Validation failed")) {
                
                // Try to get form errors from the DOM
                const formErrors = form.querySelectorAll('.invalid-feedback');
                if (formErrors.length > 0) {
                    let detailedMessage = "Branch validation errors:\n\n";
                    formErrors.forEach(errorDiv => {
                        if (errorDiv.style.display !== 'none' && errorDiv.textContent) {
                            const field = errorDiv.previousElementSibling;
                            const fieldName = field ? (field.name || field.id || 'Unknown field') : 'Unknown field';
                            detailedMessage += `• ${fieldName}: ${errorDiv.textContent}\n`;
                        }
                    });
                    originalAlert(detailedMessage);
                    return;
                }
                
                // Fallback to more helpful message
                originalAlert("Branch validation failed. Please check the form for specific error messages below each field.");
                return;
            }
            
            // Call original alert for other messages
            originalAlert(message);
        };
    }

    // Initialize when DOM is ready
    function init() {
        // Wait a bit for the form to be loaded
        setTimeout(() => {
            overrideBranchValidationMessages();
        }, 100);
        
        // Also watch for dynamic form loading
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    const form = document.getElementById('entity-form');
                    if (form && form.dataset.entity && form.dataset.entity.toLowerCase() === 'branch') {
                        overrideBranchValidationMessages();
                    }
                }
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose functions globally
    window.showDetailedBranchErrors = showDetailedBranchErrors;
    window.highlightInvalidFields = highlightInvalidFields;

})();
