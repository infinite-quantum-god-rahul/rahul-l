// Simple Form Fix - Replace modal with simple form approach
(function() {
    console.log('=== SIMPLE FORM FIX LOADING ===');
    
    // Store original functions
    const originalFunctions = {
        openEntityModal: window.openEntityModal,
        editEntity: window.editEntity
    };
    
    // Override openEntityModal to open in new window
    window.openEntityModal = function(entity) {
        console.log('Opening simple form for:', entity);
        
        // Open form in new window
        const formWindow = window.open(`/${entity}/form/`, '_blank', 
            'width=800,height=600,scrollbars=yes,resizable=yes');
        
        // Focus the new window
        if (formWindow) {
            formWindow.focus();
        }
    };
    
    // Override editEntity to open in new window
    window.editEntity = function(entity, id) {
        console.log('Opening simple edit form for:', entity, id);
        
        // Open edit form in new window
        const formWindow = window.open(`/${entity}/edit/${id}/`, '_blank', 
            'width=800,height=600,scrollbars=yes,resizable=yes');
        
        // Focus the new window
        if (formWindow) {
            formWindow.focus();
        }
    };
    
    console.log('=== SIMPLE FORM FIX LOADED ===');
})();





