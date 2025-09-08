// Minimal Users Modal Fix - Just works, no complexity
console.log('🔧 Minimal Users Fix loaded');

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 DOM ready, setting up Minimal Users Fix');
    
    // Find the modal elements
    const modal = document.getElementById('entity-modal');
    const title = document.getElementById('entity-modal-title');
    const body = document.getElementById('entity-modal-body');
    
    if (!modal || !title || !body) {
        console.error('🔧 Modal elements not found');
        return;
    }
    
    console.log('🔧 Modal elements found');
    
    // Simple, direct function override
    window.openEntityModal = function(entity) {
        console.log('🔧 Minimal Fix: openEntityModal called for', entity);
        
        // Only handle Users
        if (entity !== 'Users') {
            console.log('🔧 Not Users, skipping');
            return;
        }
        
        console.log('🔧 Handling Users modal');
        
        // Set title
        title.textContent = 'Create Users';
        
        // Show modal
        modal.style.display = 'flex';
        
        // Show loading
        body.innerHTML = '<div class="text-center p-4"><div class="spinner-border"></div><div class="mt-2">Loading...</div></div>';
        
        // Simple fetch
        fetch('/Users/get/')
        .then(response => response.json())
        .then(data => {
            console.log('🔧 Form data received:', data.success);
            
            if (data.success && data.html) {
                // Insert form
                body.innerHTML = data.html;
                
                // Add buttons
                const footer = document.createElement('div');
                footer.className = 'modal-footer';
                footer.innerHTML = `
                    <button type="button" class="btn btn-secondary" onclick="closeEntityModal()">Cancel</button>
                    <button type="submit" class="btn btn-primary" form="entity-form">Save</button>
                `;
                modal.querySelector('.modal-content').appendChild(footer);
                
                console.log('🔧 Users form loaded successfully!');
            } else {
                body.innerHTML = '<div class="alert alert-danger">Failed to load form</div>';
            }
        })
        .catch(error => {
            console.error('🔧 Error:', error);
            body.innerHTML = '<div class="alert alert-danger">Error loading form</div>';
        });
    };
    
    console.log('🔧 Minimal Users Fix: Function overridden');
});

console.log('🔧 Minimal Users Fix: Script loaded');
