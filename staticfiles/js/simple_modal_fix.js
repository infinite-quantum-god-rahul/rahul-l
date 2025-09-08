// Simple Modal Fix - Bypasses all complex modal logic and just works
console.log('🚀 Simple Modal Fix loaded');

// Override the openEntityModal function with a simple, working version
window.openEntityModal = function(entity) {
    console.log('🚀 Simple Modal Fix: openEntityModal called for', entity);
    
    // Get the base URL
    const base = `/${entity.toLowerCase()}/`;
    const url = `${base}get/`;
    
    console.log('🚀 Fetching from URL:', url);
    
    // Show loading state immediately
    const modal = document.getElementById("entity-modal");
    if (modal) {
        modal.style.display = "flex";
        const title = document.getElementById("entity-modal-title");
        const body = document.getElementById("entity-modal-body");
        
        if (title) title.textContent = `Create ${entity}`;
        if (body) body.innerHTML = '<div class="text-center p-4"><div class="spinner-border" role="status"></div><div class="mt-2">Loading form...</div></div>';
    }
    
    // Fetch the form
    fetch(url, {
        headers: { 
            "X-Requested-With": "XMLHttpRequest", 
            "Accept": "application/json,text/html" 
        },
        credentials: "include"
    })
    .then(async response => {
        console.log('🚀 Response received:', response.status, response.headers.get("content-type"));
        
        if (response.status === 401 || response.status === 403) {
            alert("Authentication required. Please log in again.");
            return;
        }
        
        const contentType = response.headers.get("content-type") || "";
        let html = "";
        
        if (contentType.includes("application/json")) {
            const data = await response.json();
            console.log('🚀 JSON response:', data);
            
            if (data.success && data.html) {
                html = data.html;
            } else {
                alert(data.error || "Failed to load form");
                return;
            }
        } else {
            html = await response.text();
            console.log('🚀 Text response length:', html.length);
        }
        
        if (!html) {
            alert("Empty form response");
            return;
        }
        
        console.log('🚀 Form HTML received, length:', html.length);
        
        // Insert the form content
        if (modal && body) {
            body.innerHTML = html;
            
            // Add footer buttons if they don't exist
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
            
            console.log('🚀 Modal content inserted successfully');
        }
    })
    .catch(error => {
        console.error('🚀 Fetch error:', error);
        alert("Failed to load form: " + error.message);
    });
};

// Override the editEntity function as well
window.editEntity = function(entity, id) {
    console.log('🚀 Simple Modal Fix: editEntity called for', entity, id);
    
    // Get the base URL
    const base = `/${entity.toLowerCase()}/`;
    const url = `${base}get/${id}/`;
    
    console.log('🚀 Fetching from URL:', url);
    
    // Show loading state immediately
    const modal = document.getElementById("entity-modal");
    if (modal) {
        modal.style.display = "flex";
        const title = document.getElementById("entity-modal-title");
        const body = document.getElementById("entity-modal-body");
        
        if (title) title.textContent = `Edit ${entity}`;
        if (body) body.innerHTML = '<div class="text-center p-4"><div class="spinner-border" role="status"></div><div class="mt-2">Loading form...</div></div>';
    }
    
    // Fetch the form
    fetch(url, {
        headers: { 
            "X-Requested-With": "XMLHttpRequest", 
            "Accept": "application/json,text/html" 
        },
        credentials: "include"
    })
    .then(async response => {
        console.log('🚀 Response received:', response.status, response.headers.get("content-type"));
        
        if (response.status === 401 || response.status === 403) {
            alert("Authentication required. Please log in again.");
            return;
        }
        
        const contentType = response.headers.get("content-type") || "";
        let html = "";
        
        if (contentType.includes("application/json")) {
            const data = await response.json();
            console.log('🚀 JSON response:', data);
            
            if (data.success && data.html) {
                html = data.html;
            } else {
                alert(data.error || "Failed to load form");
                return;
            }
        } else {
            html = await response.text();
            console.log('🚀 Text response length:', html.length);
        }
        
        if (!html) {
            alert("Empty form response");
            return;
        }
        
        console.log('🚀 Form HTML received, length:', html.length);
        
        // Insert the form content
        if (modal && body) {
            body.innerHTML = html;
            
            // Add footer buttons if they don't exist
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
            
            console.log('🚀 Modal content inserted successfully');
        }
    })
    .catch(error => {
        console.error('🚀 Fetch error:', error);
        alert("Failed to load form: " + error.message);
    });
};

console.log('🚀 Simple Modal Fix: Functions overridden successfully');
