// EMERGENCY TRUE FIX - Immediate fix for "True is not defined" error
// This script runs immediately and fixes any problematic required attributes

(function() {
    'use strict';
    
    console.log('🚨 EMERGENCY TRUE FIX LOADED - Fixing "True is not defined" error immediately');
    
    // Function to fix required attributes immediately
    function emergencyFixRequiredAttributes() {
        console.log('🔧 Applying emergency fix for required attributes...');
        
        // Find all form fields with required attributes
        const requiredFields = document.querySelectorAll('[required]');
        console.log(`Found ${requiredFields.length} fields with required attribute`);
        
        let fixedCount = 0;
        let problematicCount = 0;
        
        requiredFields.forEach((field, index) => {
            try {
                const requiredValue = field.getAttribute('required');
                console.log(`Field ${index + 1}: ${field.name || field.id || 'unknown'}, required value: "${requiredValue}"`);
                
                // Check if the required attribute has the problematic value
                if (requiredValue === 'True') {
                    console.log(`❌ PROBLEM: Field has required=True (Python boolean)`);
                    problematicCount++;
                    
                    // Fix the attribute immediately
                    field.setAttribute('required', 'required');
                    field.setAttribute('data-required', 'true');
                    
                    // Also set the data attribute for consistency
                    field.dataset.required = 'true';
                    
                    console.log(`✅ EMERGENCY FIXED: Field now has required="required"`);
                    fixedCount++;
                    
                } else if (requiredValue === 'required') {
                    console.log(`✅ GOOD: Field already has required="required"`);
                    
                    // Ensure data-required is also set
                    if (!field.hasAttribute('data-required')) {
                        field.setAttribute('data-required', 'true');
                        field.dataset.required = 'true';
                    }
                    
                } else if (requiredValue === null || requiredValue === '') {
                    console.log(`⚠️ WARNING: Field has empty required attribute`);
                    
                    // Set proper required attributes
                    field.setAttribute('required', 'required');
                    field.setAttribute('data-required', 'true');
                    field.dataset.required = 'true';
                    
                    console.log(`✅ EMERGENCY FIXED: Field now has proper required attributes`);
                    fixedCount++;
                    
                } else {
                    console.log(`⚠️ UNKNOWN: Field has required="${requiredValue}"`);
                    
                    // Convert any other value to proper required attribute
                    field.setAttribute('required', 'required');
                    field.setAttribute('data-required', 'true');
                    field.dataset.required = 'true';
                    
                    console.log(`✅ EMERGENCY FIXED: Field converted to required="required"`);
                    fixedCount++;
                }
                
            } catch (error) {
                console.error(`❌ ERROR processing field:`, error);
            }
        });
        
        console.log(`\n📊 Emergency Fix Summary:`);
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
    function setupEmergencyMonitoring() {
        console.log('🔍 Setting up emergency form monitoring...');
        
        // Create a MutationObserver to watch for new forms being added
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            // Check if this is a form or contains forms
                            if (node.tagName === 'FORM' || node.querySelector('form')) {
                                console.log('🚨 New form detected, applying emergency fixes...');
                                setTimeout(emergencyFixRequiredAttributes, 50);
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
        
        console.log('🚨 Emergency form monitoring active');
    }
    
    // Function to run the emergency fix
    function runEmergencyFix() {
        console.log('🚨 Running EMERGENCY TRUE FIX...');
        
        // Fix existing fields immediately
        emergencyFixRequiredAttributes();
        
        // Set up monitoring for new fields
        setupEmergencyMonitoring();
        
        // Also run the fix very frequently to catch any missed fields
        setInterval(emergencyFixRequiredAttributes, 1000);
        
        console.log('🚨 Emergency TRUE fix complete');
    }
    
    // Run the emergency fix IMMEDIATELY
    console.log('🚨 Starting emergency fix immediately...');
    runEmergencyFix();
    
    // Also run when the page is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🚨 DOM loaded, running additional emergency fix...');
            setTimeout(emergencyFixRequiredAttributes, 100);
        });
    }
    
    // Also run when the page is fully loaded
    window.addEventListener('load', function() {
        console.log('🚨 Page fully loaded, running final emergency fix...');
        setTimeout(emergencyFixRequiredAttributes, 200);
    });
    
    // Make the emergency fix function available globally for manual use
    window.emergencyFixRequiredAttributes = emergencyFixRequiredAttributes;
    
    console.log('🚨 Emergency TRUE fix ready and active');
    
})();
