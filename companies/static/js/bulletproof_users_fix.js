// Bulletproof Users Modal Fix - Handles all timing issues and just works
console.log('🔧 Bulletproof Users Fix loaded - Will solve the hanging issue');

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 DOM ready, setting up Bulletproof Users Fix');
    
    // Function to find modal elements with retry
    function findModalElements() {
        const modal = document.getElementById('entity-modal');
        const title = document.getElementById('entity-modal-title');
        const body = document.getElementById('entity-modal-body');
        
        if (modal && title && body) {
            console.log('🔧 Modal elements found immediately');
            return { modal, title, body };
        }
        
        // If not found, wait and retry
        console.log('🔧 Modal elements not found, waiting...');
        return new Promise((resolve) => {
            setTimeout(() => {
                const retryModal = document.getElementById('entity-modal');
                const retryTitle = document.getElementById('entity-modal-title');
                const retryBody = document.getElementById('entity-modal-body');
                
                if (retryModal && retryTitle && retryBody) {
                    console.log('🔧 Modal elements found after retry');
                    resolve({ modal: retryModal, title: retryTitle, body: retryBody });
                } else {
                    console.error('🔧 Modal elements still not found after retry');
                    resolve(null);
                }
            }, 100);
        });
    }
    
    // Main function to setup the fix
    async function setupBulletproofFix() {
        const elements = await findModalElements();
        if (!elements) {
            console.error('🔧 Cannot setup fix - modal elements not found');
            return;
        }
        
        const { modal, title, body } = elements;
        console.log('🔧 Setting up bulletproof modal fix');
        
        // Store the original function if it exists
        const originalOpenEntityModal = window.openEntityModal;
        
        // Create a new function that only intercepts Users
        window.openEntityModal = function(entity) {
            console.log('🔧 Bulletproof Fix: openEntityModal called for', entity);
            
            // Only intercept Users - let everything else use original function
            if (entity !== 'Users') {
                console.log('🔧 Not Users entity, using original function');
                if (typeof originalOpenEntityModal === 'function') {
                    return originalOpenEntityModal.call(this, entity);
                }
                // If no original function, just return (don't break other functionality)
                return;
            }
            
            console.log('🔧 Users entity detected - using bulletproof handling');
            
            // Ensure modal is visible
            modal.style.display = 'flex';
            modal.style.visibility = 'visible';
            modal.style.opacity = '1';
            
            // Set title
            title.textContent = 'Create Users';
            
            // Show loading with spinner
            body.innerHTML = `
                <div class="text-center p-4">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div class="mt-3">Loading Users form...</div>
                </div>
            `;
            
            // Clear any previous content
            body.style.visibility = 'visible';
            body.style.opacity = '1';
            body.style.display = 'block';
            
            // Fetch form with timeout protection
            const url = '/Users/get/';
            console.log('🔧 Fetching from:', url);
            
            // Create timeout promise
            const timeoutPromise = new Promise((_, reject) => {
                setTimeout(() => reject(new Error('Request timeout - form taking too long')), 15000);
            });
            
            // Create fetch promise
            const fetchPromise = fetch(url, {
                headers: { 
                    "X-Requested-With": "XMLHttpRequest", 
                    "Accept": "application/json,text/html" 
                },
                credentials: "include"
            });
            
            // Race between fetch and timeout
            Promise.race([fetchPromise, timeoutPromise])
            .then(response => {
                console.log('🔧 Response received:', response.status, response.headers.get("content-type"));
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('🔧 Data received:', {success: data.success, error: data.error, htmlLength: data.html?.length});
                
                if (data.success && data.html) {
                    // Insert the form content
                    body.innerHTML = data.html;
                    
                    // Force form visibility
                    const form = body.querySelector('#entity-form');
                    if (form) {
                        form.style.display = 'block';
                        form.style.visibility = 'visible';
                        console.log('🔧 Form element found and made visible');
                    }
                    
                    // Add footer buttons
                    let footer = modal.querySelector('.modal-footer');
                    if (!footer) {
                        footer = document.createElement('div');
                        footer.className = 'modal-footer';
                        footer.innerHTML = `
                            <button type="button" class="btn btn-secondary" onclick="closeEntityModal()">Cancel</button>
                            <button type="submit" class="btn btn-primary" form="entity-form">Save</button>
                        `;
                        modal.querySelector('.modal-content').appendChild(footer);
                    }
                    
                    console.log('🔧 Users form loaded successfully!');
                    
                    // Force a re-render to ensure everything is visible
                    setTimeout(() => {
                        body.style.display = 'none';
                        setTimeout(() => {
                            body.style.display = 'block';
                            console.log('🔧 Forced re-render complete');
                        }, 50);
                    }, 100);
                    
                } else {
                    body.innerHTML = `
                        <div class="alert alert-danger">
                            <h5>Form Load Failed</h5>
                            <p>Error: ${data.error || 'Unknown error occurred'}</p>
                            <button class="btn btn-primary" onclick="window.openEntityModal('Users')">Try Again</button>
                        </div>
                    `;
                    console.error('🔧 Form load failed:', data.error);
                }
            })
            .catch(error => {
                console.error('🔧 Fetch error:', error);
                
                if (error.message.includes('timeout')) {
                    body.innerHTML = `
                        <div class="alert alert-warning">
                            <h5>Form Loading Slowly</h5>
                            <p>The Users form is taking longer than expected. This might be due to database queries.</p>
                            <button class="btn btn-primary" onclick="window.openEntityModal('Users')">Try Again</button>
                            <button class="btn btn-secondary" onclick="closeEntityModal()">Cancel</button>
                        </div>
                    `;
                } else {
                    body.innerHTML = `
                        <div class="alert alert-danger">
                            <h5>Error Loading Form</h5>
                            <p>${error.message}</p>
                            <button class="btn btn-primary" onclick="window.openEntityModal('Users')">Try Again</button>
                            <button class="btn btn-secondary" onclick="closeEntityModal()">Cancel</button>
                        </div>
                    `;
                }
            });
        };
        
        console.log('🔧 Bulletproof Users Fix: openEntityModal function overridden for Users only');
    }
    
    // Setup the fix
    setupBulletproofFix();
});

console.log('🔧 Bulletproof Users Fix: Script loaded successfully');
