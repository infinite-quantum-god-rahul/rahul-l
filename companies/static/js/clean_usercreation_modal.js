// Clean UserCreation Modal System - Complete Isolation
// This bypasses all existing problematic code and creates a fresh, working modal

console.log('🔧 Clean UserCreation Modal System loaded');

class CleanUserCreationModal {
    constructor() {
        this.isOpen = false;
        this.isLoading = false;
        this.init();
    }
    
    init() {
        console.log('🔧 Initializing Clean UserCreation Modal System');
        this.setupEventListeners();
        this.createModalHTML();
    }
    
    createModalHTML() {
        // Create modal HTML if it doesn't exist
        if (!document.getElementById('clean-usercreation-modal')) {
            const modalHTML = `
                <div id="clean-usercreation-modal" class="modal fade" tabindex="-1" role="dialog">
                    <div class="modal-dialog modal-lg" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Create User Creation</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body" id="clean-usercreation-modal-body">
                                <div class="text-center">
                                    <div class="spinner-border text-primary" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>
                                    <p class="mt-2">Loading form...</p>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                <button type="button" class="btn btn-primary" id="clean-usercreation-save-btn" disabled>Save</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHTML);
        }
    }
    
    setupEventListeners() {
        // Find and intercept UserCreation buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('[onclick*="openEntityModal"], [onclick*="UserCreation"], .btn-add')) {
                const button = e.target;
                const buttonText = button.textContent.toLowerCase();
                
                if (buttonText.includes('user') || buttonText.includes('add') || buttonText.includes('create')) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('🔧 Clean Modal: Intercepted button click');
                    this.openModal();
                }
            }
        });
        
        // Setup save button
        document.addEventListener('click', (e) => {
            if (e.target.id === 'clean-usercreation-save-btn') {
                this.saveForm();
            }
        });
    }
    
    async openModal() {
        if (this.isOpen || this.isLoading) return;
        
        console.log('🔧 Clean Modal: Opening UserCreation modal');
        this.isOpen = true;
        this.isLoading = true;
        
        const modal = document.getElementById('clean-usercreation-modal');
        const modalBody = document.getElementById('clean-usercreation-modal-body');
        const saveBtn = document.getElementById('clean-usercreation-save-btn');
        
        // Show modal
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
        
        // Show loading
        modalBody.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Loading User Creation form...</p>
            </div>
        `;
        
        saveBtn.disabled = true;
        
        try {
            // Fetch form from clean endpoint
            const response = await fetch('/usercreation/get/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'text/html,application/json'
                },
                credentials: 'include'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('🔧 Clean Modal: Form data received:', data);
            
            if (data.success && data.html) {
                // Insert form content
                modalBody.innerHTML = data.html;
                saveBtn.disabled = false;
                console.log('🔧 Clean Modal: Form loaded successfully');
            } else {
                throw new Error('Form data not received');
            }
            
        } catch (error) {
            console.error('🔧 Clean Modal: Error loading form:', error);
            modalBody.innerHTML = `
                <div class="alert alert-danger">
                    <h6>Error Loading Form</h6>
                    <p>${error.message}</p>
                    <button class="btn btn-primary" onclick="cleanUserCreationModal.openModal()">Try Again</button>
                </div>
            `;
        } finally {
            this.isLoading = false;
        }
    }
    
    async saveForm() {
        const saveBtn = document.getElementById('clean-usercreation-save-btn');
        const form = document.querySelector('#clean-usercreation-modal form');
        
        if (!form) {
            console.error('🔧 Clean Modal: No form found');
            return;
        }
        
        saveBtn.disabled = true;
        saveBtn.textContent = 'Saving...';
        
        try {
            const formData = new FormData(form);
            const response = await fetch('/usercreation/create/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'include'
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('🔧 Clean Modal: Form saved successfully');
                // Close modal and refresh page
                const modal = document.getElementById('clean-usercreation-modal');
                const bootstrapModal = bootstrap.Modal.getInstance(modal);
                bootstrapModal.hide();
                location.reload();
            } else {
                throw new Error(result.error || 'Save failed');
            }
            
        } catch (error) {
            console.error('🔧 Clean Modal: Error saving form:', error);
            alert(`Error saving form: ${error.message}`);
        } finally {
            saveBtn.disabled = false;
            saveBtn.textContent = 'Save';
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.cleanUserCreationModal = new CleanUserCreationModal();
    console.log('🔧 Clean UserCreation Modal System initialized');
});
