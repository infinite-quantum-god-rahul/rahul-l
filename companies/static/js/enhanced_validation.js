// Enhanced Validation Error Display
// This file improves validation error messages to show specific details instead of generic "Validation failed"

(function() {
    'use strict';

    // Enhanced error display function
    function showDetailedValidationErrors(data) {
        let errorMessage = "Validation failed:\n\n";
        
        if (data.errors && typeof data.errors === 'object') {
            // Handle field-specific errors
            for (let field in data.errors) {
                const msgs = Array.isArray(data.errors[field]) ? data.errors[field].join(", ") : data.errors[field];
                errorMessage += `• ${field}: ${msgs}\n`;
            }
        } else if (data.error && typeof data.error === 'string') {
            // Handle general error message
            errorMessage += data.error;
        } else {
            // Fallback message
            errorMessage += "Please check the form for errors.";
        }
        
        // Show detailed error message
        alert(errorMessage);
        
        // Also show errors in the form
        if (data.errors) {
            showFormErrorsInForm(data.errors);
        }
    }

    // Show validation errors directly in the form
    function showFormErrorsInForm(errors) {
        const form = document.getElementById('entity-form');
        if (!form) return;
        
        // Clear previous errors
        clearFormErrors(form);
        
        // Show each error
        for (let field in errors) {
            const msgs = Array.isArray(errors[field]) ? errors[field].join(", ") : errors[field];
            markFieldAsInvalid(form, field, msgs);
        }
    }

    // Mark a field as invalid with error message
    function markFieldAsInvalid(form, fieldName, errorMessage) {
        const field = form.querySelector(`[name="${fieldName}"]`) || 
                     form.querySelector(`#id_${fieldName}`) ||
                     form.querySelector(`[id*="${fieldName}"]`);
        
        if (!field) return;
        
        // Add invalid class
        field.classList.add('is-invalid');
        
        // Create or update error message
        let errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            errorDiv.style.display = 'block';
            field.parentNode.appendChild(errorDiv);
        }
        
        errorDiv.textContent = errorMessage;
        errorDiv.style.display = 'block';
        
        // Focus on first invalid field
        if (field === form.querySelector('.is-invalid')) {
            field.focus();
        }
    }

    // Clear all form errors
    function clearFormErrors(form) {
        form.querySelectorAll('.is-invalid').forEach(field => {
            field.classList.remove('is-invalid');
        });
        
        form.querySelectorAll('.invalid-feedback').forEach(errorDiv => {
            errorDiv.style.display = 'none';
            errorDiv.textContent = '';
        });
    }

    // Override the generic "Validation failed" messages
    function overrideGenericValidationMessages() {
        // Override alert function to catch generic validation messages
        const originalAlert = window.alert;
        window.alert = function(message) {
            if (message === "Validation failed." || 
                message === "Validation failed" ||
                message.includes("Validation failed")) {
                
                // Try to get more detailed error information
                const form = document.getElementById('entity-form');
                if (form) {
                    const formErrors = form.querySelectorAll('.invalid-feedback');
                    if (formErrors.length > 0) {
                        let detailedMessage = "Validation errors:\n\n";
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
                }
                
                // Fallback to more helpful message
                originalAlert("Validation failed. Please check the form for specific error messages below each field.");
                return;
            }
            
            // Call original alert for other messages
            originalAlert(message);
        };
    }

    // Enhanced form submission handler
    function setupEnhancedFormValidation() {
        const form = document.getElementById('entity-form');
        if (!form) return;
        
        form.addEventListener('submit', function(e) {
            // Clear previous errors before submission
            clearFormErrors(form);
        });
    }

    // Initialize enhanced validation
    function init() {
        // Override generic messages
        overrideGenericValidationMessages();
        
        // Setup form validation
        setupEnhancedFormValidation();
        
        // Override the showFormErrors function if it exists
        if (typeof window.showFormErrors === 'function') {
            const originalShowFormErrors = window.showFormErrors;
            window.showFormErrors = function(errors) {
                // Call original function
                originalShowFormErrors(errors);
                
                // Also show detailed alert
                if (errors && Object.keys(errors).length > 0) {
                    showDetailedValidationErrors({ errors: errors });
                }
            };
        }
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose functions globally
    window.showDetailedValidationErrors = showDetailedValidationErrors;
    window.showFormErrorsInForm = showFormErrorsInForm;
    window.markFieldAsInvalid = markFieldAsInvalid;
    window.clearFormErrors = clearFormErrors;

})();
