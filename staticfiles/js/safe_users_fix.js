// Safe Users Modal Fix - No function overrides, just event listening
console.log('🔧 Safe Users Fix loaded - No function overrides');

// Flag to prevent multiple simultaneous requests
let isRequestInProgress = false;

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 DOM ready, setting up Safe Users Fix');
    
    // Function to find modal elements
    function findModalElements() {
        const modal = document.getElementById('entity-modal');
        const title = document.getElementById('entity-modal-title');
        const body = document.getElementById('entity-modal-body');
        
        if (modal && title && body) {
            console.log('🔧 Modal elements found');
            return { modal, title, body };
        }
        
        console.error('🔧 Modal elements not found');
        return null;
    }
    
    // Function to handle Users modal
    function handleUsersModal() {
        // Prevent multiple simultaneous requests
        if (isRequestInProgress) {
            console.log('🔧 Request already in progress, skipping');
            return;
        }
        
        console.log('🔧 Safe Fix: Handling Users modal');
        
        const elements = findModalElements();
        if (!elements) {
            console.error('🔧 Cannot handle Users modal - elements not found');
            return;
        }
        
        const { modal, title, body } = elements;
        
        // Set title
        title.textContent = 'Create Users';
        
        // Show modal
        modal.style.display = 'flex';
        
        // Show loading
        body.innerHTML = `
            <div class="text-center p-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <div class="mt-3">Loading Users form...</div>
            </div>
        `;
        
        // Set request flag
        isRequestInProgress = true;
        
        // Fetch form
        fetch('/UserCreation/get/', {
            headers: { 
                "X-Requested-With": "XMLHttpRequest", 
                "Accept": "application/json,text/html" 
            },
            credentials: "include"
        })
        .then(response => {
            console.log('🔧 Response received:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('🔧 Data received:', {success: data.success, htmlLength: data.html?.length});
            
            if (data.success && data.html) {
                // Insert form content
                body.innerHTML = data.html;
                
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
                body.innerHTML = `
                    <div class="alert alert-danger">
                        <h5>Form Load Failed</h5>
                        <p>Error: ${data.error || 'Unknown error occurred'}</p>
                        <button class="btn btn-primary" onclick="handleUsersModal()">Try Again</button>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('🔧 Fetch error:', error);
            body.innerHTML = `
                <div class="alert alert-danger">
                    <h5>Error Loading Form</h5>
                    <p>${error.message}</p>
                    <button class="btn btn-primary" onclick="handleUsersModal()">Try Again</button>
                    <button class="btn btn-secondary" onclick="closeEntityModal()">Cancel</button>
                </div>
            `;
        })
        .finally(() => {
            // Reset request flag
            isRequestInProgress = false;
        });
    }
    
    // Make the function globally accessible
    window.handleUsersModal = handleUsersModal;
    
    // Find and intercept ONLY the main Users "Add" button
    function setupButtonInterception() {
        // Look for the specific button that opens Users modal
        // Be more specific to avoid intercepting wrong buttons
        const buttons = document.querySelectorAll('button, a, .btn');
        
        console.log('🔧 Total buttons found:', buttons.length);
        
        buttons.forEach((button, index) => {
            // Check if this button is specifically for adding Users
            const text = (button.textContent || button.innerText || '').toLowerCase();
            const onclick = button.getAttribute('onclick') || '';
            const href = button.getAttribute('href') || '';
            
            // Log ALL buttons to see what we're working with
            if (index < 10) { // Log first 10 buttons
                console.log(`🔧 Button ${index}: text="${text}", onclick="${onclick}", href="${href}"`);
            }
            
            // Only intercept very specific User Creation buttons
            if ((text.includes('add user') || text.includes('+ user') || text.includes('user creation') || text.includes('create user')) && 
                (onclick.includes('openEntityModal') || onclick.includes('UserCreation'))) {
                
                console.log('🔧 Found main Users button:', button);
                console.log('🔧 Button text:', text);
                console.log('🔧 Button onclick:', onclick);
                
                // Remove any existing onclick
                button.removeAttribute('onclick');
                
                // Add new click handler
                button.addEventListener('click', function(e) {
                    console.log('🔧 Users button clicked!');
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('🔧 Main Users button clicked - using safe handler');
                    handleUsersModal();
                });
                
                // Mark this button as handled
                button.setAttribute('data-users-handled', 'true');
                
                // Test if the button is actually clickable
                console.log('🔧 Button click handler added successfully');
            }
        });
    }
    
    // Setup button interception
    setupButtonInterception();
    
    // Also watch for dynamically added buttons (but be more selective)
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                // Only setup if we haven't found the main button yet
                const mainButton = document.querySelector('[data-users-handled="true"]');
                if (!mainButton) {
                    setupButtonInterception();
                }
            }
        });
    });
    
    observer.observe(document.body, { childList: true, subtree: true });
    
    console.log('🔧 Safe Users Fix: Setup complete - no global functions overridden');
});

console.log('🔧 Safe Users Fix: Script loaded successfully');
