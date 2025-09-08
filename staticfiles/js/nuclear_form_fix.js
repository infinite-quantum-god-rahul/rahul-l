// NUCLEAR FORM FIX - COMPLETE OVERRIDE SOLUTION
(function() {
    console.log('=== NUCLEAR FORM FIX LOADING ===');
    
    // Wait for page to load completely
    function waitForLoad() {
        if (document.readyState === 'complete') {
            applyNuclearFix();
        } else {
            window.addEventListener('load', applyNuclearFix);
        }
    }
    
    function applyNuclearFix() {
        console.log('🚀 APPLYING NUCLEAR FORM FIX...');
        
        // COMPLETE OVERRIDE - Force all forms to open in new windows
        window.openEntityModal = function(entity) {
            console.log('🔥 NUCLEAR: Opening form in new window for:', entity);
            const url = `/${entity}/form/`;
            const newWindow = window.open(url, '_blank', 'width=900,height=700,scrollbars=yes,resizable=yes,menubar=no,toolbar=no');
            if (newWindow) {
                newWindow.focus();
            } else {
                alert('Please allow popups for this site to use forms');
            }
        };
        
        window.editEntity = function(entity, id) {
            console.log('🔥 NUCLEAR: Opening edit form in new window for:', entity, id);
            const url = `/${entity}/edit/${id}/`;
            const newWindow = window.open(url, '_blank', 'width=900,height=700,scrollbars=yes,resizable=yes,menubar=no,toolbar=no');
            if (newWindow) {
                newWindow.focus();
            } else {
                alert('Please allow popups for this site to use forms');
            }
        };
        
        // Override any existing modal functions
        window.closeEntityModal = function() {
            console.log('🔥 NUCLEAR: Modal close requested - ignored');
        };
        
        // Find and override all click handlers that might open modals
        const allButtons = document.querySelectorAll('button, a, [data-entity], [data-action]');
        allButtons.forEach(button => {
            const originalClick = button.onclick;
            button.onclick = function(e) {
                // Check if this button should open a form
                const entity = button.getAttribute('data-entity') || 
                              button.getAttribute('data-action') ||
                              button.textContent.toLowerCase();
                
                if (entity && (entity.includes('add') || entity.includes('new') || entity.includes('edit'))) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Extract entity name from various sources
                    let entityName = null;
                    if (button.getAttribute('data-entity')) {
                        entityName = button.getAttribute('data-entity');
                    } else if (button.closest('[data-entity]')) {
                        entityName = button.closest('[data-entity]').getAttribute('data-entity');
                    } else if (button.textContent.toLowerCase().includes('staff')) {
                        entityName = 'staff';
                    } else if (button.textContent.toLowerCase().includes('client')) {
                        entityName = 'client';
                    } else if (button.textContent.toLowerCase().includes('group')) {
                        entityName = 'group';
                    } else if (button.textContent.toLowerCase().includes('center')) {
                        entityName = 'center';
                    } else if (button.textContent.toLowerCase().includes('village')) {
                        entityName = 'village';
                    } else if (button.textContent.toLowerCase().includes('branch')) {
                        entityName = 'branch';
                    }
                    
                    if (entityName) {
                        console.log('🔥 NUCLEAR: Intercepted button click for entity:', entityName);
                        window.openEntityModal(entityName);
                        return false;
                    }
                }
                
                // Call original handler if it exists
                if (typeof originalClick === 'function') {
                    return originalClick.call(this, e);
                }
            };
        });
        
        // Override any existing event listeners
        const originalAddEventListener = EventTarget.prototype.addEventListener;
        EventTarget.prototype.addEventListener = function(type, listener, options) {
            // Block any modal-related event listeners
            if (type === 'click' && listener.toString().includes('modal')) {
                console.log('🚫 NUCLEAR: Blocked modal event listener');
                return;
            }
            return originalAddEventListener.call(this, type, listener, options);
        };
        
        // Remove any existing modals
        const existingModals = document.querySelectorAll('#entity-modal, .modal, [id*="modal"]');
        existingModals.forEach(modal => {
            console.log('🗑️ NUCLEAR: Removing existing modal:', modal.id);
            modal.remove();
        });
        
        // Add visual indicator that nuclear fix is active
        const indicator = document.createElement('div');
        indicator.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            background: #28a745;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 10000;
            font-weight: bold;
        `;
        indicator.textContent = '🔥 NUCLEAR FIX ACTIVE';
        document.body.appendChild(indicator);
        
        console.log('✅ NUCLEAR FORM FIX APPLIED SUCCESSFULLY');
    }
    
    // Apply fix immediately and also on load
    applyNuclearFix();
    waitForLoad();
    
    // Also apply on DOM content loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applyNuclearFix);
    }
    
    console.log('=== NUCLEAR FORM FIX LOADED ===');
})();







