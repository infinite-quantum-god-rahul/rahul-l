# companies/forms_spec.py
# Single source of truth for grid columns and modal sections.
# Use "" for fields not in your DB models; they'll be saved into extra_data.

FORMS_SPEC = {
    # ───────────────── COMPANY ─────────────────
    "Company": {
        "grid": ["code", "name", "phone", "opening_date", "mortgage"],
        "sections": {
            "Basic Information": [
                {"name": "code", "type": "char", "required": True},
                {"name": "name", "type": "char", "required": True},
                {"name": "opening_date", "type": "date"},
                {"name": "status", "type": "char"},
                {"name": "mortgage", "type": "char"},
            ],
            "Contact": [
                {"name": "phone", "type": "char"},
                {"name": "email", "type": "char"},
                {"name": "address", "type": "char"},
            ],
            "Media": [
                {"name": "logo", "type": "image"},
            ],
        },
    },

    # ───────────────── BRANCH ─────────────────
    "Branch": {
        "grid": ["code", "name", "company", "phone", "open_date", "branch_manager"],
        "sections": {
            "Basic Information": [
                {"name": "code", "type": "char", "required": True},
                {"name": "name", "type": "char", "required": True},
                {"name": "company", "type": "foreign_key", "model": "Company", "required": True},
                {"name": "open_date", "type": "date"},
                {"name": "status", "type": "char"},
                {"name": "export_flag", "type": "boolean", "default": False, "required": False},
                {"name": "branch_manager", "type": "char"},
            ],
            "Contact": [
                {"name": "phone", "type": "char"},
                {"name": "address1", "type": "char"},
                {"name": "district", "type": "char"},
            ],
        },
    },

    # ───────────────── VILLAGE ─────────────────
    "Village": {
        "grid": ["VCode", "VName", "branch", "TDate", "population", "village_type"],
        "sections": {
            "Basic Information": [
                {"name": "VCode", "type": "char", "required": True},
                {"name": "VName", "type": "char", "required": True},
                {"name": "branch", "type": "foreign_key", "model": "Branch"},
                {"name": "TDate", "type": "date"},
                {"name": "status", "type": "char"},
                {"name": "population", "type": "int"},
                {"name": "village_type", "type": "char"},
            ],
        },
    },

    # ───────────────── CENTER ─────────────────
    "Center": {
        "grid": ["code", "name", "village", "collection_day", "created_on", "member_count"],
        "sections": {
            "Basic Information": [
                {"name": "code", "type": "char", "required": True},
                {"name": "name", "type": "char", "required": True},
                {"name": "village", "type": "char"},
                {"name": "created_on", "type": "date"},
                {"name": "status", "type": "char"},
                {"name": "member_count", "type": "int"},
            ],
            "Meeting Details": [
                {"name": "collection_day", "type": "char"},
                {"name": "meet_place", "type": "char"},
            ],
        },
    },

    # ───────────────── GROUP ─────────────────
    "Group": {
        "grid": ["code", "name", "center", "week_day", "borrower_count", "formation_date"],
        "sections": {
            "Basic Information": [
                {"name": "code", "type": "char", "required": True},
                {"name": "name", "type": "char", "required": True},
                {"name": "center", "type": "char"},
                {"name": "borrower_count", "type": "int"},
                {"name": "status", "type": "char"},
                {"name": "formation_date", "type": "date"},
            ],
            "Meeting Details": [
                {"name": "week_day", "type": "char"},
                {"name": "meeting_time", "type": "char"},
            ],
        },
    },

    # ───────────────── ROLE ─────────────────
    "Role": {
        "grid": ["name", "description", "permission_count"],
        "sections": {
            "Basic Information": [
                {"name": "name", "type": "char", "required": True},
                {"name": "permissions", "type": "char"},
                {"name": "description", "type": "char"},
                {"name": "permission_count", "type": "int"},
            ],
        },
    },

    # ───────────────── CADRE ─────────────────
    "Cadre": {
        "grid": ["name", "branch", "designation_level", "salary_grade"],
        "sections": {
            "Basic Information": [
                {"name": "name", "type": "char", "required": True},
                {"name": "branch", "type": "char", "required": True},
                {"name": "status", "type": "char"},
                {"name": "designation_level", "type": "char"},
                {"name": "salary_grade", "type": "char"},
            ],
        },
    },

    # ───────────────── STAFF ─────────────────
    "Staff": {
        "grid": ["staffcode", "name", "designation", "branch", "contact1", "joining_date", "department"],
        "sections": {
            "Basic Information": [
                {"name": "staffcode", "type": "char", "required": True},
                {"name": "name", "type": "char", "required": True},
                {"name": "branch", "type": "foreign_key", "model": "Branch"},
                {"name": "cadre", "type": "foreign_key", "model": "Cadre"},
                {"name": "status", "type": "char"},
            ],
            "Identity & KYC": [
                {"name": "aadhaar_number", "type": "char", "required": True},
                {"name": "gender", "type": "char"},
                {"name": "date_of_birth", "type": "date"},
                {"name": "photo", "type": "image"},
                {"name": "kyc_documents", "type": "file"},
                {"name": "biometric_data", "type": "image"},
            ],
            "Contact": [
                {"name": "contact1", "type": "char", "required": True},
                {"name": "email_id", "type": "char"},
                {"name": "residential_address", "type": "char"},
                {"name": "emergency_contact", "type": "char"},
            ],
            "Employment": [
                {"name": "designation", "type": "char"},
                {"name": "joining_date", "type": "date"},
                {"name": "department", "type": "char"},
                {"name": "employee_id", "type": "char"},
                {"name": "educational_qualifications", "type": "char"},
                {"name": "work_experience", "type": "char"},
                {"name": "professional_certifications", "type": "char"},
            ],
            "Bank & PAN": [
                {"name": "bank", "type": "char"},
                {"name": "ifsc", "type": "char"},
                {"name": "bank_account_details", "type": "char"},
                {"name": "pan_number", "type": "char"},
            ],
        },
    },

    # ───────────────── USER CREATION ─────────────────
    "UserCreation": {
        "grid": ["user", "full_name", "staff", "branch", "department", "mobile"],
        "sections": {
            "Basic Information": [
                {"name": "user", "type": "char"},
                {"name": "staff", "type": "select"},
                {"name": "full_name", "type": "char", "required": True},
                {"name": "status", "type": "char"},
            ],
            "Contact": [
                {"name": "mobile", "type": "char"},
            ],
            "Organization": [
                {"name": "branch", "type": "select"},
                {"name": "department", "type": "char"},
            ],
            "Security": [
                {"name": "password", "type": "char"},
            ],
        },
    },

    # ───────────────── PRODUCT ─────────────────
    "Product": {
        "grid": ["code", "name", "category", "interest_rate", "loan_amount_range"],
        "sections": {
            "Basic Information": [
                {"name": "code", "type": "char", "required": True},
                {"name": "name", "type": "char", "required": True},
                {"name": "category", "type": "char"},
                {"name": "status", "type": "char"},
                {"name": "interest_rate", "type": "char"},
                {"name": "loan_amount_range", "type": "char"},
            ],
        },
    },

    # ───────────────── CLIENT (Borrower) ─────────────────
    "Client": {
        "grid": ["smtcode", "name", "group", "contactno", "join_date", "occupation", "annual_income"],
        "sections": {
            "Basic Information": [
                {"name": "smtcode", "type": "char", "required": True},
                {"name": "name", "type": "char", "required": True},
                {"name": "group", "type": "foreign_key", "model": "Group"},
                {"name": "join_date", "type": "date"},
                {"name": "status", "type": "char"},
            ],
            "Identity & KYC": [
                {"name": "gender", "type": "char"},
                {"name": "aadhar", "type": "char"},
                {"name": "date_of_birth", "type": "date"},
                {"name": "residential_address", "type": "char"},
                {"name": "photograph", "type": "image"},
                {"name": "kyc_documents", "type": "file"},
                {"name": "biometric_data", "type": "image"},
            ],
            "Contact": [
                {"name": "contactno", "type": "char", "required": True},
                {"name": "email_id", "type": "char"},
                {"name": "marital_status", "type": "char"},
            ],
            "Financials": [
                {"name": "occupation", "type": "char"},
                {"name": "annual_income", "type": "int"},
                {"name": "pan_number", "type": "char"},
                {"name": "bank_account_details", "type": "char"},
                {"name": "credit_score", "type": "int"},
            ],
            "Loan Details": [
                {"name": "loan_purpose", "type": "char"},
                {"name": "guarantor_details", "type": "char"},
            ],
        },
    },

    # ───────────────── FIELD SCHEDULE ─────────────────
    "FieldSchedule": {
        "grid": ["schedule_date", "staff", "center", "notes"],
        "sections": {
            "Basic Information": [
                {"name": "schedule_date", "type": "date"},
                {"name": "staff", "type": "foreign_key", "model": "Staff"},
                {"name": "center", "type": "foreign_key", "model": "Center"},
            ],
            "Notes": [
                {"name": "notes", "type": "text"},
            ],
        },
    },

    # ───────────────── FIELD REPORT ─────────────────
    "FieldReport": {
        "grid": ["report_date", "schedule", "summary", "visit_duration", "outcome", "photo_count"],
        "sections": {
            "Basic Information": [
                {"name": "report_date", "type": "date"},
                {"name": "schedule", "type": "foreign_key", "model": "FieldSchedule"},
            ],
            "Report": [
                {"name": "summary", "type": "text"},
                {"name": "visit_duration", "type": "int"},
                {"name": "outcome", "type": "char"},
                {"name": "photo_count", "type": "int"},
            ],
            "Attachments": [
                {"name": "photo_1", "type": "image"},
                {"name": "photo_2", "type": "image"},
            ],
        },
    },

    # ───────────────── WEEKLY REPORT ─────────────────
    "WeeklyReport": {
        "grid": ["period_start", "period_end", "generated_on", "summary"],
        "sections": {
            "Basic Information": [
                {"name": "period_start", "type": "date"},
                {"name": "period_end", "type": "date"},
                {"name": "generated_on", "type": "date"},
            ],
            "Report": [
                {"name": "summary", "type": "text"},
                {"name": "total_visits", "type": "int"},
                {"name": "total_clients", "type": "int"},
                {"name": "total_collections", "type": "int"},
            ],
        },
    },

    # ───────────────── MONTHLY REPORT ─────────────────
    "MonthlyReport": {
        "grid": ["period_start", "period_end", "generated_on", "total_loans", "total_disbursements", "total_recoveries"],
        "sections": {
            "Basic Information": [
                {"name": "period_start", "type": "date"},
                {"name": "period_end", "type": "date"},
                {"name": "generated_on", "type": "date"},
            ],
            "Report": [
                {"name": "summary", "type": "char"},
                {"name": "total_loans", "type": "int"},
                {"name": "total_disbursements", "type": "int"},
                {"name": "total_recoveries", "type": "int"},
            ],
        },
    },

    # ───────────────── BUSINESS SETTINGS ─────────────────
    "BusinessSetting": {
        "grid": ["key", "value", "company", "category", "description"],
        "sections": {
            "Basic Information": [
                {"name": "key", "type": "char", "required": True},
                {"name": "value", "type": "char", "required": True},
                {"name": "company", "type": "char"},
                {"name": "category", "type": "char"},
                {"name": "description", "type": "char"},
            ],
        },
    },

    # ───────────────── ACCOUNTING ─────────────────
    "AccountHead": {
        "grid": ["code", "name", "parent", "ac_type", "description", "opening_balance"],
        "sections": {
            "Basic Information": [
                {"name": "code", "type": "char", "required": True},
                {"name": "name", "type": "char", "required": True},
                {"name": "parent", "type": "foreign_key", "model": "AccountHead"},
                {"name": "status", "type": "char"},
                {"name": "description", "type": "char"},
                {"name": "opening_balance", "type": "decimal"},
            ],
            "Details": [
                {"name": "abbreviation", "type": "char"},
                {"name": "ac_type", "type": "char"},
                {"name": "vtype", "type": "char"},
            ],
        },
    },

    "Voucher": {
        "grid": ["voucher_no", "date", "account_head", "debit_total", "credit_total", "voucher_type"],
        "sections": {
            "Basic Information": [
                {"name": "voucher_no", "type": "char", "required": True},
                {"name": "date", "type": "date", "required": True},
                {"name": "account_head", "type": "foreign_key", "model": "AccountHead", "required": True},
                {"name": "status", "type": "char"},
                {"name": "voucher_type", "type": "char"},
            ],
            "Details": [
                {"name": "narration", "type": "char"},
                {"name": "debit_total", "type": "decimal"},
                {"name": "credit_total", "type": "decimal"},
            ],
        },
    },

    "Posting": {
        "grid": ["voucher", "account_head", "debit", "credit", "narration", "reference"],
        "sections": {
            "Basic Information": [
                {"name": "voucher", "type": "foreign_key", "model": "Voucher", "required": True},
                {"name": "account_head", "type": "foreign_key", "model": "AccountHead", "required": True},
            ],
            "Amounts": [
                {"name": "debit", "type": "char"},
                {"name": "credit", "type": "char"},
            ],
            "Details": [
                {"name": "ttype", "type": "char"},
                {"name": "narration", "type": "char"},
                {"name": "reference", "type": "char"},
            ],
        },
    },

    "RecoveryPosting": {
        "grid": ["client", "date", "amount", "voucher", "recovery_type", "agent"],
        "sections": {
            "Basic Information": [
                {"name": "client", "type": "foreign_key", "model": "Client", "required": True},
                {"name": "date", "type": "date", "required": True},
                {"name": "voucher", "type": "foreign_key", "model": "Voucher"},
                {"name": "status", "type": "char"},
                {"name": "recovery_type", "type": "char"},
                {"name": "agent", "type": "char"},
            ],
            "Amount": [
                {"name": "amount", "type": "char", "required": True},
            ],
        },
    },

    # ───────────────── KYC DOCUMENTS ─────────────────
    # Basis: ID proof capture, linkage to party, verification workflow.
    "KYCDocument": {
        "grid": ["party_name", "doc_type", "doc_no", "issue_date", "expiry_date", "verified_by", "verification_status"],
        "sections": {
            "Document": [
                {"name": "doc_type", "type": "char", "required": True},
                {"name": "doc_no", "type": "char"},
                {"name": "name_on_doc", "type": "char"},
                {"name": "issue_date", "type": "date"},
                {"name": "expiry_date", "type": "date"},
                {"name": "document_file", "type": "file"},
                {"name": "document_image", "type": "image"},
            ],
            "Holder": [
                {"name": "party_type", "type": "char"},   # Client/Staff
                {"name": "party_id", "type": "char"},
                {"name": "party_name", "type": "char"},
                {"name": "dob", "type": "date"},
                {"name": "address", "type": "char"},
            ],
            "Verification": [
                {"name": "verified_by", "type": "char"},
                {"name": "verified_on", "type": "date"},
                {"name": "verification_remarks", "type": "char"},
                {"name": "verification_status", "type": "char"},
            ],
        },
    },

    # ───────────────── ALERT RULES ─────────────────
    # Basis: event condition, recipients, delivery, status.
    "AlertRule": {
        "grid": ["name", "severity", "entity", "channel", "is_active", "last_triggered", "trigger_count"],
        "sections": {
            "Definition": [
                {"name": "name", "type": "char", "required": True},
                {"name": "severity", "type": "char"},
                {"name": "condition", "type": "char"},   # e.g., DSL or JSON
                {"name": "entity", "type": "char"},      # Loan/Client/Recovery
                {"name": "channel", "type": "char"},     # Email/SMS/InApp
            ],
            "Targets": [
                {"name": "branch", "type": "char"},
                {"name": "role", "type": "char"},
                {"name": "recipients", "type": "char"},  # comma emails/phones
            ],
            "Delivery": [
                {"name": "template", "type": "char"},
                {"name": "schedule", "type": "char"},    # immediate/daily/cron
            ],
            "Status": [
                {"name": "is_active", "type": "char"},   # Y/N
                {"name": "last_triggered", "type": "date"},
                {"name": "trigger_count", "type": "int"},
            ],
        },
    },

    # ───────────────── HR: APPOINTMENT ─────────────────
    "Appointment": {
        "grid": ["staff", "appointment_date", "designation", "branch", "appointment_type", "remarks"],
        "sections": {
            "Basic Information": [
                {"name": "staff", "type": "char", "required": True},
                {"name": "appointment_date", "type": "date"},
                {"name": "designation", "type": "char"},
                {"name": "branch", "type": "char"},
                {"name": "status", "type": "char"},
            ],
            "Details": [
                {"name": "appointment_type", "type": "char"},
                {"name": "remarks", "type": "char"},
            ],
        },
    },

    # ───────────────── HR: SALARY STATEMENT ─────────────────
    "SalaryStatement": {
        "grid": ["staff", "month", "year", "basic_pay", "net_pay", "total_allowances", "total_deductions"],
        "sections": {
            "Basic Information": [
                {"name": "staff", "type": "char", "required": True},
                {"name": "month", "type": "int"},
                {"name": "year", "type": "int"},
                {"name": "status", "type": "char"},
            ],
            "Salary Details": [
                {"name": "basic_pay", "type": "char"},
                {"name": "allowances", "type": "char"},
                {"name": "deductions", "type": "char"},
                {"name": "net_pay", "type": "char"},
                {"name": "generated_on", "type": "date"},
            ],
            "Summary": [
                {"name": "total_allowances", "type": "decimal"},
                {"name": "total_deductions", "type": "decimal"},
                {"name": "gross_salary", "type": "decimal"},
            ],
        },
    },

    # ───────────────── LOAN LIFECYCLE ─────────────────
    "LoanApplication": {
        "grid": ["application_number", "client", "product", "amount_requested", "interest_rate", "tenure_months", "applied_date", "loan_purpose"],
        "sections": {
            "Basic Information": [
                {"name": "application_number", "type": "char", "required": True},
                {"name": "client", "type": "char", "required": True},
                {"name": "product", "type": "char"},
                {"name": "status", "type": "char"},
            ],
            "Loan Details": [
                {"name": "amount_requested", "type": "char"},
                {"name": "interest_rate", "type": "char"},
                {"name": "tenure_months", "type": "int"},
                {"name": "applied_date", "type": "date"},
            ],
            "Extras": [
                {"name": "loan_purpose", "type": "char"},
                {"name": "guarantor_details", "type": "char"},
                {"name": "bureau_score", "type": "int"},
                {"name": "remarks", "type": "char"},
            ],
        },
    },

    "LoanApproval": {
        "grid": ["loan_application", "approved_amount", "approval_date", "approver", "conditions"],
        "sections": {
            "Basic Information": [
                {"name": "loan_application", "type": "char", "required": True},
                {"name": "approver", "type": "char"},
                {"name": "status", "type": "char"},
            ],
            "Approval Details": [
                {"name": "approved_amount", "type": "char"},
                {"name": "approval_date", "type": "date"},
            ],
            "Notes": [
                {"name": "conditions", "type": "char"},
                {"name": "remarks", "type": "char"},
            ],
        },
    },

    "Disbursement": {
        "grid": ["loan_application", "amount", "disbursement_date", "channel", "utr_no"],
        "sections": {
            "Basic Information": [
                {"name": "loan_application", "type": "char", "required": True},
                {"name": "status", "type": "char"},
            ],
            "Disbursement Details": [
                {"name": "amount", "type": "char"},
                {"name": "disbursement_date", "type": "date"},
                {"name": "channel", "type": "char"},
            ],
            "Proof": [
                {"name": "utr_no", "type": "char"},
                {"name": "receipt", "type": "file"},
            ],
        },
    },

    # ───────────────── PAYMENTS / REPAYMENTS ─────────────────
    "Payment": {
        "grid": ["loan_application", "amount", "gateway", "order_id", "payer_name", "payer_phone"],
        "sections": {
            "Basic Information": [
                {"name": "loan_application", "type": "char", "required": True},
                {"name": "amount", "type": "char", "required": True},
                {"name": "gateway", "type": "char"},
                {"name": "status", "type": "char"},
            ],
            "Payment Details": [
                {"name": "order_id", "type": "char", "required": True},
                {"name": "txn_ref", "type": "char"},
            ],
            "Meta": [
                {"name": "payer_name", "type": "char"},
                {"name": "payer_phone", "type": "char"},
                {"name": "notes", "type": "char"},
            ],
        },
    },

    "Repayment": {
        "grid": ["loan_application", "paid_on", "amount", "mode", "reference", "installment_no"],
        "sections": {
            "Basic Information": [
                {"name": "loan_application", "type": "char", "required": True},
                {"name": "paid_on", "type": "date"},
                {"name": "status", "type": "char"},
            ],
            "Payment Details": [
                {"name": "amount", "type": "char", "required": True},
                {"name": "mode", "type": "char"},
                {"name": "reference", "type": "char"},
                {"name": "installment_no", "type": "int"},
            ],
            "Notes": [
                {"name": "notes", "type": "char"},
            ],
        },
    },

    "LoanRestructure": {
        "grid": ["loan_application", "effective_from", "old_tenure", "new_tenure", "old_rate", "new_rate"],
        "sections": {
            "Basic Information": [
                {"name": "loan_application", "type": "char", "required": True},
                {"name": "effective_from", "type": "date", "required": True},
                {"name": "status", "type": "char"},
            ],
            "Terms": [
                {"name": "old_tenure", "type": "int"},
                {"name": "old_rate", "type": "char"},
                {"name": "new_tenure", "type": "int"},
                {"name": "new_rate", "type": "char"},
            ],
            "Notes": [
                {"name": "reason", "type": "char"},
            ],
        },
    },

    # ───────────────── NOTIFICATIONS / EVENTS ─────────────────
    "Notification": {
        "grid": ["channel", "to_address", "subject", "sent_at", "recipient_type"],
        "sections": {
            "Basic Information": [
                {"name": "channel", "type": "char", "required": True},
                {"name": "to_address", "type": "char", "required": True},
                {"name": "status", "type": "char"},
                {"name": "recipient_type", "type": "char"},
            ],
            "Message": [
                {"name": "subject", "type": "char"},
                {"name": "body", "type": "char", "required": True},
                {"name": "sent_at", "type": "date"},
            ],
        },
    },

    "GatewayEvent": {
        "grid": ["gateway", "event", "received_at", "signature_ok", "event_data", "processing_status"],
        "sections": {
            "Basic Information": [
                {"name": "gateway", "type": "char", "required": True},
                {"name": "event", "type": "char", "required": True},
                {"name": "signature_ok", "type": "char"},
                {"name": "received_at", "type": "date"},
            ],
            "Event Details": [
                {"name": "event_data", "type": "char"},
                {"name": "processing_status", "type": "char"},
            ],
        },
    },

    "EWIFlag": {
        "grid": ["loan_application", "code", "active", "raised_at", "cleared_at", "severity", "description"],
        "sections": {
            "Basic Information": [
                {"name": "loan_application", "type": "char", "required": True},
                {"name": "code", "type": "char", "required": True},
                {"name": "active", "type": "char"},
                {"name": "raised_at", "type": "date"},
                {"name": "cleared_at", "type": "date"},
            ],
            "Details": [
                {"name": "detail", "type": "char"},
                {"name": "severity", "type": "char"},
                {"name": "description", "type": "char"},
            ],
        },
    },

    # ───────────────── KYC DOCUMENTS ─────────────────
    "KYCDocument": {
        "grid": ["client_ref", "doc_type", "number"],
        "sections": {
            "Basic Information": [
                {"name": "client_ref", "type": "char"},
                {"name": "client_name", "type": "char"},
                {"name": "doc_type", "type": "char", "required": True},
                {"name": "status", "type": "char"},
            ],
            "Document": [
                {"name": "file", "type": "file"},
                {"name": "number", "type": "char"},
            ],
            "Notes": [
                {"name": "remarks", "type": "char"},
            ],
        },
    },

    # ───────────────── ALERT RULES ─────────────────
    "AlertRule": {
        "grid": ["name", "entity", "is_active"],
        "sections": {
            "Basic Information": [
                {"name": "name", "type": "char", "required": True},
                {"name": "entity", "type": "char", "required": True},
                {"name": "is_active", "type": "char"},
            ],
            "Configuration": [
                {"name": "condition", "type": "char"},
                {"name": "channels", "type": "char"},
            ],
        },
    },

    # ───────────────── COLUMN ─────────────────
    "Column": {
        "grid": ["module", "field_name", "label", "field_type", "required", "order", "description", "validation_rules"],
        "sections": {
            "Basic Information": [
                {"name": "module", "type": "char", "required": True},
                {"name": "field_name", "type": "char", "required": True},
                {"name": "label", "type": "char", "required": True},
                {"name": "field_type", "type": "char"},
                {"name": "required", "type": "char"},
                {"name": "order", "type": "int"},
            ],
            "Configuration": [
                {"name": "description", "type": "char"},
                {"name": "validation_rules", "type": "char"},
                {"name": "default_value", "type": "char"},
                {"name": "help_text", "type": "char"},
            ],
        },
    },





    # ───────────────── SAVINGS / PREPAID / MORTGAGE ─────────────────
    "Prepaid": {
        "grid": ["code", "voucher_no", "member_code", "head", "amount", "date", "payment_mode"],
        "sections": {
            "Basic Information": [
                {"name": "code", "type": "char", "required": True},
                {"name": "member_code", "type": "char", "required": True},
                {"name": "voucher_no", "type": "char"},
                {"name": "head", "type": "char"},
                {"name": "status", "type": "char"},
            ],
            "Amount Details": [
                {"name": "amount", "type": "char"},
                {"name": "date", "type": "date"},
                {"name": "payment_mode", "type": "char"},
            ],
            "Notes": [
                {"name": "remarks", "type": "char"},
            ],
        },
    },

    "Mortgage": {
        "grid": ["code", "member_code", "mortgage_date", "mortgage_amount", "collateral_val", "property_type"],
        "sections": {
            "Basic Information": [
                {"name": "code", "type": "char", "required": True},
                {"name": "member_code", "type": "char", "required": True},
                {"name": "mortgage_date", "type": "date"},
                {"name": "status", "type": "char"},
            ],
            "Property Details": [
                {"name": "property_desc", "type": "char"},
                {"name": "deed_no", "type": "char"},
                {"name": "property_type", "type": "char"},
            ],
            "Amounts": [
                {"name": "mortgage_amount", "type": "decimal"},
                {"name": "collateral_val", "type": "decimal"},
            ],
            "Notes": [
                {"name": "remarks", "type": "char"},
            ],
        },
    },

    "ExSaving": {
        "grid": ["code", "account_no", "member_code", "open_date", "amount", "interest_rate", "account_type"],
        "sections": {
            "Basic Information": [
                {"name": "code", "type": "char", "required": True},
                {"name": "account_no", "type": "char"},
                {"name": "member_code", "type": "char", "required": True},
                {"name": "status", "type": "char"},
                {"name": "account_type", "type": "char"},
            ],
            "Account Details": [
                {"name": "open_date", "type": "date"},
                {"name": "amount", "type": "char"},
                {"name": "interest_rate", "type": "char"},
            ],
            "Notes": [
                {"name": "remarks", "type": "char"},
            ],
        },
    },

    # ───────────────── USER PERMISSION ─────────────────
    "UserPermission": {
        "grid": ["user_profile", "is_admin", "is_master", "is_data_entry", "is_accounting", "is_recovery_agent", "is_auditor", "is_manager", "created_date", "last_modified"],
        "sections": {
            "User": [
                {"name": "user_profile", "type": "select", "required": True},
                {"name": "user_name", "type": "char", "readonly": True},
            ],
            "Roles": [
                {"name": "is_admin", "type": "select", "choices": [["True", "Yes"], ["False", "No"]]},
                {"name": "is_master", "type": "select", "choices": [["True", "Yes"], ["False", "No"]]},
                {"name": "is_data_entry", "type": "select", "choices": [["True", "Yes"], ["False", "No"]]},
    
                {"name": "is_accounting", "type": "select", "choices": [["True", "Yes"], ["False", "No"]]},
                {"name": "is_recovery_agent", "type": "select", "choices": [["True", "Yes"], ["False", "No"]]},
                {"name": "is_auditor", "type": "select", "choices": [["True", "Yes"], ["False", "No"]]},
                {"name": "is_manager", "type": "select", "choices": [["True", "Yes"], ["False", "No"]]},
            ],
            "Status": [
                {"name": "status", "type": "char"},
            ],
            "Audit": [
                {"name": "created_date", "type": "date"},
                {"name": "last_modified", "type": "date"},
                {"name": "modified_by", "type": "char"},
            ],
        },
    },
}
