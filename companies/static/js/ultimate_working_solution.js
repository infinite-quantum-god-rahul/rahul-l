// Ultimate Working Solution - This WILL NOT be deleted
// Complete modal system for User Creation

console.log('🚀 Ultimate Working Solution loaded - This will NOT be deleted!');

class UltimateModal {
    constructor() {
        this.init();
    }
    
    init() {
        console.log('🚀 Initializing Ultimate Modal Solution');
        this.createModal();
        this.replaceButtonBehavior();
        console.log('🚀 Ultimate Solution ready');
    }
    
    createModal() {
        // Create modal HTML
        const modalHTML = `
            <div id="ultimate-modal" class="modal fade" tabindex="-1" style="z-index: 9999; display: none;">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Create User Creation</h5>
                            <button type="button" class="btn-close" onclick="ultimateModal.closeModal()"></button>
                        </div>
                        <div class="modal-body" id="ultimate-modal-body">
                            <div class="text-center">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                                <p class="mt-2">Loading form...</p>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" onclick="ultimateModal.closeModal()">Cancel</button>
                            <button type="button" class="btn btn-primary" id="ultimate-save-btn" disabled>Save</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }
    
    replaceButtonBehavior() {
        // Find the User Creation button and completely replace its behavior
        const buttons = document.querySelectorAll('.btn-add, [onclick*="openEntityModal"], [onclick*="UserCreation"]');
        
        buttons.forEach(button => {
            const buttonText = button.textContent.toLowerCase();
            if (buttonText.includes('user') || buttonText.includes('add') || buttonText.includes('create')) {
                console.log('🚀 Ultimate: Replacing button behavior for:', button);
                
                // Remove all existing onclick handlers
                button.removeAttribute('onclick');
                
                // Add new click handler
                button.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('🚀 Ultimate: Button clicked, opening modal');
                    this.openModal();
                });
            }
        });
    }
    
    openModal() {
        console.log('🚀 Ultimate: Opening modal');
        
        const modal = document.getElementById('ultimate-modal');
        const modalBody = document.getElementById('ultimate-modal-body');
        const saveBtn = document.getElementById('ultimate-save-btn');
        
        // Show modal
        modal.style.display = 'block';
        modal.classList.add('show');
        document.body.classList.add('modal-open');
        
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
        
        // Load form
        this.loadForm();
    }
    
    async loadForm() {
        try {
            console.log('🚀 Ultimate: Loading form from server');
            
            const modalBody = document.getElementById('ultimate-modal-body');
            const saveBtn = document.getElementById('ultimate-save-btn');
            
            const response = await fetch('/usercreation/get/', {
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
            console.log('🚀 Ultimate: Form data received:', data);
            
            if (data.success && data.html) {
                // Clean and insert form
                const cleanHtml = this.cleanFormHtml(data.html);
                console.log('🚀 Ultimate: Clean HTML:', cleanHtml);
                modalBody.innerHTML = cleanHtml;
                
                // Debug: Check what's actually in the modal body
                console.log('🚀 Ultimate: Modal body content after insertion:', modalBody.innerHTML);
                console.log('🚀 Ultimate: Modal body children count:', modalBody.children.length);
                
                saveBtn.disabled = false;
                console.log('🚀 Ultimate: Form loaded successfully');
                
                // Set up form submission
                this.setupFormSubmission();
            } else {
                throw new Error('Form data not received');
            }
            
        } catch (error) {
            console.error('🚀 Ultimate: Error loading form:', error);
            const modalBody = document.getElementById('ultimate-modal-body');
            modalBody.innerHTML = `
                <div class="alert alert-danger">
                    <h6>Error Loading Form</h6>
                    <p>${error.message}</p>
                    <button class="btn btn-primary" onclick="ultimateModal.loadForm()">Try Again</button>
                </div>
            `;
        }
    }
    
    cleanFormHtml(html) {
        // Remove problematic content
        let cleanHtml = html;
        cleanHtml = cleanHtml.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '');
        cleanHtml = cleanHtml.replace(/True/g, 'true');
        cleanHtml = cleanHtml.replace(/False/g, 'false');
        return cleanHtml;
    }
    
    setupFormSubmission() {
        const form = document.getElementById('super-clean-usercreation-form');
        const saveBtn = document.getElementById('ultimate-save-btn');
        
        console.log('🚀 Ultimate: Looking for form with ID "super-clean-usercreation-form"');
        console.log('🚀 Ultimate: Form element found:', form);
        console.log('🚀 Ultimate: Save button found:', saveBtn);
        
        if (form && saveBtn) {
            saveBtn.onclick = () => this.submitForm(form);
            console.log('🚀 Ultimate: Form submission setup complete');
        } else {
            console.log('🚀 Ultimate: Form or save button not found!');
        }
    }
    
    async submitForm(form) {
        try {
            console.log('🚀 Ultimate: Submitting form');
            const saveBtn = document.getElementById('ultimate-save-btn');
            saveBtn.disabled = true;
            saveBtn.textContent = 'Saving...';
            
            const formData = new FormData(form);
            
            const response = await fetch('/usercreation/create/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                },
                credentials: 'include'
            });
            
            const data = await response.json();
            
            if (data.success) {
                console.log('🚀 Ultimate: Form submitted successfully');
                this.showSuccess('User Creation successful!');
                setTimeout(() => this.closeModal(), 2000);
            } else {
                throw new Error(data.error || 'Form submission failed');
            }
            
        } catch (error) {
            console.error('🚀 Ultimate: Form submission error:', error);
            this.showError('Error saving: ' + error.message);
            const saveBtn = document.getElementById('ultimate-save-btn');
            saveBtn.disabled = false;
            saveBtn.textContent = 'Save';
        }
    }
    
    showSuccess(message) {
        const modalBody = document.getElementById('ultimate-modal-body');
        modalBody.innerHTML = `
            <div class="alert alert-success text-center">
                <h6>Success!</h6>
                <p>${message}</p>
            </div>
        `;
    }
    
    showError(message) {
        const modalBody = document.getElementById('ultimate-modal-body');
        modalBody.innerHTML = `
            <div class="alert alert-danger text-center">
                <h6>Error</h6>
                <p>${message}</p>
            </div>
        `;
    }
    
    closeModal() {
        console.log('🚀 Ultimate: Closing modal');
        const modal = document.getElementById('ultimate-modal');
        modal.style.display = 'none';
        modal.classList.remove('show');
        document.body.classList.remove('modal-open');
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.ultimateModal = new UltimateModal();
    console.log('🚀 Ultimate Working Solution initialized - This will NOT be deleted!');
});
