// Branch Required Attribute Fix - Client-side fix for "True is not defined" error
// This script runs after the page loads and fixes any problematic required attributes

(function() {
    'use strict';
    
    console.log('Branch required attribute fix loaded');
    
    // Function to fix required attributes
    function fixRequiredAttributes() {
        console.log('Fixing required attributes...');
        
        // Find all form fields with required attributes
        const requiredFields = document.querySelectorAll('[required]');
        console.log(`Found ${requiredFields.length} fields with required attribute`);
        
        let fixedCount = 0;
        let problematicCount = 0;
        
        requiredFields.forEach((field, index) => {
            try {
                const requiredValue = field.getAttribute('required');
                console.log(`Field ${index + 1}: ${field.name}, required value: "${requiredValue}"`);
                
                // Check if the required attribute has the problematic value
                if (requiredValue === 'True') {
                    console.log(`❌ PROBLEM: Field ${field.name} has required=True (Python boolean)`);
                    problematicCount++;
                    
                    // Fix the attribute
                    field.setAttribute('required', 'required');
                    field.setAttribute('data-required', 'true');
                    
                    // Also set the data attribute for consistency
                    field.dataset.required = 'true';
                    
                    console.log(`✅ FIXED: Field ${field.name} now has required="required"`);
                    fixedCount++;
                    
                } else if (requiredValue === 'required') {
                    console.log(`✅ GOOD: Field ${field.name} already has required="required"`);
                    
                    // Ensure data-required is also set
                    if (!field.hasAttribute('data-required')) {
                        field.setAttribute('data-required', 'true');
                        field.dataset.required = 'true';
                    }
                    
                } else if (requiredValue === null || requiredValue === '') {
                    console.log(`⚠️ WARNING: Field ${field.name} has empty required attribute`);
                    
                    // Set proper required attributes
                    field.setAttribute('required', 'required');
                    field.setAttribute('data-required', 'true');
                    field.dataset.required = 'true';
                    
                    console.log(`✅ FIXED: Field ${field.name} now has proper required attributes`);
                    fixedCount++;
                    
                } else {
                    console.log(`⚠️ UNKNOWN: Field ${field.name} has required="${requiredValue}"`);
                    
                    // Convert any other value to proper required attribute
                    field.setAttribute('required', 'required');
                    field.setAttribute('data-required', 'true');
                    field.dataset.required = 'true';
                    
                    console.log(`✅ FIXED: Field ${field.name} converted to required="required"`);
                    fixedCount++;
                }
                
            } catch (error) {
                console.error(`❌ ERROR processing field ${field.name}:`, error);
            }
        });
        
        console.log(`\n📊 Fix Summary:`);
        console.log(`  - Total fields checked: ${requiredFields.length}`);
        console.log(`  - Fields fixed: ${fixedCount}`);
        console.log(`  - Problematic fields found: ${problematicCount}`);
        
        if (problematicCount > 0) {
            console.log(`🎉 Successfully fixed ${problematicCount} problematic required attributes!`);
            console.log(`✅ The "True is not defined" error should no longer occur`);
        } else {
            console.log(`✅ No problematic required attributes found`);
        }
    }
    
    // Function to monitor for dynamically added forms
    function setupFormMonitoring() {
        console.log('Setting up form monitoring...');
        
        // Create a MutationObserver to watch for new forms being added
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            // Check if this is a form or contains forms
                            if (node.tagName === 'FORM' || node.querySelector('form')) {
                                console.log('New form detected, applying fixes...');
                                setTimeout(fixRequiredAttributes, 100);
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
        
        console.log('Form monitoring active');
    }
    
    // Function to run the fix
    function runFix() {
        console.log('Running Branch required attribute fix...');
        
        // Fix existing fields
        fixRequiredAttributes();
        
        // Set up monitoring for new fields
        setupFormMonitoring();
        
        // Also run the fix periodically to catch any missed fields
        setInterval(fixRequiredAttributes, 2000);
        
        console.log('Branch required attribute fix complete');
    }
    
    // Run the fix when the page is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', runFix);
    } else {
        runFix();
    }
    
    // Also run when the page is fully loaded
    window.addEventListener('load', function() {
        console.log('Page fully loaded, running additional fix...');
        setTimeout(fixRequiredAttributes, 500);
    });
    
    // Make the fix function available globally for manual use
    window.fixBranchRequiredAttributes = fixRequiredAttributes;
    
    console.log('Branch required attribute fix ready');
    
})();
