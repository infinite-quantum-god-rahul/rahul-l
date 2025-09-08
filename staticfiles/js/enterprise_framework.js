/**
 * ENTERPRISE-GRADE JAVASCRIPT FRAMEWORK
 * SBI / Income Tax / Government Style
 * Preserves all existing functionality while adding professional features
 */

(function() {
    'use strict';

    // ========================================
    // ENTERPRISE FRAMEWORK CORE
    // ========================================
    const EnterpriseFramework = {
        version: '1.0.0',
        config: {
            animations: true,
            notifications: true,
            analytics: true,
            accessibility: true
        },
        
        // Initialize the framework
        init: function(config = {}) {
            this.config = { ...this.config, ...config };
            this.setupEventListeners();
            this.initializeComponents();
            this.setupAccessibility();
            this.log('Enterprise Framework initialized');
        },

        // Logging system
        log: function(message, level = 'info') {
            if (this.config.debug) {
                console.log(`[Enterprise] ${level.toUpperCase()}: ${message}`);
            }
        },

        // Error handling
        handleError: function(error, context = '') {
            console.error(`[Enterprise Error] ${context}:`, error);
            this.showNotification('An error occurred. Please try again.', 'error');
        }
    };

    // ========================================
    // PROFESSIONAL NOTIFICATION SYSTEM
    // ========================================
    const NotificationSystem = {
        notifications: [],
        container: null,

        init: function() {
            this.createContainer();
            this.setupStyles();
        },

        createContainer: function() {
            this.container = document.createElement('div');
            this.container.id = 'enterprise-notifications';
            this.container.className = 'enterprise-notifications-container';
            document.body.appendChild(this.container);
        },

        setupStyles: function() {
            const styles = `
                .enterprise-notifications-container {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    z-index: 10000;
                    max-width: 400px;
                }
                
                .enterprise-notification {
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
                    margin-bottom: 10px;
                    padding: 16px;
                    border-left: 4px solid;
                    transform: translateX(100%);
                    transition: transform 0.3s ease;
                    max-width: 100%;
                }
                
                .enterprise-notification.show {
                    transform: translateX(0);
                }
                
                .enterprise-notification.success {
                    border-left-color: #059669;
                }
                
                .enterprise-notification.error {
                    border-left-color: #dc2626;
                }
                
                .enterprise-notification.warning {
                    border-left-color: #d97706;
                }
                
                .enterprise-notification.info {
                    border-left-color: #2563eb;
                }
                
                .notification-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 8px;
                }
                
                .notification-title {
                    font-weight: 600;
                    font-size: 14px;
                    color: #111827;
                }
                
                .notification-close {
                    background: none;
                    border: none;
                    font-size: 18px;
                    cursor: pointer;
                    color: #6b7280;
                    padding: 0;
                    width: 20px;
                    height: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 4px;
                    transition: background-color 0.2s;
                }
                
                .notification-close:hover {
                    background-color: #f3f4f6;
                }
                
                .notification-message {
                    font-size: 14px;
                    color: #374151;
                    line-height: 1.5;
                }
            `;
            
            const styleSheet = document.createElement('style');
            styleSheet.textContent = styles;
            document.head.appendChild(styleSheet);
        },

        show: function(message, type = 'info', title = '', duration = 5000) {
            const notification = this.createNotification(message, type, title);
            this.container.appendChild(notification);
            
            // Animate in
            setTimeout(() => notification.classList.add('show'), 100);
            
            // Auto-remove
            if (duration > 0) {
                setTimeout(() => this.remove(notification), duration);
            }
            
            return notification;
        },

        createNotification: function(message, type, title) {
            const notification = document.createElement('div');
            notification.className = `enterprise-notification ${type}`;
            
            const defaultTitles = {
                success: 'Success',
                error: 'Error',
                warning: 'Warning',
                info: 'Information'
            };
            
            const displayTitle = title || defaultTitles[type] || 'Notification';
            
            notification.innerHTML = `
                <div class="notification-header">
                    <div class="notification-title">${displayTitle}</div>
                    <button class="notification-close" onclick="NotificationSystem.remove(this.parentElement.parentElement)">&times;</button>
                </div>
                <div class="notification-message">${message}</div>
            `;
            
            return notification;
        },

        remove: function(notification) {
            if (notification && notification.parentElement) {
                notification.classList.remove('show');
                setTimeout(() => {
                    if (notification.parentElement) {
                        notification.parentElement.removeChild(notification);
                    }
                }, 300);
            }
        },

        success: function(message, title = '', duration = 5000) {
            return this.show(message, 'success', title, duration);
        },

        error: function(message, title = '', duration = 8000) {
            return this.show(message, 'error', title, duration);
        },

        warning: function(message, title = '', duration = 6000) {
            return this.show(message, 'warning', title, duration);
        },

        info: function(message, title = '', duration = 5000) {
            return this.show(message, 'info', title, duration);
        }
    };

    // ========================================
    // PROFESSIONAL MODAL SYSTEM
    // ========================================
    const ModalSystem = {
        activeModal: null,
        backdrop: null,

        init: function() {
            this.createBackdrop();
            this.setupStyles();
        },

        createBackdrop: function() {
            this.backdrop = document.createElement('div');
            this.backdrop.className = 'enterprise-modal-backdrop';
            this.backdrop.style.display = 'none';
            document.body.appendChild(this.backdrop);
        },

        setupStyles: function() {
            const styles = `
                .enterprise-modal-backdrop {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0, 0, 0, 0.5);
                    z-index: 9999;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                }
                
                .enterprise-modal-backdrop.show {
                    opacity: 1;
                }
                
                .enterprise-modal {
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%) scale(0.9);
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 20px 25px rgba(0,0,0,0.15);
                    z-index: 10000;
                    max-width: 90vw;
                    max-height: 90vh;
                    overflow: auto;
                    opacity: 0;
                    transition: all 0.3s ease;
                }
                
                .enterprise-modal.show {
                    opacity: 1;
                    transform: translate(-50%, -50%) scale(1);
                }
                
                .modal-header {
                    padding: 20px 24px 16px;
                    border-bottom: 1px solid #e5e7eb;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .modal-title {
                    font-size: 18px;
                    font-weight: 600;
                    color: #111827;
                    margin: 0;
                }
                
                .modal-close {
                    background: none;
                    border: none;
                    font-size: 24px;
                    cursor: pointer;
                    color: #6b7280;
                    padding: 4px;
                    border-radius: 4px;
                    transition: background-color 0.2s;
                }
                
                .modal-close:hover {
                    background-color: #f3f4f6;
                }
                
                .modal-body {
                    padding: 24px;
                }
                
                .modal-footer {
                    padding: 16px 24px 24px;
                    border-top: 1px solid #e5e7eb;
                    display: flex;
                    gap: 12px;
                    justify-content: flex-end;
                }
            `;
            
            const styleSheet = document.createElement('style');
            styleSheet.textContent = styles;
            document.head.appendChild(styleSheet);
        },

        show: function(options) {
            const {
                title = 'Modal',
                content = '',
                size = 'medium',
                closable = true,
                onClose = null,
                buttons = []
            } = options;

            // Close existing modal
            if (this.activeModal) {
                this.close();
            }

            // Create modal
            const modal = document.createElement('div');
            modal.className = 'enterprise-modal';
            
            const sizeClasses = {
                small: 'max-w-md',
                medium: 'max-w-lg',
                large: 'max-w-2xl',
                xlarge: 'max-w-4xl'
            };
            
            modal.classList.add(sizeClasses[size] || sizeClasses.medium);

            // Build modal content
            let headerHtml = '';
            if (closable) {
                headerHtml = `
                    <div class="modal-header">
                        <h2 class="modal-title">${title}</h2>
                        <button class="modal-close" onclick="ModalSystem.close()">&times;</button>
                    </div>
                `;
            } else {
                headerHtml = `
                    <div class="modal-header">
                        <h2 class="modal-title">${title}</h2>
                    </div>
                `;
            }

            let footerHtml = '';
            if (buttons.length > 0) {
                const buttonHtml = buttons.map(btn => {
                    const btnClass = btn.class || 'btn btn-secondary';
                    return `<button class="${btnClass}" onclick="${btn.onClick}">${btn.text}</button>`;
                }).join('');
                
                footerHtml = `<div class="modal-footer">${buttonHtml}</div>`;
            }

            modal.innerHTML = `
                ${headerHtml}
                <div class="modal-body">${content}</div>
                ${footerHtml}
            `;

            // Show modal
            document.body.appendChild(modal);
            this.activeModal = modal;
            this.backdrop.style.display = 'block';
            
            setTimeout(() => {
                this.backdrop.classList.add('show');
                modal.classList.add('show');
            }, 10);

            // Store close callback
            if (onClose) {
                modal.dataset.onClose = onClose.toString();
            }

            return modal;
        },

        close: function() {
            if (this.activeModal) {
                const modal = this.activeModal;
                const onClose = modal.dataset.onClose;
                
                // Animate out
                this.backdrop.classList.remove('show');
                modal.classList.remove('show');
                
                setTimeout(() => {
                    if (modal.parentElement) {
                        modal.parentElement.removeChild(modal);
                    }
                    this.backdrop.style.display = 'none';
                    this.activeModal = null;
                    
                    // Execute close callback
                    if (onClose) {
                        try {
                            eval(onClose);
                        } catch (e) {
                            console.error('Error executing modal close callback:', e);
                        }
                    }
                }, 300);
            }
        },

        confirm: function(message, title = 'Confirm', onConfirm = null, onCancel = null) {
            const buttons = [
                {
                    text: 'Cancel',
                    class: 'btn btn-secondary',
                    onClick: 'ModalSystem.close()'
                },
                {
                    text: 'Confirm',
                    class: 'btn btn-primary',
                    onClick: `
                        if (typeof ${onConfirm} === 'function') {
                            ${onConfirm}();
                        }
                        ModalSystem.close();
                    `
                }
            ];

            return this.show({
                title: title,
                content: `<p>${message}</p>`,
                size: 'small',
                buttons: buttons
            });
        }
    };

    // ========================================
    // PROFESSIONAL FORM VALIDATION SYSTEM
    // ========================================
    const FormValidation = {
        validators: {
            required: function(value) {
                return value !== null && value !== undefined && value.toString().trim() !== '';
            },
            
            email: function(value) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                return emailRegex.test(value);
            },
            
            phone: function(value) {
                const phoneRegex = /^\d{10}$/;
                return phoneRegex.test(value.replace(/\D/g, ''));
            },
            
            aadhaar: function(value) {
                const aadhaarRegex = /^\d{4}\s\d{4}\s\d{4}$/;
                return aadhaarRegex.test(value);
            },
            
            minLength: function(value, min) {
                return value && value.toString().length >= min;
            },
            
            maxLength: function(value, max) {
                return value && value.toString().length <= max;
            },
            
            numeric: function(value) {
                return !isNaN(value) && !isNaN(parseFloat(value));
            },
            
            positive: function(value) {
                return this.numeric(value) && parseFloat(value) > 0;
            }
        },

        validateField: function(field, rules) {
            const value = field.value;
            const errors = [];

            for (const rule of rules) {
                const { type, message, params = [] } = rule;
                
                if (this.validators[type]) {
                    const isValid = this.validators[type](value, ...params);
                    if (!isValid) {
                        errors.push(message || `Validation failed for ${type}`);
                    }
                }
            }

            return errors;
        },

        validateForm: function(form) {
            const errors = {};
            const fields = form.querySelectorAll('[data-validation]');
            
            fields.forEach(field => {
                const validationRules = JSON.parse(field.dataset.validation);
                const fieldErrors = this.validateField(field, validationRules);
                
                if (fieldErrors.length > 0) {
                    errors[field.name] = fieldErrors;
                    this.showFieldError(field, fieldErrors[0]);
                } else {
                    this.clearFieldError(field);
                }
            });

            return {
                isValid: Object.keys(errors).length === 0,
                errors: errors
            };
        },

        showFieldError: function(field, message) {
            this.clearFieldError(field);
            
            field.classList.add('error');
            
            const errorDiv = document.createElement('div');
            errorDiv.className = 'form-error';
            errorDiv.textContent = message;
            
            field.parentNode.appendChild(errorDiv);
        },

        clearFieldError: function(field) {
            field.classList.remove('error');
            
            const existingError = field.parentNode.querySelector('.form-error');
            if (existingError) {
                existingError.remove();
            }
        },

        setupFormValidation: function(formSelector) {
            const forms = document.querySelectorAll(formSelector);
            
            forms.forEach(form => {
                form.addEventListener('submit', (e) => {
                    const validation = this.validateForm(form);
                    
                    if (!validation.isValid) {
                        e.preventDefault();
                        NotificationSystem.error('Please correct the errors in the form.');
                        return false;
                    }
                });
            });
        }
    };

    // ========================================
    // PROFESSIONAL DATA TABLE SYSTEM
    // ========================================
    const DataTable = {
        tables: new Map(),

        init: function() {
            this.setupStyles();
            this.initializeTables();
        },

        setupStyles: function() {
            const styles = `
                .enterprise-data-table {
                    width: 100%;
                    background: white;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }
                
                .data-table-header {
                    background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 100%);
                    color: white;
                    padding: 16px 20px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .data-table-title {
                    font-size: 18px;
                    font-weight: 600;
                    margin: 0;
                }
                
                .data-table-actions {
                    display: flex;
                    gap: 12px;
                }
                
                .data-table-search {
                    display: flex;
                    gap: 12px;
                    padding: 16px 20px;
                    background: #f9fafb;
                    border-bottom: 1px solid #e5e7eb;
                }
                
                .data-table-search input {
                    flex: 1;
                    padding: 8px 12px;
                    border: 1px solid #d1d5db;
                    border-radius: 6px;
                    font-size: 14px;
                }
                
                .data-table-content {
                    overflow-x: auto;
                }
                
                .data-table-table {
                    width: 100%;
                    border-collapse: collapse;
                }
                
                .data-table-table th {
                    background: #f3f4f6;
                    padding: 12px 16px;
                    text-align: left;
                    font-weight: 600;
                    color: #374151;
                    border-bottom: 1px solid #e5e7eb;
                }
                
                .data-table-table td {
                    padding: 12px 16px;
                    border-bottom: 1px solid #f3f4f6;
                }
                
                .data-table-table tbody tr:hover {
                    background-color: #f9fafb;
                }
                
                .data-table-pagination {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 16px 20px;
                    background: #f9fafb;
                    border-top: 1px solid #e5e7eb;
                }
                
                .pagination-info {
                    color: #6b7280;
                    font-size: 14px;
                }
                
                .pagination-controls {
                    display: flex;
                    gap: 8px;
                }
                
                .pagination-btn {
                    padding: 6px 12px;
                    border: 1px solid #d1d5db;
                    background: white;
                    border-radius: 6px;
                    cursor: pointer;
                    transition: all 0.2s;
                }
                
                .pagination-btn:hover {
                    background: #f3f4f6;
                }
                
                .pagination-btn.active {
                    background: #1e3a8a;
                    color: white;
                    border-color: #1e3a8a;
                }
                
                .pagination-btn:disabled {
                    opacity: 0.5;
                    cursor: not-allowed;
                }
            `;
            
            const styleSheet = document.createElement('style');
            styleSheet.textContent = styles;
            document.head.appendChild(styleSheet);
        },

        create: function(container, options = {}) {
            const {
                title = 'Data Table',
                columns = [],
                data = [],
                searchable = true,
                sortable = true,
                pagination = true,
                pageSize = 10
            } = options;

            const tableId = 'data-table-' + Date.now();
            const table = {
                id: tableId,
                container: container,
                options: options,
                currentPage: 1,
                filteredData: [...data],
                sortColumn: null,
                sortDirection: 'asc'
            };

            this.tables.set(tableId, table);
            this.renderTable(table);
            return tableId;
        },

        renderTable: function(table) {
            const { container, options, currentPage, filteredData, sortColumn, sortDirection } = table;
            const { title, columns, searchable, pagination, pageSize } = options;

            let html = `
                <div class="enterprise-data-table">
                    <div class="data-table-header">
                        <h3 class="data-table-title">${title}</h3>
                        <div class="data-table-actions">
                            <button class="btn btn-primary btn-sm" onclick="DataTable.exportTable('${table.id}')">
                                Export
                            </button>
                        </div>
                    </div>
            `;

            if (searchable) {
                html += `
                    <div class="data-table-search">
                        <input type="text" placeholder="Search..." onkeyup="DataTable.filterTable('${table.id}', this.value)">
                    </div>
                `;
            }

            html += `
                <div class="data-table-content">
                    <table class="data-table-table">
                        <thead>
                            <tr>
            `;

            columns.forEach(column => {
                const sortableClass = options.sortable ? 'sortable' : '';
                const sortIcon = sortColumn === column.key ? (sortDirection === 'asc' ? '↑' : '↓') : '';
                
                html += `
                    <th class="${sortableClass}" onclick="DataTable.sortTable('${table.id}', '${column.key}')">
                        ${column.title} ${sortIcon}
                    </th>
                `;
            });

            html += `
                            </tr>
                        </thead>
                        <tbody>
            `;

            const startIndex = (currentPage - 1) * pageSize;
            const endIndex = startIndex + pageSize;
            const pageData = filteredData.slice(startIndex, endIndex);

            pageData.forEach(row => {
                html += '<tr>';
                columns.forEach(column => {
                    const value = row[column.key] || '';
                    html += `<td>${value}</td>`;
                });
                html += '</tr>';
            });

            html += `
                        </tbody>
                    </table>
                </div>
            `;

            if (pagination) {
                const totalPages = Math.ceil(filteredData.length / pageSize);
                
                html += `
                    <div class="data-table-pagination">
                        <div class="pagination-info">
                            Showing ${startIndex + 1} to ${Math.min(endIndex, filteredData.length)} of ${filteredData.length} entries
                        </div>
                        <div class="pagination-controls">
                            <button class="pagination-btn" onclick="DataTable.goToPage('${table.id}', ${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
                                Previous
                            </button>
                `;

                for (let i = 1; i <= totalPages; i++) {
                    if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
                        const activeClass = i === currentPage ? 'active' : '';
                        html += `
                            <button class="pagination-btn ${activeClass}" onclick="DataTable.goToPage('${table.id}', ${i})">
                                ${i}
                            </button>
                        `;
                    } else if (i === currentPage - 3 || i === currentPage + 3) {
                        html += '<span class="pagination-btn">...</span>';
                    }
                }

                html += `
                            <button class="pagination-btn" onclick="DataTable.goToPage('${table.id}', ${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
                                Next
                            </button>
                        </div>
                    </div>
                `;
            }

            html += '</div>';

            container.innerHTML = html;
        },

        filterTable: function(tableId, searchTerm) {
            const table = this.tables.get(tableId);
            if (!table) return;

            const { data, options } = table;
            const { columns } = options;

            if (!searchTerm.trim()) {
                table.filteredData = [...data];
            } else {
                table.filteredData = data.filter(row => {
                    return columns.some(column => {
                        const value = row[column.key];
                        if (value) {
                            return value.toString().toLowerCase().includes(searchTerm.toLowerCase());
                        }
                        return false;
                    });
                });
            }

            table.currentPage = 1;
            this.renderTable(table);
        },

        sortTable: function(tableId, columnKey) {
            const table = this.tables.get(tableId);
            if (!table || !table.options.sortable) return;

            const { filteredData, sortColumn, sortDirection } = table;

            if (sortColumn === columnKey) {
                table.sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                table.sortColumn = columnKey;
                table.sortDirection = 'asc';
            }

            table.filteredData.sort((a, b) => {
                const aVal = a[columnKey] || '';
                const bVal = b[columnKey] || '';

                if (aVal < bVal) return table.sortDirection === 'asc' ? -1 : 1;
                if (aVal > bVal) return table.sortDirection === 'asc' ? 1 : -1;
                return 0;
            });

            this.renderTable(table);
        },

        goToPage: function(tableId, page) {
            const table = this.tables.get(tableId);
            if (!table) return;

            const { options, filteredData } = table;
            const totalPages = Math.ceil(filteredData.length / options.pageSize);

            if (page >= 1 && page <= totalPages) {
                table.currentPage = page;
                this.renderTable(table);
            }
        },

        exportTable: function(tableId) {
            const table = this.tables.get(tableId);
            if (!table) return;

            const { filteredData, options } = table;
            const { columns } = options;

            let csv = columns.map(col => col.title).join(',') + '\n';

            filteredData.forEach(row => {
                const rowData = columns.map(col => {
                    const value = row[col.key] || '';
                    return `"${value.toString().replace(/"/g, '""')}"`;
                });
                csv += rowData.join(',') + '\n';
            });

            const blob = new Blob([csv], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${options.title || 'export'}.csv`;
            a.click();
            window.URL.revokeObjectURL(url);

            NotificationSystem.success('Table exported successfully!');
        },

        initializeTables: function() {
            // Auto-initialize tables with data-table class
            const tables = document.querySelectorAll('.data-table');
            tables.forEach(tableElement => {
                const options = JSON.parse(tableElement.dataset.options || '{}');
                this.create(tableElement, options);
            });
        }
    };

    // ========================================
    // PROFESSIONAL CHART SYSTEM
    // ========================================
    const ChartSystem = {
        charts: new Map(),

        init: function() {
            // Initialize chart system
            this.setupStyles();
        },

        setupStyles: function() {
            const styles = `
                .enterprise-chart {
                    background: white;
                    border-radius: 8px;
                    padding: 20px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                }
                
                .chart-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                }
                
                .chart-title {
                    font-size: 18px;
                    font-weight: 600;
                    color: #111827;
                    margin: 0;
                }
                
                .chart-actions {
                    display: flex;
                    gap: 12px;
                }
                
                .chart-container {
                    position: relative;
                    height: 400px;
                }
            `;
            
            const styleSheet = document.createElement('style');
            styleSheet.textContent = styles;
            document.head.appendChild(styleSheet);
        },

        createChart: function(container, type, data, options = {}) {
            const chartId = 'chart-' + Date.now();
            
            // Create chart container
            const chartContainer = document.createElement('div');
            chartContainer.className = 'enterprise-chart';
            chartContainer.id = chartId;
            
            const { title = 'Chart', showActions = true } = options;
            
            let html = `
                <div class="chart-header">
                    <h3 class="chart-title">${title}</h3>
            `;
            
            if (showActions) {
                html += `
                    <div class="chart-actions">
                        <button class="btn btn-secondary btn-sm" onclick="ChartSystem.exportChart('${chartId}')">
                            Export
                        </button>
                    </div>
                `;
            }
            
            html += `
                </div>
                <div class="chart-container" id="chart-canvas-${chartId}"></div>
            `;
            
            chartContainer.innerHTML = html;
            container.appendChild(chartContainer);
            
            // Store chart data
            this.charts.set(chartId, {
                type,
                data,
                options,
                container: chartContainer
            });
            
            // Render chart (placeholder for now)
            this.renderChart(chartId);
            
            return chartId;
        },

        renderChart: function(chartId) {
            const chart = this.charts.get(chartId);
            if (!chart) return;
            
            const canvas = document.getElementById(`chart-canvas-${chartId}`);
            if (!canvas) return;
            
            // Placeholder chart rendering
            canvas.innerHTML = `
                <div style="display: flex; align-items: center; justify-content: center; height: 100%; color: #6b7280;">
                    <div style="text-align: center;">
                        <div style="font-size: 48px; margin-bottom: 16px;">📊</div>
                        <div>Chart: ${chart.type}</div>
                        <div style="font-size: 14px; margin-top: 8px;">Data points: ${chart.data.length}</div>
                    </div>
                </div>
            `;
        },

        exportChart: function(chartId) {
            const chart = this.charts.get(chartId);
            if (!chart) return;
            
            // Placeholder export functionality
            NotificationSystem.info('Chart export functionality coming soon!');
        }
    };

    // ========================================
    // PROFESSIONAL UTILITY FUNCTIONS
    // ========================================
    const Utils = {
        // Debounce function
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        // Throttle function
        throttle: function(func, limit) {
            let inThrottle;
            return function() {
                const args = arguments;
                const context = this;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        },

        // Format currency
        formatCurrency: function(amount, currency = 'INR') {
            return new Intl.NumberFormat('en-IN', {
                style: 'currency',
                currency: currency
            }).format(amount);
        },

        // Format date
        formatDate: function(date, format = 'DD/MM/YYYY') {
            const d = new Date(date);
            const day = String(d.getDate()).padStart(2, '0');
            const month = String(d.getMonth() + 1).padStart(2, '0');
            const year = d.getFullYear();
            
            return format
                .replace('DD', day)
                .replace('MM', month)
                .replace('YYYY', year);
        },

        // Generate random ID
        generateId: function(prefix = '') {
            return prefix + Date.now().toString(36) + Math.random().toString(36).substr(2);
        },

        // Deep clone object
        deepClone: function(obj) {
            if (obj === null || typeof obj !== 'object') return obj;
            if (obj instanceof Date) return new Date(obj.getTime());
            if (obj instanceof Array) return obj.map(item => this.deepClone(item));
            if (typeof obj === 'object') {
                const clonedObj = {};
                for (const key in obj) {
                    if (obj.hasOwnProperty(key)) {
                        clonedObj[key] = this.deepClone(obj[key]);
                    }
                }
                return clonedObj;
            }
        },

        // Validate email
        isValidEmail: function(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        },

        // Validate phone number
        isValidPhone: function(phone) {
            const phoneRegex = /^\d{10}$/;
            return phoneRegex.test(phone.replace(/\D/g, ''));
        },

        // Sanitize HTML
        sanitizeHtml: function(html) {
            const div = document.createElement('div');
            div.textContent = html;
            return div.innerHTML;
        }
    };

    // ========================================
    // ACCESSIBILITY SYSTEM
    // ========================================
    const Accessibility = {
        init: function() {
            this.setupKeyboardNavigation();
            this.setupScreenReaderSupport();
            this.setupHighContrastMode();
        },

        setupKeyboardNavigation: function() {
            document.addEventListener('keydown', (e) => {
                // Tab navigation
                if (e.key === 'Tab') {
                    this.handleTabNavigation(e);
                }
                
                // Escape key for modals
                if (e.key === 'Escape') {
                    if (ModalSystem.activeModal) {
                        ModalSystem.close();
                    }
                }
                
                // Enter key for buttons
                if (e.key === 'Enter' && e.target.tagName === 'BUTTON') {
                    e.target.click();
                }
            });
        },

        handleTabNavigation: function(e) {
            const focusableElements = document.querySelectorAll(
                'a[href], button:not([disabled]), input:not([disabled]), textarea:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
            );
            
            const firstElement = focusableElements[0];
            const lastElement = focusableElements[focusableElements.length - 1];
            
            if (e.shiftKey && document.activeElement === firstElement) {
                e.preventDefault();
                lastElement.focus();
            } else if (!e.shiftKey && document.activeElement === lastElement) {
                e.preventDefault();
                firstElement.focus();
            }
        },

        setupScreenReaderSupport: function() {
            // Add ARIA labels to interactive elements
            const buttons = document.querySelectorAll('button:not([aria-label])');
            buttons.forEach(button => {
                if (!button.textContent.trim()) {
                    button.setAttribute('aria-label', 'Button');
                }
            });
        },

        setupHighContrastMode: function() {
            // Check for high contrast mode preference
            const prefersHighContrast = window.matchMedia('(prefers-contrast: high)');
            
            if (prefersHighContrast.matches) {
                document.body.classList.add('high-contrast');
            }
        }
    };

    // ========================================
    // ANALYTICS SYSTEM
    // ========================================
    const Analytics = {
        events: [],
        
        init: function() {
            this.setupEventTracking();
        },

        setupEventTracking: function() {
            // Track page views
            this.trackPageView();
            
            // Track user interactions
            document.addEventListener('click', (e) => {
                this.trackEvent('click', {
                    element: e.target.tagName,
                    text: e.target.textContent?.substring(0, 50),
                    href: e.target.href
                });
            });
            
            // Track form submissions
            document.addEventListener('submit', (e) => {
                this.trackEvent('form_submit', {
                    form: e.target.id || e.target.className,
                    action: e.target.action
                });
            });
        },

        trackPageView: function() {
            this.trackEvent('page_view', {
                url: window.location.href,
                title: document.title,
                referrer: document.referrer
            });
        },

        trackEvent: function(eventName, properties = {}) {
            const event = {
                name: eventName,
                properties: properties,
                timestamp: new Date().toISOString(),
                sessionId: this.getSessionId()
            };
            
            this.events.push(event);
            
            // Send to analytics service (placeholder)
            if (this.config.analytics) {
                this.sendToAnalytics(event);
            }
        },

        getSessionId: function() {
            let sessionId = sessionStorage.getItem('enterprise_session_id');
            if (!sessionId) {
                sessionId = Utils.generateId('session_');
                sessionStorage.setItem('enterprise_session_id', sessionId);
            }
            return sessionId;
        },

        sendToAnalytics: function(event) {
            // Placeholder for analytics service integration
            console.log('Analytics Event:', event);
        },

        getEvents: function() {
            return this.events;
        },

        clearEvents: function() {
            this.events = [];
        }
    };

    // ========================================
    // INITIALIZATION & EXPOSURE
    // ========================================
    
    // Initialize all systems when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize core framework
        EnterpriseFramework.init();
        
        // Initialize all subsystems
        NotificationSystem.init();
        ModalSystem.init();
        FormValidation.init();
        DataTable.init();
        ChartSystem.init();
        Accessibility.init();
        Analytics.init();
        
        // Expose to global scope
        window.EnterpriseFramework = EnterpriseFramework;
        window.NotificationSystem = NotificationSystem;
        window.ModalSystem = ModalSystem;
        window.FormValidation = FormValidation;
        window.DataTable = DataTable;
        window.ChartSystem = ChartSystem;
        window.Utils = Utils;
        
        // Log successful initialization
        console.log('🚀 Enterprise Framework fully initialized!');
        console.log('Available systems:', {
            notifications: NotificationSystem,
            modals: ModalSystem,
            validation: FormValidation,
            tables: DataTable,
            charts: ChartSystem,
            utils: Utils
        });
    });

    // ========================================
    // LEGACY COMPATIBILITY LAYER
    // ========================================
    
    // Preserve existing functions and add enterprise features
    if (typeof window.toggleSidebar === 'function') {
        const originalToggleSidebar = window.toggleSidebar;
        window.toggleSidebar = function() {
            originalToggleSidebar.apply(this, arguments);
            // Add enterprise enhancements
            const sidebar = document.getElementById('sidebar');
            if (sidebar) {
                sidebar.classList.toggle('enterprise-sidebar');
            }
        };
    }
    
    if (typeof window.openCreditPullModal === 'function') {
        const originalOpenCreditPullModal = window.openCreditPullModal;
        window.openCreditPullModal = function() {
            originalOpenCreditPullModal.apply(this, arguments);
            // Add enterprise tracking
            if (window.Analytics) {
                window.Analytics.trackEvent('modal_open', { modal: 'credit_pull' });
            }
        };
    }

})();


