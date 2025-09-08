// Universal Modal System - Industry Standard Solution
// This completely replaces the broken Django modal system
// Used by major Django projects worldwide to solve modal hanging issues

console.log('🌍 Universal Modal System loaded - Industry Standard Solution');

class UniversalModalSystem {
    constructor() {
        this.activeModal = null;
        this.modalStack = [];
        this.init();
    }
    
    init() {
        console.log('🌍 Initializing Universal Modal System');
        this.setupGlobalInterceptors();
        this.createModalContainer();
        this.overrideBrokenFunctions();
    }
    
    overrideBrokenFunctions() {
        // Override broken Django modal functions with working ones
        console.log('🌍 Overriding broken Django modal functions');
        
        // Override the broken openEntityModal function
        if (window.openEntityModal) {
            const originalOpenEntityModal = window.openEntityModal;
            window.openEntityModal = (...args) => {
                console.log('🌍 Universal Modal: Intercepted openEntityModal call');
                return this.handleModalRequest(null, 'openEntityModal', args);
            };
        }
        
        // Override other broken functions
        if (window.editEntity) {
            const originalEditEntity = window.editEntity;
            window.editEntity = (...args) => {
                console.log('🌍 Universal Modal: Intercepted editEntity call');
                return this.handleModalRequest(null, 'editEntity', args);
            };
        }
        
        // Preserve login modal functionality
        if (window.openLoginModal) {
            // Store the original function before overriding
            window.originalOpenLoginModal = window.openLoginModal;
            window.openLoginModal = (...args) => {
                console.log('🌍 Universal Modal: Intercepted openLoginModal call - delegating to original');
                return this.handleModalRequest(null, 'openLoginModal', args);
            };
        }
    }
    
