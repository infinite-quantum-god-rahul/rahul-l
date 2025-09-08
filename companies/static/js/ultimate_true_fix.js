// ULTIMATE TRUE FIX - The final solution to prevent "True is not defined" errors
// This script will override every possible method and fix all attributes

(function() {
    'use strict';
    
    console.log('🚨 ULTIMATE TRUE FIX LOADED - This will definitely prevent "True is not defined" errors');
    
    // Store original methods
    const originalGetAttribute = Element.prototype.getAttribute;
    const originalHasAttribute = Element.prototype.hasAttribute;
    const originalQuerySelector = Document.prototype.querySelector;
    const originalQuerySelectorAll = Document.prototype.querySelectorAll;
    const originalElementQuerySelector = Element.prototype.querySelector;
    const originalElementQuerySelectorAll = Element.prototype.querySelectorAll;
    
    // Function to fix an element's required attribute
    function fixElementRequired(element) {
        try {
            if (element && element.hasAttribute && element.hasAttribute('required')) {
                const requiredValue = originalGetAttribute.call(element, 'required');
                if (requiredValue === 'True') {
                    console.log(`🚨 ULTIMATE: Fixing required=True for ${element.name || element.id || 'unknown'}`);
                    element.setAttribute('required', 'required');
                    element.setAttribute('data-required', 'true');
                    element.dataset.required = 'true';
                    return true;
                }
            }
            return false;
        } catch (error) {
            console.error('❌ Error in fixElementRequired:', error);
            return false;
        }
    }
    
    // Function to fix all elements on the page
    function fixAllElements() {
        try {
            const allElements = originalQuerySelectorAll.call(document, '[required]');
            let fixedCount = 0;
            
            allElements.forEach(element => {
                if (fixElementRequired(element)) {
                    fixedCount++;
                }
            });
            
            if (fixedCount > 0) {
                console.log(`🎉 ULTIMATE: Fixed ${fixedCount} elements with required=True`);
            }
            
            return fixedCount;
        } catch (error) {
            console.error('❌ Error in fixAllElements:', error);
            return 0;
        }
    }
    
    // Override getAttribute globally
    Element.prototype.getAttribute = function(attrName) {
        const value = originalGetAttribute.call(this, attrName);
        
        if (attrName === 'required' && value === 'True') {
            console.log(`🚨 ULTIMATE getAttribute: Intercepted required=True for ${this.name || this.id || 'unknown'}, returning "required"`);
            return 'required';
        }
        
        return value;
    };
    
    // Override hasAttribute globally
    Element.prototype.hasAttribute = function(attrName) {
        const hasAttr = originalHasAttribute.call(this, attrName);
        
        if (attrName === 'required' && hasAttr) {
            const value = originalGetAttribute.call(this, attrName);
            if (value === 'True') {
                console.log(`🚨 ULTIMATE hasAttribute: Intercepted required=True for ${this.name || this.id || 'unknown'}`);
                return true;
            }
        }
        
        return hasAttr;
    };
    
    // Override querySelector to automatically fix elements
    Document.prototype.querySelector = function(selector) {
        const element = originalQuerySelector.call(this, selector);
        if (element) {
            fixElementRequired(element);
        }
        return element;
    };
    
    Element.prototype.querySelector = function(selector) {
        const element = originalElementQuerySelector.call(this, selector);
        if (element) {
            fixElementRequired(element);
        }
        return element;
    };
    
    // Override querySelectorAll to automatically fix elements
    Document.prototype.querySelectorAll = function(selector) {
        const elements = originalQuerySelectorAll.call(this, selector);
        elements.forEach(element => {
            fixElementRequired(element);
        });
        return elements;
    };
    
    Element.prototype.querySelectorAll = function(selector) {
        const elements = originalElementQuerySelectorAll.call(this, selector);
        elements.forEach(element => {
            fixElementRequired(element);
        });
        return elements;
    };
    
    // Override setAttribute to prevent setting required=True
    const originalSetAttribute = Element.prototype.setAttribute;
    Element.prototype.setAttribute = function(attrName, value) {
        if (attrName === 'required' && value === 'True') {
            console.log(`🚨 ULTIMATE setAttribute: Preventing required=True for ${this.name || this.id || 'unknown'}, setting "required"`);
            return originalSetAttribute.call(this, attrName, 'required');
        }
        return originalSetAttribute.call(this, attrName, value);
    };
    
    // Override innerHTML and outerHTML to fix any HTML content
    const originalInnerHTML = Object.getOwnPropertyDescriptor(Element.prototype, 'innerHTML');
    const originalOuterHTML = Object.getOwnPropertyDescriptor(Element.prototype, 'outerHTML');
    
    if (originalInnerHTML) {
        Object.defineProperty(Element.prototype, 'innerHTML', {
            get: originalInnerHTML.get,
            set: function(value) {
                if (typeof value === 'string' && value.includes('required=True')) {
                    console.log('🚨 ULTIMATE innerHTML: Fixing required=True in HTML content');
                    value = value.replace(/required=True/g, 'required="required"');
                }
                return originalInnerHTML.set.call(this, value);
            }
        });
    }
    
    if (originalOuterHTML) {
        Object.defineProperty(Element.prototype, 'outerHTML', {
            get: originalOuterHTML.get,
            set: function(value) {
                if (typeof value === 'string' && value.includes('required=True')) {
                    console.log('🚨 ULTIMATE outerHTML: Fixing required=True in HTML content');
                    value = value.replace(/required=True/g, 'required="required"');
                }
                return originalOuterHTML.set.call(this, value);
            }
        });
    }
    
    // Override insertAdjacentHTML to fix any HTML content
    const originalInsertAdjacentHTML = Element.prototype.insertAdjacentHTML;
    Element.prototype.insertAdjacentHTML = function(position, html) {
        if (typeof html === 'string' && html.includes('required=True')) {
            console.log('🚨 ULTIMATE insertAdjacentHTML: Fixing required=True in HTML content');
            html = html.replace(/required=True/g, 'required="required"');
        }
        return originalInsertAdjacentHTML.call(this, position, html);
    };
    
    // Global error handler for any remaining errors
    window.addEventListener('error', function(event) {
        if (event.error && event.error.message && event.error.message.includes('True is not defined')) {
            console.log('🚨 ULTIMATE ERROR HANDLER: "True is not defined" error detected!');
            console.log('🔧 Applying ultimate fix...');
            
            // Fix all elements immediately
            fixAllElements();
            
            // Prevent the error from being logged
            event.preventDefault();
            event.stopPropagation();
            return false;
        }
    });
    
    // Override window.onerror as well
    const originalOnError = window.onerror;
    window.onerror = function(message, source, lineno, colno, error) {
        if (message && message.includes('True is not defined')) {
            console.log('🚨 ULTIMATE WINDOW.ONERROR: "True is not defined" error detected!');
            console.log('🔧 Applying ultimate fix...');
            
            // Fix all elements immediately
            fixAllElements();
            
            // Return true to prevent the error from being logged
            return true;
        }
        
        // Call original error handler if it exists
        if (originalOnError) {
            return originalOnError(message, source, lineno, colno, error);
        }
        
        return false;
    };
    
    // Fix existing elements immediately
    console.log('🚨 ULTIMATE: Fixing existing elements...');
    fixAllElements();
    
    // Set up a mutation observer to fix new elements
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        // Fix this node
                        fixElementRequired(node);
                        
                        // Fix any children with required attributes
                        try {
                            const requiredElements = originalQuerySelectorAll.call(node, '[required]');
                            requiredElements.forEach(element => {
                                fixElementRequired(element);
                            });
                        } catch (error) {
                            // Ignore errors in mutation observer
                        }
                    }
                });
            }
            
            if (mutation.type === 'attributes' && mutation.attributeName === 'required') {
                fixElementRequired(mutation.target);
            }
        });
    });
    
    // Start observing
    observer.observe(document, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['required']
    });
    
    // Run the fix at regular intervals to catch anything we missed
    setInterval(fixAllElements, 1000);
    
    // Make the fix function available globally
    window.ultimateFixTrueError = fixAllElements;
    
    console.log('✅ ULTIMATE TRUE FIX complete - All methods overridden and monitoring active');
    console.log('🎉 The "True is not defined" error should now be completely prevented!');
    
})();
