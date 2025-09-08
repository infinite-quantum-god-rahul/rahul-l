// Users-Specific Modal Fix - Bypasses the complex form queries that cause hanging
console.log('🔧 Users-Specific Fix loaded - Will handle Users entity without hanging');

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 DOM ready, setting up Users-Specific Fix');
    
    // Find the modal elements
    const modal = document.getElementById('entity-modal');
    const title = document.getElementById('entity-modal-title');
    const body = document.getElementById('entity-modal-body');
    
    if (!modal || !title || !body) {
        console.error('🔧 Modal elements not found');
        return;
    }
    
    console.log('🔧 Modal elements found:', {modal: !!modal, title: !!title, body: !!body});
    
    // Override ONLY the Users modal - leave other entities alone
    const originalOpenEntityModal = window.openEntityModal;
    
    window.openEntityModal = function(entity) {
        console.log('🔧 Users-Specific Fix: openEntityModal called for', entity);
        
        // Only intercept Users - let other entities use original function
        if (entity !== 'Users') {
            console.log('🔧 Not Users entity, using original function');
            if (typeof originalOpenEntityModal === 'function') {
                return originalOpenEntityModal.call(this, entity);
            }
            return;
        }
        
        console.log('🔧 Users entity detected - using special handling');
        
        // Set modal title
        title.textContent = `Create ${entity}`;
        
        // Show loading state
        modal.style.display = 'flex';
        body.innerHTML = '<div class="text-center p-4"><div class="spinner-border" role="status"></div><div class="mt-2">Loading Users form...</div></div>';
        
        // Fetch the form with a timeout to prevent hanging
        const url = '/Users/get/';
        console.log('🔧 Fetching from:', url);
        
        // Add timeout to prevent hanging
        const timeoutPromise = new Promise((_, reject) => {
            setTimeout(() => reject(new Error('Request timeout - Users form taking too long')), 10000); // 10 second timeout
        });
        
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
            return response.json();
        })
        .then(data => {
            console.log('🔧 Data received:', {success: data.success, error: data.error, htmlLength: data.html?.length});
            
            if (data.success && data.html) {
                // Insert the form content
                body.innerHTML = data.html;
                
                // Ensure the form is visible
                body.style.visibility = 'visible';
                body.style.opacity = '1';
                body.style.display = 'block';
                
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
                
            } else {
                body.innerHTML = `<div class="alert alert-danger">Error: ${data.error || 'Failed to load form'}</div>`;
                console.error('🔧 Form load failed:', data.error);
            }
        })
        .catch(error => {
            console.error('🔧 Fetch error:', error);
            if (error.message.includes('timeout')) {
                body.innerHTML = `
                    <div class="alert alert-warning">
                        <h5>Users Form Loading Slowly</h5>
                        <p>The Users form is taking longer than expected to load. This might be due to complex database queries.</p>
                        <button class="btn btn-primary" onclick="window.openEntityModal('Users')">Try Again</button>
                        <button class="btn btn-secondary" onclick="closeEntityModal()">Cancel</button>
                    </div>
                `;
            } else {
                body.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
            }
        });
    };
    
    console.log('🔧 Users-Specific Fix: openEntityModal function overridden for Users only');
});

console.log('🔧 Users-Specific Fix: Script loaded successfully');