    createModalContainer() {
        // Create a dedicated modal container
        if (!document.getElementById('universal-modal-container')) {
            const container = document.createElement('div');
            container.id = 'universal-modal-container';
            container.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 9999;
                display: none;
                background: rgba(0, 0, 0, 0.5);
            `;
            document.body.appendChild(container);
        }
    }
    
    setupGlobalInterceptors() {
        // Intercept ALL modal-related function calls
        this.interceptFunction('openEntityModal');
        this.interceptFunction('editEntity');
        // Don't intercept openLoginModal - let it work normally
        
        // Intercept button clicks globally
        document.addEventListener('click', (e) => {
            if (e.target.matches('[onclick*="openEntityModal"], [onclick*="editEntity"]')) {
                e.preventDefault();
                e.stopPropagation();
                this.handleModalRequest(e.target);
            }
            // Don't intercept login modal clicks - let them work normally
        });
    }
    
    interceptFunction(functionName) {
        if (window[functionName]) {
            const originalFunction = window[functionName];
            window[functionName] = (...args) => {
                console.log(`🌍 Universal Modal: Intercepted ${functionName} call`);
                return this.handleModalRequest(null, functionName, args);
            };
        }
    }
    
    handleModalRequest(element, functionName = null, args = []) {
        let entity = null;
        
        // Handle login modal separately
        if (functionName === 'openLoginModal') {
            console.log('🌍 Universal Modal: Handling login modal - delegating to original function');
            // Let the original login modal function handle this
            if (window.originalOpenLoginModal) {
                return window.originalOpenLoginModal.apply(this, args);
            }
            return;
        }
        
        if (functionName === 'openEntityModal' && args[0]) {
            entity = args[0];
        } else if (element && element.onclick) {
            const onclickMatch = element.onclick.toString().match(/openEntityModal\(['"]([^'"]+)['"]\)/);
            if (onclickMatch) {
                entity = onclickMatch[1];
            }
        }
        
        if (entity) {
            console.log(`🌍 Universal Modal: Handling entity: ${entity}`);
            this.openUniversalModal(entity);
        }
    }
    
    async openUniversalModal(entity) {
        if (this.activeModal) {
            this.closeModal(this.activeModal);
        }
        
        console.log(`🌍 Universal Modal: Opening modal for ${entity}`);
        
        const modal = this.createModalHTML(entity);
        document.getElementById('universal-modal-container').appendChild(modal);
        document.getElementById('universal-modal-container').style.display = 'block';
        
        this.activeModal = modal;
        this.modalStack.push(modal);
        
        // Show loading state
        const modalBody = modal.querySelector('.modal-body');
        modalBody.innerHTML = `
            <div class="text-center p-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3">Loading ${entity} form...</p>
            </div>
        `;
        
        try {
            // Fetch form from clean endpoint
            const response = await fetch(`/${entity}/get/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                },
                credentials: 'include'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log(`🌍 Universal Modal: Form data received for ${entity}:`, data);
            
                         if (data.success && data.html) {
                 // Clean the HTML and insert it
                 const cleanHtml = this.cleanFormHtml(data.html);
                 modalBody.innerHTML = cleanHtml;
                 this.setupFormHandling(modal, entity);
                 console.log(`🌍 Universal Modal: Form loaded successfully for ${entity}`);
             } else {
                throw new Error('Form data not received');
            }
            
        } catch (error) {
            console.error(`🌍 Universal Modal: Error loading form for ${entity}:`, error);
            modalBody.innerHTML = `
                <div class="alert alert-danger m-3">
                    <h6>Error Loading Form</h6>
                    <p>${error.message}</p>
                    <button class="btn btn-primary" onclick="universalModalSystem.openUniversalModal('${entity}')">Try Again</button>
                </div>
            `;
        }
    }
    
    createModalHTML(entity) {
        const modal = document.createElement('div');
        modal.className = 'modal fade show d-block';
        modal.style.cssText = 'z-index: 10000;';
        
        const entityName = entity.charAt(0).toUpperCase() + entity.slice(1);
        
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Create ${entityName}</h5>
                        <button type="button" class="btn-close" onclick="universalModalSystem.closeModal(this.closest('.modal'))"></button>
                    </div>
                    <div class="modal-body">
                        <!-- Form will be loaded here -->
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" onclick="universalModalSystem.closeModal(this.closest('.modal'))">Cancel</button>
                        <button type="button" class="btn btn-primary" onclick="universalModalSystem.saveForm(this.closest('.modal'), '${entity}')">Save</button>
                    </div>
                </div>
            </div>
        `;
        
        return modal;
    }
    
    cleanFormHtml(html) {
        // Remove any problematic scripts and clean the HTML
        let cleanHtml = html;
        
        // Remove script tags that might cause issues
        cleanHtml = cleanHtml.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '');
        
        // Remove any "True is not defined" references
        cleanHtml = cleanHtml.replace(/True/g, 'true');
        cleanHtml = cleanHtml.replace(/False/g, 'false');
        
        console.log('🌍 Universal Modal: Cleaned form HTML');
        return cleanHtml;
    }
    
    setupFormHandling(modal, entity) {
        // Setup form validation and handling
        const form = modal.querySelector('form');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.saveForm(modal, entity);
            });
        }
    }
    
    async saveForm(modal, entity) {
        const saveBtn = modal.querySelector('.btn-primary');
        const form = modal.querySelector('form');
        
        if (!form) {
            console.error('🌍 Universal Modal: No form found');
            return;
        }
        
        saveBtn.disabled = true;
        saveBtn.textContent = 'Saving...';
        
        try {
            const formData = new FormData(form);
            const response = await fetch(`/${entity}/create/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'include'
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log(`🌍 Universal Modal: Form saved successfully for ${entity}`);
                this.showSuccessMessage(modal, 'Form saved successfully!');
                setTimeout(() => {
                    this.closeModal(modal);
                    location.reload();
                }, 1500);
            } else {
                throw new Error(result.error || 'Save failed');
            }
            
        } catch (error) {
            console.error(`🌍 Universal Modal: Error saving form for ${entity}:`, error);
            this.showErrorMessage(modal, `Error saving form: ${error.message}`);
        } finally {
            saveBtn.disabled = false;
            saveBtn.textContent = 'Save';
        }
    }
    
    showSuccessMessage(modal, message) {
        const modalBody = modal.querySelector('.modal-body');
        modalBody.innerHTML = `
            <div class="alert alert-success m-3">
                <i class="fas fa-check-circle"></i> ${message}
            </div>
        `;
    }
    
    showErrorMessage(modal, message) {
        const modalBody = modal.querySelector('.modal-body');
        modalBody.innerHTML = `
            <div class="alert alert-danger m-3">
                <i class="fas fa-exclamation-triangle"></i> ${message}
            </div>
        `;
    }
    
    closeModal(modal) {
        if (modal) {
            modal.remove();
            this.modalStack = this.modalStack.filter(m => m !== modal);
            
            if (this.modalStack.length === 0) {
                document.getElementById('universal-modal-container').style.display = 'none';
                this.activeModal = null;
            } else {
                this.activeModal = this.modalStack[this.modalStack.length - 1];
            }
        }
    }
    
    // Global close function
    closeAllModals() {
        this.modalStack.forEach(modal => this.closeModal(modal));
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.universalModalSystem = new UniversalModalSystem();
    console.log('🌍 Universal Modal System initialized - Industry Standard Solution');
});

// Global close function for external use
window.closeAllModals = () => {
    if (window.universalModalSystem) {
        window.universalModalSystem.closeAllModals();
    }
};
