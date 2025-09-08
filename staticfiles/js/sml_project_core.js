/**
 * SML PROJECT CORE JAVASCRIPT
 * Professional Loan Monitoring System
 * Integrates with Enterprise Framework
 * Preserves all existing functionality
 */

(function() {
    'use strict';

    // ========================================
    // SML PROJECT CORE SYSTEM
    // ========================================
    const SMLProject = {
        version: '2.0.0',
        config: {
            apiEndpoints: {
                loans: '/api/loans/',
                clients: '/api/clients/',
                fieldSchedule: '/api/field-schedule/',
                npa: '/api/npa/',
                reports: '/api/reports/',
                creditBureau: '/api/credit-bureau/'
            },
            features: {
                aiCreditAnalysis: true,
                mobileApp: true,
                creditBureau: true,
                loanRestructuring: true,
                biometricKYC: true
            }
        },

        // Initialize SML Project
        init: function() {
            this.setupEventListeners();
            this.initializeComponents();
            this.setupCreditBureau();
            this.setupAIAnalytics();
            console.log('🚀 SML Project Core initialized!');
        },

        // Setup event listeners
        setupEventListeners: function() {
            // Loan application events
            document.addEventListener('click', (e) => {
                if (e.target.matches('[data-sml-action="apply-loan"]')) {
                    this.openLoanApplication(e.target.dataset.clientId);
                }
                if (e.target.matches('[data-sml-action="view-loan"]')) {
                    this.viewLoanDetails(e.target.dataset.loanId);
                }
                if (e.target.matches('[data-sml-action="restructure-loan"]')) {
                    this.openLoanRestructure(e.target.dataset.loanId);
                }
            });

            // Field schedule events
            document.addEventListener('click', (e) => {
                if (e.target.matches('[data-sml-action="schedule-field"]')) {
                    this.openFieldSchedule(e.target.dataset.routeId);
                }
                if (e.target.matches('[data-sml-action="complete-visit"]')) {
                    this.completeFieldVisit(e.target.dataset.visitId);
                }
            });

            // KYC document events
            document.addEventListener('click', (e) => {
                if (e.target.matches('[data-sml-action="upload-kyc"]')) {
                    this.openKYCDocumentUpload(e.target.dataset.clientId);
                }
                if (e.target.matches('[data-sml-action="verify-kyc"]')) {
                    this.verifyKYCDocument(e.target.dataset.docId);
                }
            });
        },

        // Initialize SML components
        initializeComponents: function() {
            this.initializeLoanDashboard();
            this.initializeNPADashboard();
            this.initializeFieldOperations();
            this.initializeClientManagement();
            this.initializeFinancialReports();
        }
    };

    // ========================================
    // LOAN MANAGEMENT SYSTEM
    // ========================================
    const LoanManagement = {
        // Open loan application modal
        openLoanApplication: function(clientId = null) {
            const modalContent = `
                <div class="sml-form-section">
                    <h3 class="sml-form-section-title">
                        <i class="fas fa-file-invoice-dollar"></i> New Loan Application
                    </h3>
                    
                    <form id="loan-application-form" class="enterprise-form">
                        <div class="sml-form-row">
                            <div class="form-group">
                                <label class="form-label">Loan Type *</label>
                                <select name="loan_type" class="form-control" required>
                                    <option value="">Select loan type</option>
                                    <option value="personal">Personal Loan</option>
                                    <option value="business">Business Loan</option>
                                    <option value="agriculture">Agriculture Loan</option>
                                    <option value="gold">Gold Loan</option>
                                    <option value="mortgage">Mortgage Loan</option>
                                </select>
                            </div>
                            
                            <div class="form-group">
                                <label class="form-label">Loan Amount (₹) *</label>
                                <input type="number" name="loan_amount" class="form-control" 
                                       min="1000" max="10000000" step="1000" required>
                            </div>
                        </div>
                        
                        <div class="sml-form-row">
                            <div class="form-group">
                                <label class="form-label">Tenure (Months) *</label>
                                <input type="number" name="tenure" class="form-control" 
                                       min="3" max="120" required>
                            </div>
                            
                            <div class="form-group">
                                <label class="form-label">Purpose *</label>
                                <textarea name="purpose" class="form-control" rows="3" required></textarea>
                            </div>
                        </div>
                        
                        <div class="sml-form-actions">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-paper-plane"></i> Submit Application
                            </button>
                            <button type="button" class="btn btn-secondary" onclick="ModalSystem.close()">
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            `;

            ModalSystem.show({
                title: 'New Loan Application',
                content: modalContent,
                size: 'large',
                onClose: () => this.handleLoanApplicationClose()
            });

            // Setup form submission
            document.getElementById('loan-application-form').addEventListener('submit', (e) => {
                e.preventDefault();
                this.submitLoanApplication(e.target);
            });
        },

        // Submit loan application
        submitLoanApplication: function(form) {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            // Show loading
            showLoading();
            
            // Simulate API call
            setTimeout(() => {
                hideLoading();
                
                // Show success notification
                if (window.NotificationSystem) {
                    window.NotificationSystem.success(
                        'Loan application submitted successfully! Application ID: LA' + Date.now(),
                        'Application Submitted'
                    );
                }
                
                // Close modal
                ModalSystem.close();
                
                // Refresh loan dashboard
                this.refreshLoanDashboard();
            }, 2000);
        },

        // View loan details
        viewLoanDetails: function(loanId) {
            const modalContent = `
                <div class="sml-loan-card">
                    <div class="card-header">
                        <h3 class="card-title">Loan Details - ${loanId}</h3>
                        <div class="card-actions">
                            <span class="sml-status-badge sml-status-approved">Approved</span>
                        </div>
                    </div>
                    
                    <div class="sml-client-info">
                        <div class="sml-client-detail">
                            <span class="sml-client-detail-label">Loan Amount</span>
                            <span class="sml-client-detail-value">₹50,000</span>
                        </div>
                        <div class="sml-client-detail">
                            <span class="sml-client-detail-label">Interest Rate</span>
                            <span class="sml-client-detail-value">12% p.a.</span>
                        </div>
                        <div class="sml-client-detail">
                            <span class="sml-client-detail-label">Tenure</span>
                            <span class="sml-client-detail-value">24 months</span>
                        </div>
                        <div class="sml-client-detail">
                            <span class="sml-client-detail-label">EMI Amount</span>
                            <span class="sml-client-detail-value">₹2,353</span>
                        </div>
                    </div>
                    
                    <div class="sml-repayment-schedule">
                        <h4>Repayment Schedule</h4>
                        <div class="sml-repayment-item">
                            <span class="sml-repayment-date">15 Jan 2024</span>
                            <span class="sml-repayment-amount">₹2,353</span>
                            <span class="sml-repayment-status sml-status-approved">Paid</span>
                        </div>
                        <div class="sml-repayment-item">
                            <span class="sml-repayment-date">15 Feb 2024</span>
                            <span class="sml-repayment-amount">₹2,353</span>
                            <span class="sml-repayment-status sml-status-pending">Pending</span>
                        </div>
                    </div>
                </div>
            `;

            ModalSystem.show({
                title: 'Loan Details',
                content: modalContent,
                size: 'large'
            });
        },

        // Open loan restructuring
        openLoanRestructure: function(loanId) {
            const modalContent = `
                <div class="sml-form-section">
                    <h3 class="sml-form-section-title">
                        <i class="fas fa-exchange-alt"></i> Loan Restructuring
                    </h3>
                    
                    <form id="loan-restructure-form" class="enterprise-form">
                        <div class="sml-form-row">
                            <div class="form-group">
                                <label class="form-label">Restructuring Type *</label>
                                <select name="restructure_type" class="form-control" required>
                                    <option value="">Select type</option>
                                    <option value="tenure_extension">Tenure Extension</option>
                                    <option value="emi_reduction">EMI Reduction</option>
                                    <option value="interest_waiver">Interest Waiver</option>
                                    <option value="moratorium">Moratorium</option>
                                </select>
                            </div>
                            
                            <div class="form-group">
                                <label class="form-label">New Tenure (Months)</label>
                                <input type="number" name="new_tenure" class="form-control" 
                                       min="1" max="120">
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Reason for Restructuring *</label>
                            <textarea name="reason" class="form-control" rows="4" required></textarea>
                        </div>
                        
                        <div class="sml-form-actions">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Submit Restructuring
                            </button>
                            <button type="button" class="btn btn-secondary" onclick="ModalSystem.close()">
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            `;

            ModalSystem.show({
                title: 'Loan Restructuring',
                content: modalContent,
                size: 'large'
            });
        },

        // Initialize loan dashboard
        initializeLoanDashboard: function() {
            const dashboardContainer = document.getElementById('loan-dashboard');
            if (!dashboardContainer) return;

            this.renderLoanDashboard(dashboardContainer);
        },

        // Render loan dashboard
        renderLoanDashboard: function(container) {
            const dashboardHTML = `
                <div class="sml-npa-dashboard">
                    <div class="sml-npa-card low-risk">
                        <div class="sml-npa-number">₹2,45,000</div>
                        <div class="sml-npa-label">Total Disbursed</div>
                        <div class="sml-npa-trend up">
                            <i class="fas fa-arrow-up"></i> +12.5%
                        </div>
                    </div>
                    
                    <div class="sml-npa-card medium-risk">
                        <div class="sml-npa-number">₹18,500</div>
                        <div class="sml-npa-label">Monthly Collection</div>
                        <div class="sml-npa-trend up">
                            <i class="fas fa-arrow-up"></i> +8.2%
                        </div>
                    </div>
                    
                    <div class="sml-npa-card high-risk">
                        <div class="sml-npa-number">₹12,000</div>
                        <div class="sml-npa-label">Overdue Amount</div>
                        <div class="sml-npa-trend down">
                            <i class="fas fa-arrow-down"></i> -5.1%
                        </div>
                    </div>
                </div>
                
                <div class="sml-loan-card">
                    <div class="card-header">
                        <h3 class="card-title">Recent Loan Applications</h3>
                        <div class="card-actions">
                            <button class="btn btn-primary btn-sm" onclick="LoanManagement.openLoanApplication()">
                                <i class="fas fa-plus"></i> New Application
                            </button>
                        </div>
                    </div>
                    
                    <div class="sml-table-container">
                        <table class="sml-table">
                            <thead>
                                <tr>
                                    <th>Application ID</th>
                                    <th>Client Name</th>
                                    <th>Loan Amount</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>LA001</td>
                                    <td>Ramesh Kumar</td>
                                    <td>₹50,000</td>
                                    <td><span class="sml-status-badge sml-status-approved">Approved</span></td>
                                    <td>
                                        <button class="btn btn-sm btn-primary" onclick="LoanManagement.viewLoanDetails('LA001')">
                                            View
                                        </button>
                                    </td>
                                </tr>
                                <tr>
                                    <td>LA002</td>
                                    <td>Meena Devi</td>
                                    <td>₹75,000</td>
                                    <td><span class="sml-status-badge sml-status-pending">Pending</span></td>
                                    <td>
                                        <button class="btn btn-sm btn-warning">Review</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            `;

            container.innerHTML = dashboardHTML;
        },

        // Refresh loan dashboard
        refreshLoanDashboard: function() {
            const dashboardContainer = document.getElementById('loan-dashboard');
            if (dashboardContainer) {
                this.renderLoanDashboard(dashboardContainer);
            }
        },

        // Handle loan application close
        handleLoanApplicationClose: function() {
            // Cleanup or additional logic
            console.log('Loan application modal closed');
        }
    };

    // ========================================
    // FIELD OPERATIONS SYSTEM
    // ========================================
    const FieldOperations = {
        // Open field schedule
        openFieldSchedule: function(routeId) {
            const modalContent = `
                <div class="sml-field-schedule">
                    <h3>Field Schedule - Route ${routeId}</h3>
                    
                    <div class="sml-schedule-day">
                        <div class="sml-schedule-day-header">
                            <span class="sml-schedule-day-title">Monday</span>
                            <span class="sml-schedule-day-date">15 Jan 2024</span>
                        </div>
                        
                        <div class="sml-schedule-item completed">
                            <span>Center A - Group 1</span>
                            <span>9:00 AM</span>
                            <span>Completed</span>
                        </div>
                        
                        <div class="sml-schedule-item pending">
                            <span>Center B - Group 2</span>
                            <span>11:00 AM</span>
                            <span>Pending</span>
                        </div>
                    </div>
                    
                    <div class="sml-schedule-day">
                        <div class="sml-schedule-day-header">
                            <span class="sml-schedule-day-title">Tuesday</span>
                            <span class="sml-schedule-day-date">16 Jan 2024</span>
                        </div>
                        
                        <div class="sml-schedule-item pending">
                            <span>Center C - Group 3</span>
                            <span>10:00 AM</span>
                            <span>Pending</span>
                        </div>
                    </div>
                </div>
            `;

            ModalSystem.show({
                title: 'Field Schedule',
                content: modalContent,
                size: 'large'
            });
        },

        // Complete field visit
        completeFieldVisit: function(visitId) {
            // Implementation for completing field visit
            console.log('Completing field visit:', visitId);
            
            if (window.NotificationSystem) {
                window.NotificationSystem.success('Field visit marked as completed!');
            }
        },

        // Initialize field operations
        initializeFieldOperations: function() {
            const fieldContainer = document.getElementById('field-operations');
            if (!fieldContainer) return;

            this.renderFieldOperations(fieldContainer);
        },

        // Render field operations
        renderFieldOperations: function(container) {
            const fieldHTML = `
                <div class="sml-route-card">
                    <div class="sml-route-map">
                        <i class="fas fa-map-marked-alt fa-3x"></i>
                        <p>Route visualization will be displayed here</p>
                    </div>
                    
                    <div class="sml-route-stops">
                        <div class="sml-route-stop">
                            <div class="sml-stop-number">1</div>
                            <span>Village A - Center 1</span>
                        </div>
                        <div class="sml-route-stop">
                            <div class="sml-stop-number">2</div>
                            <span>Village B - Center 2</span>
                        </div>
                        <div class="sml-route-stop">
                            <div class="sml-stop-number">3</div>
                            <span>Village C - Center 3</span>
                        </div>
                    </div>
                </div>
            `;

            container.innerHTML = fieldHTML;
        }
    };

    // ========================================
    // CLIENT MANAGEMENT SYSTEM
    // ========================================
    const ClientManagement = {
        // Open KYC document upload
        openKYCDocumentUpload: function(clientId) {
            const modalContent = `
                <div class="sml-form-section">
                    <h3 class="sml-form-section-title">
                        <i class="fas fa-id-card"></i> KYC Document Upload
                    </h3>
                    
                    <form id="kyc-upload-form" class="enterprise-form">
                        <div class="sml-form-row">
                            <div class="form-group">
                                <label class="form-label">Document Type *</label>
                                <select name="document_type" class="form-control" required>
                                    <option value="">Select document type</option>
                                    <option value="aadhaar">Aadhaar Card</option>
                                    <option value="pan">PAN Card</option>
                                    <option value="voter_id">Voter ID</option>
                                    <option value="driving_license">Driving License</option>
                                    <option value="passport">Passport</option>
                                </select>
                            </div>
                            
                            <div class="form-group">
                                <label class="form-label">Document Number</label>
                                <input type="text" name="document_number" class="form-control">
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Document File *</label>
                            <input type="file" name="document_file" class="form-control" 
                                   accept="image/*,.pdf" required>
                            <div class="form-help">Upload clear image or PDF (Max 5MB)</div>
                        </div>
                        
                        <div class="sml-form-actions">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-upload"></i> Upload Document
                            </button>
                            <button type="button" class="btn btn-secondary" onclick="ModalSystem.close()">
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            `;

            ModalSystem.show({
                title: 'KYC Document Upload',
                content: modalContent,
                size: 'large'
            });
        },

        // Verify KYC document
        verifyKYCDocument: function(docId) {
            // Implementation for KYC verification
            console.log('Verifying KYC document:', docId);
            
            if (window.NotificationSystem) {
                window.NotificationSystem.success('KYC document verified successfully!');
            }
        },

        // Initialize client management
        initializeClientManagement: function() {
            const clientContainer = document.getElementById('client-management');
            if (!clientContainer) return;

            this.renderClientManagement(clientContainer);
        },

        // Render client management
        renderClientManagement: function(container) {
            const clientHTML = `
                <div class="sml-client-card">
                    <div class="card-header">
                        <h3 class="card-title">Client Profile</h3>
                        <div class="card-actions">
                            <button class="btn btn-primary btn-sm" onclick="ClientManagement.openKYCDocumentUpload()">
                                <i class="fas fa-upload"></i> Upload KYC
                            </button>
                        </div>
                    </div>
                    
                    <img src="/static/images/default_avatar.png" alt="Client Avatar" class="sml-client-avatar">
                    
                    <div class="sml-client-info">
                        <div class="sml-client-detail">
                            <span class="sml-client-detail-label">Full Name</span>
                            <span class="sml-client-detail-value">Ramesh Kumar</span>
                        </div>
                        <div class="sml-client-detail">
                            <span class="sml-client-detail-label">Aadhaar Number</span>
                            <span class="sml-client-detail-value">1234-5678-9012</span>
                        </div>
                        <div class="sml-client-detail">
                            <span class="sml-client-detail-label">Contact Number</span>
                            <span class="sml-client-detail-value">9876543210</span>
                        </div>
                        <div class="sml-client-detail">
                            <span class="sml-client-detail-label">Occupation</span>
                            <span class="sml-client-detail-value">Farmer</span>
                        </div>
                    </div>
                </div>
                
                <div class="sml-kyc-section">
                    <h3>KYC Documents</h3>
                    
                    <div class="sml-kyc-document verified">
                        <div class="sml-kyc-icon verified">
                            <i class="fas fa-check"></i>
                        </div>
                        <div class="sml-kyc-info">
                            <div class="sml-kyc-name">Aadhaar Card</div>
                            <div class="sml-kyc-status">Verified on 10 Jan 2024</div>
                        </div>
                    </div>
                    
                    <div class="sml-kyc-document pending">
                        <div class="sml-kyc-icon pending">
                            <i class="fas fa-clock"></i>
                        </div>
                        <div class="sml-kyc-info">
                            <div class="sml-kyc-name">PAN Card</div>
                            <div class="sml-kyc-status">Pending verification</div>
                        </div>
                    </div>
                </div>
            `;

            container.innerHTML = clientHTML;
        }
    };

    // ========================================
    // CREDIT BUREAU INTEGRATION
    // ========================================
    const CreditBureau = {
        // Setup credit bureau integration
        setupCreditBureau: function() {
            // Initialize credit bureau API connections
            console.log('Credit Bureau integration initialized');
        },

        // Pull credit report
        pullCreditReport: function(clientId) {
            const modalContent = `
                <div class="sml-credit-bureau">
                    <div class="sml-credit-score">
                        <div class="sml-credit-number">750</div>
                        <div class="sml-credit-label">Credit Score</div>
                        <div class="sml-credit-rating sml-credit-good">Good</div>
                    </div>
                    
                    <div class="sml-table-container">
                        <table class="sml-table">
                            <thead>
                                <tr>
                                    <th>Parameter</th>
                                    <th>Value</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Payment History</td>
                                    <td>95%</td>
                                    <td><span class="sml-text-success">Excellent</span></td>
                                </tr>
                                <tr>
                                    <td>Credit Utilization</td>
                                    <td>35%</td>
                                    <td><span class="sml-text-success">Good</span></td>
                                </tr>
                                <tr>
                                    <td>Credit History Length</td>
                                    <td>5 years</td>
                                    <td><span class="sml-text-warning">Average</span></td>
                                </tr>
                                <tr>
                                    <td>Recent Inquiries</td>
                                    <td>2</td>
                                    <td><span class="sml-text-success">Good</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            `;

            ModalSystem.show({
                title: 'Credit Bureau Report',
                content: modalContent,
                size: 'xlarge'
            });
        }
    };

    // ========================================
    // AI ANALYTICS SYSTEM
    // ========================================
    const AIAnalytics = {
        // Setup AI analytics
        setupAIAnalytics: function() {
            console.log('AI Analytics system initialized');
        },

        // Analyze credit risk
        analyzeCreditRisk: function(clientData) {
            // AI-based credit risk analysis
            const riskScore = this.calculateRiskScore(clientData);
            return {
                score: riskScore,
                risk: riskScore > 700 ? 'Low' : riskScore > 500 ? 'Medium' : 'High',
                recommendations: this.generateRecommendations(riskScore)
            };
        },

        // Calculate risk score
        calculateRiskScore: function(clientData) {
            // Simplified risk calculation (in real implementation, this would use ML models)
            let score = 500; // Base score
            
            if (clientData.income > 50000) score += 100;
            if (clientData.employment > 2) score += 50;
            if (clientData.creditHistory > 3) score += 75;
            if (clientData.existingLoans < 2) score += 50;
            
            return Math.min(score, 900);
        },

        // Generate recommendations
        generateRecommendations: function(riskScore) {
            if (riskScore > 700) {
                return ['Approve loan with standard terms', 'Consider higher loan amount'];
            } else if (riskScore > 500) {
                return ['Approve with additional collateral', 'Reduce loan amount', 'Higher interest rate'];
            } else {
                return ['Require additional collateral', 'Consider co-signer', 'Strict monitoring required'];
            }
        }
    };

    // ========================================
    // FINANCIAL REPORTS SYSTEM
    // ========================================
    const FinancialReports = {
        // Initialize financial reports
        initializeFinancialReports: function() {
            const reportsContainer = document.getElementById('financial-reports');
            if (!reportsContainer) return;

            this.renderFinancialReports(reportsContainer);
        },

        // Render financial reports
        renderFinancialReports: function(container) {
            const reportsHTML = `
                <div class="sml-financial-card">
                    <h3>Financial Summary</h3>
                    
                    <div class="sml-financial-summary">
                        <div class="sml-financial-item">
                            <div class="sml-financial-amount">₹15,45,000</div>
                            <div class="sml-financial-label">Total Portfolio</div>
                        </div>
                        
                        <div class="sml-financial-item">
                            <div class="sml-financial-amount">₹2,34,500</div>
                            <div class="sml-financial-label">Monthly Disbursement</div>
                        </div>
                        
                        <div class="sml-financial-item">
                            <div class="sml-financial-amount">₹1,89,200</div>
                            <div class="sml-financial-label">Monthly Collection</div>
                        </div>
                        
                        <div class="sml-financial-item">
                            <div class="sml-financial-amount">87.2%</div>
                            <div class="sml-financial-label">Collection Efficiency</div>
                        </div>
                    </div>
                </div>
            `;

            container.innerHTML = reportsHTML;
        }
    };

    // ========================================
    // NPA DASHBOARD SYSTEM
    // ========================================
    const NPADashboard = {
        // Initialize NPA dashboard
        initializeNPADashboard: function() {
            const npaContainer = document.getElementById('npa-dashboard');
            if (!npaContainer) return;

            this.renderNPADashboard(npaContainer);
        },

        // Render NPA dashboard
        renderNPADashboard: function(container) {
            const npaHTML = `
                <div class="sml-npa-dashboard">
                    <div class="sml-npa-card low-risk">
                        <div class="sml-npa-number">₹45,000</div>
                        <div class="sml-npa-label">0-30 Days</div>
                        <div class="sml-npa-trend down">
                            <i class="fas fa-arrow-down"></i> -2.1%
                        </div>
                    </div>
                    
                    <div class="sml-npa-card medium-risk">
                        <div class="sml-npa-number">₹78,500</div>
                        <div class="sml-npa-label">31-60 Days</div>
                        <div class="sml-npa-trend up">
                            <i class="fas fa-arrow-up"></i> +5.3%
                        </div>
                    </div>
                    
                    <div class="sml-npa-card high-risk">
                        <div class="sml-npa-number">₹1,23,000</div>
                        <div class="sml-npa-label">60+ Days</div>
                        <div class="sml-npa-trend up">
                            <i class="fas fa-arrow-up"></i> +8.7%
                        </div>
                    </div>
                </div>
                
                <div class="sml-loan-card">
                    <div class="card-header">
                        <h3 class="card-title">NPA Analysis</h3>
                        <div class="card-actions">
                            <button class="btn btn-warning btn-sm">
                                <i class="fas fa-exclamation-triangle"></i> Generate Report
                            </button>
                        </div>
                    </div>
                    
                    <div class="sml-table-container">
                        <table class="sml-table">
                            <thead>
                                <tr>
                                    <th>Client Name</th>
                                    <th>Loan Amount</th>
                                    <th>Days Overdue</th>
                                    <th>Risk Level</th>
                                    <th>Action Required</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Anjali Devi</td>
                                    <td>₹25,000</td>
                                    <td>45 days</td>
                                    <td><span class="sml-text-warning">Medium</span></td>
                                    <td>Field Visit</td>
                                </tr>
                                <tr>
                                    <td>Rajesh Singh</td>
                                    <td>₹50,000</td>
                                    <td>75 days</td>
                                    <td><span class="sml-text-error">High</span></td>
                                    <td>Legal Notice</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            `;

            container.innerHTML = npaHTML;
        }
    };

    // ========================================
    // INITIALIZATION & EXPOSURE
    // ========================================
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize SML Project Core
        SMLProject.init();
        
        // Initialize all subsystems
        LoanManagement.initializeLoanDashboard();
        FieldOperations.initializeFieldOperations();
        ClientManagement.initializeClientManagement();
        FinancialReports.initializeFinancialReports();
        NPADashboard.initializeNPADashboard();
        
        // Expose to global scope
        window.SMLProject = SMLProject;
        window.LoanManagement = LoanManagement;
        window.FieldOperations = FieldOperations;
        window.ClientManagement = ClientManagement;
        window.CreditBureau = CreditBureau;
        window.AIAnalytics = AIAnalytics;
        window.FinancialReports = FinancialReports;
        window.NPADashboard = NPADashboard;
        
        console.log('🎯 SML Project Core fully initialized!');
    });

    // ========================================
    // LEGACY COMPATIBILITY LAYER
    // ========================================
    
    // Preserve existing functions and add SML features
    if (typeof window.openCreditPullModal === 'function') {
        const originalOpenCreditPullModal = window.openCreditPullModal;
        window.openCreditPullModal = function() {
            originalOpenCreditPullModal.apply(this, arguments);
            // Add SML credit bureau integration
            if (window.CreditBureau) {
                window.CreditBureau.pullCreditReport();
            }
        };
    }

})();


