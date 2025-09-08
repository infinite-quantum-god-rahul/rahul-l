// Universal Modal Fix - Works for ALL entities (Users, Prepaid, Mortgage, ExSaving, etc.)
console.log('🔧 Universal Modal Fix loaded - Will handle ALL entities');

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 DOM ready, setting up Universal Modal Fix');
    
    // Find the modal elements
    const modal = document.getElementById('entity-modal');
    const title = document.getElementById('entity-modal-title');
    const body = document.getElementById('entity-modal-body');
    
    if (!modal || !title || !body) {
        console.error('🔧 Modal elements not found');
        return;
    }
    
    console.log('🔧 Modal elements found:', {modal: !!modal, title: !!title, body: !!body});
    
    // Override the openEntityModal function for ALL entities
    window.openEntityModal = function(entity) {
        console.log('🔧 Universal Modal Fix: openEntityModal called for', entity);
        
        // Set modal title
        title.textContent = `Create ${entity}`;
        
        // Show loading state
        modal.style.display = 'flex';
        body.innerHTML = `<div class="text-center p-4"><div class="spinner-border" role="status"></div><div class="mt-2">Loading ${entity} form...</div></div>`;
        
        // Fetch the form for ANY entity
        const url = `/${entity}/get/`;
        console.log('🔧 Fetching from:', url);
        
        fetch(url, {
            headers: { 
                "X-Requested-With": "XMLHttpRequest", 
                "Accept": "application/json,text/html" 
            },
            credentials: "include"
        })
        .then(response => {
            console.log('🔧 Response received:', response.status, response.headers.get("content-type"));
            return response.json();
        })
        .then(data => {
            console.log('🔧 Data received:', {success: data.success, error: data.error, htmlLength: data.html?.length});
            
            if (data.success && data.html) {
                // DEBUG: Log what we're about to insert
                console.log('🔧 About to insert HTML:', data.html.substring(0, 200) + '...');
                
                // Insert the form content
                body.innerHTML = data.html;
                
                // DEBUG: Check what's actually in the body now
                console.log('🔧 Body content after insertion:', body.innerHTML.substring(0, 200) + '...');
                console.log('🔧 Body children count:', body.children.length);
                console.log('🔧 Body first child:', body.firstElementChild);
                
                // Ensure the form is visible
                body.style.visibility = 'visible';
                body.style.opacity = '1';
                body.style.display = 'block';
                
                // Add some basic styling to ensure form elements are visible
                const form = body.querySelector('#entity-form');
                if (form) {
                    form.style.display = 'block';
                    form.style.visibility = 'visible';
                    console.log('🔧 Form element found and styled');
                } else {
                    console.error('🔧 Form element not found in body');
                }
                
                // Check all form fields
                const formFields = body.querySelectorAll('input, select, textarea, label');
                console.log('🔧 Found form fields:', formFields.length);
                formFields.forEach((field, index) => {
                    if (index < 5) { // Log first 5 fields
                        console.log('🔧 Field:', field.tagName, field.type || 'N/A', field.name || 'N/A');
                    }
                });
                
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
                
                console.log('🔧 Form loaded successfully for:', entity);
                
                // DEBUG: Force a re-render
                body.style.display = 'none';
                setTimeout(() => {
                    body.style.display = 'block';
                    console.log('🔧 Forced re-render of modal body');
                }, 100);
                
            } else {
                body.innerHTML = `<div class="alert alert-danger">Error: ${data.error || 'Failed to load form'}</div>`;
                console.error('🔧 Form load failed:', data.error);
            }
        })
        .catch(error => {
            console.error('🔧 Fetch error:', error);
            body.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        });
    };
    
    // Also override editEntity for editing existing records
    window.editEntity = function(entity, id) {
        console.log('🔧 Universal Modal Fix: editEntity called for', entity, 'ID:', id);
        
        // Set modal title
        title.textContent = `Edit ${entity}`;
        
        // Show loading state
        modal.style.display = 'flex';
        body.innerHTML = `<div class="text-center p-4"><div class="spinner-border" role="status"></div><div class="mt-2">Loading ${entity} data...</div></div>`;
        
        // Fetch the form with existing data
        const url = `/${entity}/get/?id=${id}`;
        console.log('🔧 Fetching edit data from:', url);
        
        fetch(url, {
            headers: { 
                "X-Requested-With": "XMLHttpRequest", 
                "Accept": "application/json,text/html" 
            },
            credentials: "include"
        })
        .then(response => {
            console.log('🔧 Response received:', response.status, response.headers.get("content-type"));
            return response.json();
        })
        .then(data => {
            console.log('🔧 Edit data received:', {success: data.success, error: data.error, htmlLength: data.html?.length});
            
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
                        <button type="submit" class="btn btn-primary" form="entity-form">Update</button>
                    `;
                    modal.querySelector('.modal-content').appendChild(footer);
                }
                
                console.log('🔧 Edit form loaded successfully for:', entity);
                
            } else {
                body.innerHTML = `<div class="alert alert-danger">Error: ${data.error || 'Failed to load edit form'}</div>`;
                console.error('🔧 Edit form load failed:', data.error);
            }
        })
        .catch(error => {
            console.error('🔧 Edit fetch error:', error);
            body.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        });
    };
    
    console.log('🔧 Universal Modal Fix: Both openEntityModal and editEntity functions overridden');
});

console.log('🔧 Universal Modal Fix: Script loaded successfully');
