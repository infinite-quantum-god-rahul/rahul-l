// Iframe Modal Fix - Use iframe to isolate form from main page conflicts
(function() {
    console.log('=== IFRAME MODAL FIX LOADING ===');
    
    // Store original functions
    const originalFunctions = {
        openEntityModal: window.openEntityModal,
        editEntity: window.editEntity,
        closeEntityModal: window.closeEntityModal
    };
    
    // Create iframe modal container
    function createIframeModal() {
        // Remove existing modal if any
        const existingModal = document.getElementById('entity-modal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // Create new iframe modal
        const modal = document.createElement('div');
        modal.id = 'iframe-entity-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            z-index: 9999;
            display: none;
        `;
        
        modal.innerHTML = `
            <div style="
                background: white;
                margin: 2% auto;
                border-radius: 8px;
                width: 95%;
                height: 90vh;
                position: relative;
                overflow: hidden;
            ">
                <button onclick="window.closeIframeModal()" style="
                    position: absolute;
                    top: 10px;
                    right: 15px;
                    background: #dc3545;
                    border: none;
                    font-size: 18px;
                    cursor: pointer;
                    color: white;
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    z-index: 10000;
                ">&times;</button>
                <iframe id="form-iframe" style="
                    width: 100%;
                    height: 100%;
                    border: none;
                    border-radius: 8px;
                "></iframe>
            </div>
        `;
        
        document.body.appendChild(modal);
        return modal;
    }
    
    // Override openEntityModal with iframe version
    window.openEntityModal = function(entity) {
        console.log('Opening iframe modal for:', entity);
        
        const modal = createIframeModal();
        const iframe = document.getElementById('form-iframe');
        
        // Load form in iframe
        iframe.src = `/${entity}/form/`;
        modal.style.display = 'block';
        
        // Listen for messages from iframe
        window.addEventListener('message', function(event) {
            if (event.data.type === 'formSubmitted') {
                window.closeIframeModal();
                location.reload();
            }
        });
    };
    
    // Override editEntity with iframe version
    window.editEntity = function(entity, id) {
        console.log('Opening iframe edit modal for:', entity, id);
        
        const modal = createIframeModal();
        const iframe = document.getElementById('form-iframe');
        
        // Load edit form in iframe
        iframe.src = `/${entity}/edit/${id}/`;
        modal.style.display = 'block';
        
        // Listen for messages from iframe
        window.addEventListener('message', function(event) {
            if (event.data.type === 'formSubmitted') {
                window.closeIframeModal();
                location.reload();
            }
        });
    };
    
    // Close iframe modal
    window.closeIframeModal = function() {
        const modal = document.getElementById('iframe-entity-modal');
        if (modal) {
            modal.style.display = 'none';
        }
    };
    
    // Override closeEntityModal to work with iframe modal
    window.closeEntityModal = function() {
        window.closeIframeModal();
    };
    
    console.log('=== IFRAME MODAL FIX LOADED ===');
})();





