# companies/forms_spec.py
# Single source of truth for grid columns and modal sections.
# Use "extra__" for fields not in your DB models; they'll be saved into extra_data.

FORMS_SPEC = {
    # ───────────────── COMPANY ─────────────────
    "Company": {
        "grid": ["code", "name", "phone", "opening_date", "extra__mortgage"],
        "sections": {
            "Basic Information": [
                {"name": "code", "type": "char", "required": True},
                {"name": "name", "type": "char", "required": True},
                {"name": "opening_date", "type": "date"},
                {"name": "status", "type": "char"},
                {"name": "extra__mortgage", "type": "char"},
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
        "grid": ["code", "name", "company", "phone", "open_date", "extra__branch_manager"],
        "sections": {
            "Basic Information": [
                {"name": "code", "type": "char", "required": True},
                {"name": "name", "type": "char", "required": True},
                {"name": "company", "type": "foreign_key", "model": "Company", "required": True},
                {"name": "open_date", "type": "date"},
                {"name": "status", "type": "char"},
                {"name": "extra__branch_manager", "type": "char"},
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
        "grid": ["VCode", "VName", "branch", "TDate", "extra__population", "extra__village_type"],
        "sections": {
            "Basic Information": [
                {"name": "VCode", "type": "char", "required": True},
                {"name": "VName", "type": "char", "required": True},
                {"name": "branch", "type": "foreign_key", "model": "Branch"},
                {"name": "TDate", "type": "date"},
                {"name": "status", "type": "char"},
                {"name": "extra__population", "type": "int"},
                {"name": "extra__village_type", "type": "char"},
            ],
        },
    },

    # ───────────────── CENTER ─────────────────
    "Center": {
        "grid": ["code", "name", "village", "collection_day", "created_on", "extra__member_count"],
        "sections": {
            "Basic Information": [
                {"name": "code", "type": "char", "required": True},
                {"name": "name", "type": "char", "required": True},
                {"name": "village", "type": "char"},
                {"name": "created_on", "type": "date"},
                {"name": "status", "type": "char"},
                {"name": "extra__member_count", "type": "int"},
            ],
            "Meeting Details": [
                {"name": "collection_day", "type": "char"},
                {"name": "meet_place", "type": "char"},
            ],
        },
    },

    # ───────────────── GROUP ─────────────────
    "Group": {
        "grid": ["code", "name", "center", "week_day", "borrower_count", "extra__formation_date"],
        "sections": {
            "Basic Information": [
                {"name": "code", "type": "char", "required": True},
                {"name": "name", "type": "char", "required": True},
                {"name": "center", "type": "char"},
                {"name": "borrower_count", "type": "int"},
                {"name": "status", "type": "char"},
                {"name": "extra__formation_date", "type": "date"},
            ],
            "Meeting Details": [
                {"name": "week_day", "type": "char"},
                {"name": "meeting_time", "type": "char"},
            ],
        },
    },

    # ───────────────── ROLE ─────────────────
    "Role": {
        "grid": ["name", "extra__description", "extra__permission_count"],
        "sections": {
            "Basic Information": [
                {"name": "name", "type": "char", "required": True},
                {"name": "permissions", "type": "char"},
                {"name": "extra__description", "type": "char"},
                {"name": "extra__permission_count", "type": "int"},
            ],
        },
    },

    # ───────────────── CADRE ─────────────────
    "Cadre": {
        "grid": ["name", "branch", "extra__designation_level", "extra__salary_grade"],
        "sections": {
            "Basic Information": [
                {"name": "name", "type": "char", "required": True},
                {"name": "branch", "type": "char", "required": True},
                {"name": "status", "type": "char"},
                {"name": "extra__designation_level", "type": "char"},
                {"name": "extra__salary_grade", "type": "char"},
            ],
        },
    },

    # ───────────────── STAFF ─────────────────
    "Staff": {
        "grid": ["staffcode", "name", "designation", "branch", "contact1", "joining_date", "extra__department"],
        "sections": {
            "Basic Information": [
                {"name": "staffcode", "type": "char", "required": True},
                {"name": "name", "type": "char", "required": True},
                {"name": "branch", "type": "foreign_key", "model": "Branch"},
                {"name": "cadre", "type": "foreign_key", "model": "Cadre"},
                {"name": "status", "type": "char"},
            ],
            "Identity & KYC": [
                {"name": "extra__aadhaar_number", "type": "char", "required": True},
                {"name": "extra__gender", "type": "char"},
                {"name": "extra__date_of_birth", "type": "date"},
                {"name": "photo", "type": "image"},
                {"name": "extra__kyc_documents", "type": "file"},
                {"name": "extra__biometric_data", "type": "file"},
            ],
            "Contact": [
                {"name": "contact1", "type": "char", "required": True},
                {"name": "extra__email_id", "type": "char"},
                {"name": "extra__residential_address", "type": "char"},
                {"name": "extra__emergency_contact", "type": "char"},
            ],
            "Employment": [
                {"name": "designation", "type": "char"},
                {"name": "joining_date", "type": "date"},
                {"name": "extra__department", "type": "char"},
                {"name": "extra__employee_id", "type": "char"},
                {"name": "extra__educational_qualifications", "type": "char"},
                {"name": "extra__work_experience", "type": "char"},
                {"name": "extra__professional_certifications", "type": "char"},
            ],
            "Bank & PAN": [
                {"name": "bank", "type": "char"},
                {"name": "ifsc", "type": "char"},
                {"name": "extra__bank_account_details", "type": "char"},
                {"name": "extra__pan_number", "type": "char"},
            ],
        },
    },

    # ───────────────── USERS ─────────────────
    "Users": {
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
        "grid": ["code", "name", "category", "extra__interest_rate", "extra__loan_amount_range"],
        "sections": {
            "Basic Information": [
                {"name": "code", "type": "char", "required": True},
                {"name": "name", "type": "char", "required": True},
                {"name": "category", "type": "char"},
                {"name": "status", "type": "char"},
                {"name": "extra__interest_rate", "type": "char"},
                {"name": "extra__loan_amount_range", "type": "char"},
            ],
        },
    },

    # ───────────────── CLIENT (Borrower) ─────────────────
    "Client": {
        "grid": ["smtcode", "name", "group", "contactno", "join_date", "extra__occupation", "extra__annual_income"],
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
                {"name": "extra__date_of_birth", "type": "date"},
                {"name": "extra__residential_address", "type": "char"},
                {"name": "extra__photograph", "type": "image"},
                {"name": "extra__kyc_documents", "type": "file"},
                {"name": "extra__biometric_data", "type": "file"},
            ],
            "Contact": [
                {"name": "contactno", "type": "char", "required": True},
                {"name": "extra__email_id", "type": "char"},
                {"name": "extra__marital_status", "type": "char"},
            ],
            "Financials": [
                {"name": "extra__occupation", "type": "char"},
                {"name": "extra__annual_income", "type": "int"},
                {"name": "extra__pan_number", "type": "char"},
                {"name": "extra__bank_account_details", "type": "char"},
                {"name": "extra__credit_score", "type": "int"},
            ],
            "Loan Details": [
                {"name": "extra__loan_purpose", "type": "char"},
                {"name": "extra__guarantor_details", "type": "char"},
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
        "grid": ["report_date", "schedule", "summary", "extra__visit_duration", "extra__outcome", "extra__photo_count"],
        "sections": {
            "Basic Information": [
                {"name": "report_date", "type": "date"},
                {"name": "schedule", "type": "foreign_key", "model": "FieldSchedule"},
            ],
            "Report": [
                {"name": "summary", "type": "text"},
                {"name": "extra__visit_duration", "type": "int"},
                {"name": "extra__outcome", "type": "char"},
                {"name": "extra__photo_count", "type": "int"},
            ],
            "Attachments": [
                {"name": "extra__photo_1", "type": "image"},
                {"name": "extra__photo_2", "type": "image"},
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
                {"name": "extra__total_visits", "type": "int"},
                {"name": "extra__total_clients", "type": "int"},
                {"name": "extra__total_collections", "type": "int"},
            ],
        },
    },

    # ───────────────── MONTHLY REPORT ─────────────────
    "MonthlyReport": {
        "grid": ["period_start", "period_end", "generated_on", "extra__total_loans", "extra__total_disbursements", "extra__total_recoveries"],
        "sections": {
            "Basic Information": [
                {"name": "period_start", "type": "date"},
                {"name": "period_end", "type": "date"},
                {"name": "generated_on", "type": "date"},
            ],
            "Report": [
                {"name": "summary", "type": "char"},
                {"name": "extra__total_loans", "type": "int"},
                {"name": "extra__total_disbursements", "type": "int"},
                {"name": "extra__total_recoveries", "type": "int"},
            ],
        },
    },

    # ───────────────── BUSINESS SETTINGS ─────────────────
    "BusinessSetting": {
        "grid": ["key", "value", "company", "extra__category", "extra__description"],
        "sections": {
            "Basic Information": [
                {"name": "key", "type": "char", "required": True},
                {"name": "value", "type": "char", "required": True},
                {"name": "company", "type": "char"},
                {"name": "extra__category", "type": "char"},
                {"name": "extra__description", "type": "char"},
            ],
        },
    },

    # ───────────────── ACCOUNTING ─────────────────
    "AccountHead": {
        "grid": ["code", "name", "parent", "ac_type", "extra__description", "extra__opening_balance"],
        "sections": {
            "Basic Information": [
                {"name": "code", "type": "char", "required": True},
                {"name": "name", "type": "char", "required": True},
                {"name": "parent", "type": "foreign_key", "model": "AccountHead"},
                {"name": "status", "type": "char"},
                {"name": "extra__description", "type": "char"},
                {"name": "extra__opening_balance", "type": "decimal"},
            ],
            "Details": [
                {"name": "abbreviation", "type": "char"},
                {"name": "ac_type", "type": "char"},
                {"name": "vtype", "type": "char"},
            ],
        },
    },

    "Voucher": {
        "grid": ["voucher_no", "date", "account_head", "debit_total", "credit_total", "extra__voucher_type"],
        "sections": {
            "Basic Information": [
                {"name": "voucher_no", "type": "char", "required": True},
                {"name": "date", "type": "date", "required": True},
                {"name": "account_head", "type": "foreign_key", "model": "AccountHead", "required": True},
                {"name": "status", "type": "char"},
                {"name": "extra__voucher_type", "type": "char"},
            ],
            "Details": [
                {"name": "narration", "type": "char"},
                {"name": "debit_total", "type": "decimal"},
                {"name": "credit_total", "type": "decimal"},
            ],
        },
    },

    "Posting": {
        "grid": ["voucher", "account_head", "debit", "credit", "narration", "extra__reference"],
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
                {"name": "extra__reference", "type": "char"},
            ],
        },
    },

    "RecoveryPosting": {
        "grid": ["client", "date", "amount", "voucher", "extra__recovery_type", "extra__agent"],
        "sections": {
            "Basic Information": [
                {"name": "client", "type": "foreign_key", "model": "Client", "required": True},
                {"name": "date", "type": "date", "required": True},
                {"name": "voucher", "type": "foreign_key", "model": "Voucher"},
                {"name": "status", "type": "char"},
                {"name": "extra__recovery_type", "type": "char"},
                {"name": "extra__agent", "type": "char"},
            ],
            "Amount": [
                {"name": "amount", "type": "char", "required": True},
            ],
        },
    },

    # ───────────────── KYC DOCUMENTS ─────────────────
    # Basis: ID proof capture, linkage to party, verification workflow.
    "KYCDocument": {
        "grid": ["extra__party_name", "extra__doc_type", "extra__doc_no", "extra__issue_date", "extra__expiry_date", "extra__verified_by", "extra__verification_status"],
        "sections": {
            "Document": [
                {"name": "extra__doc_type", "type": "char", "required": True},
                {"name": "extra__doc_no", "type": "char"},
                {"name": "extra__name_on_doc", "type": "char"},
                {"name": "extra__issue_date", "type": "date"},
                {"name": "extra__expiry_date", "type": "date"},
                {"name": "extra__document_file", "type": "file"},
                {"name": "extra__document_image", "type": "image"},
            ],
            "Holder": [
                {"name": "extra__party_type", "type": "char"},   # Client/Staff
                {"name": "extra__party_id", "type": "char"},
                {"name": "extra__party_name", "type": "char"},
                {"name": "extra__dob", "type": "date"},
                {"name": "extra__address", "type": "char"},
            ],
            "Verification": [
                {"name": "extra__verified_by", "type": "char"},
                {"name": "extra__verified_on", "type": "date"},
                {"name": "extra__verification_remarks", "type": "char"},
                {"name": "extra__verification_status", "type": "char"},
            ],
        },
    },

    # ───────────────── ALERT RULES ─────────────────
    # Basis: event condition, recipients, delivery, status.
    "AlertRule": {
        "grid": ["extra__name", "extra__severity", "extra__entity", "extra__channel", "extra__is_active", "extra__last_triggered", "extra__trigger_count"],
        "sections": {
            "Definition": [
                {"name": "extra__name", "type": "char", "required": True},
                {"name": "extra__severity", "type": "char"},
                {"name": "extra__condition", "type": "char"},   # e.g., DSL or JSON
                {"name": "extra__entity", "type": "char"},      # Loan/Client/Recovery
                {"name": "extra__channel", "type": "char"},     # Email/SMS/InApp
            ],
            "Targets": [
                {"name": "extra__branch", "type": "char"},
                {"name": "extra__role", "type": "char"},
                {"name": "extra__recipients", "type": "char"},  # comma emails/phones
            ],
            "Delivery": [
                {"name": "extra__template", "type": "char"},
                {"name": "extra__schedule", "type": "char"},    # immediate/daily/cron
            ],
            "Status": [
                {"name": "extra__is_active", "type": "char"},   # Y/N
                {"name": "extra__last_triggered", "type": "date"},
                {"name": "extra__trigger_count", "type": "int"},
            ],
        },
    },

    # ───────────────── HR: APPOINTMENT ─────────────────
    "Appointment": {
        "grid": ["staff", "appointment_date", "designation", "branch", "extra__appointment_type", "extra__remarks"],
        "sections": {
            "Basic Information": [
                {"name": "staff", "type": "char", "required": True},
                {"name": "appointment_date", "type": "date"},
                {"name": "designation", "type": "char"},
                {"name": "branch", "type": "char"},
                {"name": "status", "type": "char"},
            ],
            "Details": [
                {"name": "extra__appointment_type", "type": "char"},
                {"name": "remarks", "type": "char"},
            ],
        },
    },

    # ───────────────── HR: SALARY STATEMENT ─────────────────
    "SalaryStatement": {
        "grid": ["staff", "month", "year", "basic_pay", "net_pay", "extra__total_allowances", "extra__total_deductions"],
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
                {"name": "extra__total_allowances", "type": "decimal"},
                {"name": "extra__total_deductions", "type": "decimal"},
                {"name": "extra__gross_salary", "type": "decimal"},
            ],
        },
    },

    # ───────────────── LOAN LIFECYCLE ─────────────────
    "LoanApplication": {
        "grid": ["application_number", "client", "product", "amount_requested", "interest_rate", "tenure_months", "applied_date", "extra__loan_purpose"],
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
                {"name": "extra__loan_purpose", "type": "char"},
                {"name": "extra__guarantor_details", "type": "char"},
                {"name": "extra__bureau_score", "type": "int"},
                {"name": "extra__remarks", "type": "char"},
            ],
        },
    },

    "LoanApproval": {
        "grid": ["loan_application", "approved_amount", "approval_date", "approver", "extra__conditions"],
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
                {"name": "extra__conditions", "type": "char"},
                {"name": "extra__remarks", "type": "char"},
            ],
        },
    },

    "Disbursement": {
        "grid": ["loan_application", "amount", "disbursement_date", "channel", "extra__utr_no"],
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
                {"name": "extra__utr_no", "type": "char"},
                {"name": "extra__receipt", "type": "file"},
            ],
        },
    },

    # ───────────────── PAYMENTS / REPAYMENTS ─────────────────
    "Payment": {
        "grid": ["loan_application", "amount", "gateway", "order_id", "extra__payer_name", "extra__payer_phone"],
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
                {"name": "extra__payer_name", "type": "char"},
                {"name": "extra__payer_phone", "type": "char"},
                {"name": "extra__notes", "type": "char"},
            ],
        },
    },

    "Repayment": {
        "grid": ["loan_application", "paid_on", "amount", "mode", "reference", "extra__installment_no"],
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
                {"name": "extra__installment_no", "type": "int"},
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
        "grid": ["channel", "to_address", "subject", "sent_at", "extra__recipient_type"],
        "sections": {
            "Basic Information": [
                {"name": "channel", "type": "char", "required": True},
                {"name": "to_address", "type": "char", "required": True},
                {"name": "status", "type": "char"},
                {"name": "extra__recipient_type", "type": "char"},
            ],
            "Message": [
                {"name": "subject", "type": "char"},
                {"name": "body", "type": "char", "required": True},
                {"name": "sent_at", "type": "date"},
            ],
        },
    },

    "GatewayEvent": {
        "grid": ["gateway", "event", "received_at", "signature_ok", "extra__event_data", "extra__processing_status"],
        "sections": {
            "Basic Information": [
                {"name": "gateway", "type": "char", "required": True},
                {"name": "event", "type": "char", "required": True},
                {"name": "signature_ok", "type": "char"},
                {"name": "received_at", "type": "date"},
            ],
            "Event Details": [
                {"name": "extra__event_data", "type": "char"},
                {"name": "extra__processing_status", "type": "char"},
            ],
        },
    },

    "EWIFlag": {
        "grid": ["loan_application", "code", "active", "raised_at", "cleared_at", "extra__severity", "extra__description"],
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
                {"name": "extra__severity", "type": "char"},
                {"name": "extra__description", "type": "char"},
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
        "grid": ["module", "field_name", "label", "field_type", "required", "order", "extra__description", "extra__validation_rules"],
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
                {"name": "extra__description", "type": "char"},
                {"name": "extra__validation_rules", "type": "char"},
                {"name": "extra__default_value", "type": "char"},
                {"name": "extra__help_text", "type": "char"},
            ],
        },
    },





    # ───────────────── SAVINGS / PREPAID / MORTGAGE ─────────────────
    "Prepaid": {
        "grid": ["code", "voucher_no", "member_code", "head", "amount", "date", "extra__payment_mode"],
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
                {"name": "extra__payment_mode", "type": "char"},
            ],
            "Notes": [
                {"name": "remarks", "type": "char"},
            ],
        },
    },

    "Mortgage": {
        "grid": ["code", "member_code", "mortgage_date", "mortgage_amount", "collateral_val", "extra__property_type"],
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
                {"name": "extra__property_type", "type": "char"},
            ],
            "Amounts": [
                {"name": "mortgage_amount", "type": "char"},
                {"name": "collateral_val", "type": "char"},
            ],
            "Notes": [
                {"name": "remarks", "type": "char"},
            ],
        },
    },

    "ExSaving": {
        "grid": ["code", "account_no", "member_code", "open_date", "amount", "extra__interest_rate", "extra__account_type"],
        "sections": {
            "Basic Information": [
                {"name": "code", "type": "char", "required": True},
                {"name": "account_no", "type": "char"},
                {"name": "member_code", "type": "char", "required": True},
                {"name": "status", "type": "char"},
                {"name": "extra__account_type", "type": "char"},
            ],
            "Account Details": [
                {"name": "open_date", "type": "date"},
                {"name": "amount", "type": "char"},
                {"name": "extra__interest_rate", "type": "char"},
            ],
            "Notes": [
                {"name": "remarks", "type": "char"},
            ],
        },
    },

    # ───────────────── ROLE MANAGEMENT ─────────────────
    "Role": {
        "grid": ["name", "description", "is_active", "extra__permission_count", "extra__created_date"],
        "sections": {
            "Basic Information": [
                {"name": "name", "type": "char", "required": True},
                {"name": "description", "type": "char"},
                {"name": "is_active", "type": "select", "choices": [["True", "Active"], ["False", "Inactive"]]},
            ],
            "Permissions": [
                {"name": "permissions", "type": "char"},
                {"name": "extra__permission_count", "type": "int", "readonly": True},
            ],
            "Audit": [
                {"name": "extra__created_date", "type": "date"},
                {"name": "extra__last_modified", "type": "date"},
                {"name": "extra__modified_by", "type": "char"},
            ],
        },
    },

    # ───────────────── USER PERMISSION ─────────────────
    "UserPermission": {
        "grid": ["user_profile", "is_admin", "is_master", "is_data_entry", "is_accounting", "is_recovery_agent", "is_auditor", "is_manager", "extra__created_date", "extra__last_modified"],
        "sections": {
            "User": [
                {"name": "user_profile", "type": "select", "required": True},
                {"name": "extra__user_name", "type": "char", "readonly": True},
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
                {"name": "extra__created_date", "type": "date"},
                {"name": "extra__last_modified", "type": "date"},
                {"name": "extra__modified_by", "type": "char"},
            ],
        },
    },
}
