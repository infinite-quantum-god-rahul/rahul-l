// Modal Isolation Fix - Complete alternative approach
(function() {
    console.log('=== MODAL ISOLATION FIX LOADING ===');
    
    // Store original functions
    const originalFunctions = {
        openEntityModal: window.openEntityModal,
        editEntity: window.editEntity,
        closeEntityModal: window.closeEntityModal
    };
    
    // Create isolated modal container
    function createIsolatedModal() {
        // Remove existing modal if any
        const existingModal = document.getElementById('entity-modal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // Create new isolated modal
        const modal = document.createElement('div');
        modal.id = 'isolated-entity-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            z-index: 9999;
            display: none;
            overflow-y: auto;
        `;
        
        modal.innerHTML = `
            <div style="
                background: white;
                margin: 2% auto;
                padding: 20px;
                border-radius: 8px;
                width: 90%;
                max-width: 800px;
                max-height: 90vh;
                overflow-y: auto;
                position: relative;
            ">
                <button onclick="window.closeIsolatedModal()" style="
                    position: absolute;
                    top: 10px;
                    right: 15px;
                    background: none;
                    border: none;
                    font-size: 24px;
                    cursor: pointer;
                    color: #666;
                ">&times;</button>
                <div id="isolated-modal-content"></div>
            </div>
        `;
        
        document.body.appendChild(modal);
        return modal;
    }
    
    // Override openEntityModal with isolated version
    window.openEntityModal = function(entity) {
        console.log('Opening isolated modal for:', entity);
        
        const modal = createIsolatedModal();
        const content = document.getElementById('isolated-modal-content');
        
        // Fetch form content
        fetch(`/${entity}/form/`)
            .then(response => response.text())
            .then(html => {
                // Extract form content from response
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const form = doc.querySelector('#entity-form');
                
                if (form) {
                    // Remove any problematic scripts and styles
                    const scripts = form.querySelectorAll('script');
                    scripts.forEach(script => script.remove());
                    
                    const styles = form.querySelectorAll('style');
                    styles.forEach(style => style.remove());
                    
                    // Add isolated styles
                    form.style.cssText = `
                        pointer-events: auto !important;
                        user-select: auto !important;
                    `;
                    
                    // Enable all inputs
                    const inputs = form.querySelectorAll('input, select, textarea');
                    inputs.forEach(input => {
                        input.removeAttribute('readonly');
                        input.removeAttribute('disabled');
                        input.style.cssText = `
                            pointer-events: auto !important;
                            user-select: auto !important;
                            background-color: white !important;
                            cursor: text !important;
                            opacity: 1 !important;
                            color: black !important;
                        `;
                    });
                    
                    content.innerHTML = form.outerHTML;
                    modal.style.display = 'block';
                    
                    // Add isolated event handlers
                    setupIsolatedEventHandlers();
                }
            })
            .catch(error => {
                console.error('Error loading form:', error);
                content.innerHTML = '<p>Error loading form</p>';
                modal.style.display = 'block';
            });
    };
    
    // Override editEntity with isolated version
    window.editEntity = function(entity, id) {
        console.log('Opening isolated edit modal for:', entity, id);
        
        const modal = createIsolatedModal();
        const content = document.getElementById('isolated-modal-content');
        
        // Fetch edit form content
        fetch(`/${entity}/edit/${id}/`)
            .then(response => response.text())
            .then(html => {
                // Extract form content from response
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const form = doc.querySelector('#entity-form');
                
                if (form) {
                    // Remove any problematic scripts and styles
                    const scripts = form.querySelectorAll('script');
                    scripts.forEach(script => script.remove());
                    
                    const styles = form.querySelectorAll('style');
                    styles.forEach(style => style.remove());
                    
                    // Add isolated styles
                    form.style.cssText = `
                        pointer-events: auto !important;
                        user-select: auto !important;
                    `;
                    
                    // Enable all inputs
                    const inputs = form.querySelectorAll('input, select, textarea');
                    inputs.forEach(input => {
                        input.removeAttribute('readonly');
                        input.removeAttribute('disabled');
                        input.style.cssText = `
                            pointer-events: auto !important;
                            user-select: auto !important;
                            background-color: white !important;
                            cursor: text !important;
                            opacity: 1 !important;
                            color: black !important;
                        `;
                    });
                    
                    content.innerHTML = form.outerHTML;
                    modal.style.display = 'block';
                    
                    // Add isolated event handlers
                    setupIsolatedEventHandlers();
                }
            })
            .catch(error => {
                console.error('Error loading edit form:', error);
                content.innerHTML = '<p>Error loading edit form</p>';
                modal.style.display = 'block';
            });
    };
    
    // Setup isolated event handlers
    function setupIsolatedEventHandlers() {
        const modal = document.getElementById('isolated-entity-modal');
        const form = modal.querySelector('#entity-form');
        
        if (form) {
            // Prevent any clicks inside modal from closing it
            modal.addEventListener('click', function(e) {
                e.stopPropagation();
            }, true);
            
            // Handle form submission
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                console.log('Form submitted in isolated modal');
                
                // Get form data
                const formData = new FormData(form);
                
                // Submit via AJAX
                fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.closeIsolatedModal();
                        // Refresh the page or update the list
                        location.reload();
                    } else {
                        alert('Error: ' + (data.message || 'Unknown error'));
                    }
                })
                .catch(error => {
                    console.error('Error submitting form:', error);
                    alert('Error submitting form');
                });
            });
            
            // Handle Enter key submission
            form.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
                    e.preventDefault();
                    form.dispatchEvent(new Event('submit'));
                }
            });
        }
    }
    
    // Close isolated modal
    window.closeIsolatedModal = function() {
        const modal = document.getElementById('isolated-entity-modal');
        if (modal) {
            modal.style.display = 'none';
        }
    };
    
    // Override closeEntityModal to work with isolated modal
    window.closeEntityModal = function() {
        window.closeIsolatedModal();
    };
    
    console.log('=== MODAL ISOLATION FIX LOADED ===');
})();







