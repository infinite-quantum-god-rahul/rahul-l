# companies/forms_spec.py
# Single source of truth for grid columns and modal sections.
# Use "extra__" for fields not in your DB models; they’ll be saved into extra_data.

FORMS_SPEC = {
    # ───────────────── STAFF ─────────────────
    # Basis: Staff Enrollment mandatory + additional fields, plus photo/KYC/biometric. :contentReference[oaicite:0]{index=0} :contentReference[oaicite:1]{index=1}
    "Staff": {
        "grid": ["name", "designation", "contact1", "joining_date"],  # minimal business columns
        "sections": {
            "Identity & KYC": [
                {"name": "extra__aadhaar_number", "type": "char", "required": True},
                {"name": "extra__gender", "type": "char"},
                {"name": "extra__date_of_birth", "type": "date"},
                {"name": "photo", "type": "image"},                         # model field already exists
                {"name": "extra__kyc_documents", "type": "file"},
                {"name": "extra__biometric_data", "type": "file"},
            ],
            "Contact": [
                {"name": "contact1", "type": "char", "required": True},     # model field
                {"name": "extra__email_id", "type": "char"},
                {"name": "extra__residential_address", "type": "char"},
                {"name": "extra__emergency_contact", "type": "char"},
            ],
            "Employment": [
                {"name": "designation", "type": "char"},                    # model field
                {"name": "extra__department", "type": "char"},
                {"name": "joining_date", "type": "date"},                   # model field
                {"name": "extra__employee_id", "type": "char"},
                {"name": "extra__educational_qualifications", "type": "char"},
                {"name": "extra__work_experience", "type": "char"},
                {"name": "extra__professional_certifications", "type": "char"},
            ],
            "Bank & PAN": [
                {"name": "extra__bank_account_details", "type": "char"},
                {"name": "extra__pan_number", "type": "char"},
            ],
        },
    },

    # ───────────────── CLIENT (Borrower) ─────────────────
    # Basis: Borrower Enrollment mandatory + additional. :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}
    "Client": {
        "grid": ["name", "extra__aadhaar_number", "extra__contact_number", "extra__occupation"],
        "sections": {
            "Identity & KYC": [
                {"name": "extra__aadhaar_number", "type": "char", "required": True},
                {"name": "extra__gender", "type": "char"},
                {"name": "extra__date_of_birth", "type": "date"},
                {"name": "extra__residential_address", "type": "char"},
                {"name": "extra__photograph", "type": "image"},
                {"name": "extra__kyc_documents", "type": "file"},
                {"name": "extra__biometric_data", "type": "file"},
            ],
            "Contact": [
                {"name": "name", "type": "char", "required": True},          # model field
                {"name": "extra__contact_number", "type": "char", "required": True},
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
    # Basis: Route / Center / Group mapping + example columns. :contentReference[oaicite:4]{index=4} :contentReference[oaicite:5]{index=5}
    "FieldSchedule": {
        "grid": ["route", "center", "group", "staff"],  # minimal ops view
        "sections": {
            "Assignment": [
                {"name": "route", "type": "char"},
                {"name": "center", "type": "char"},
                {"name": "group", "type": "char"},
                {"name": "staff", "type": "char"},
            ],
            "Notes": [
                {"name": "extra__remarks", "type": "char"},
            ],
        },
    },

    # ───────────────── PRODUCT / BUSINESS SETTINGS ─────────────────
    # Basis: Tenure and ROI definitions and product config. :contentReference[oaicite:6]{index=6}
    "Product": {
        "grid": ["name", "extra__roi", "extra__tenure_months"],
        "sections": {
            "Core": [
                {"name": "name", "type": "char"},                # model field
                {"name": "extra__tenure_months", "type": "int"},
                {"name": "extra__roi", "type": "char"},
            ],
            "Rules": [
                {"name": "extra__emi_method", "type": "char"},
                {"name": "extra__processing_fee", "type": "char"},
            ],
        },
    },

    "BusinessSetting": {
        "grid": ["extra__product_code", "extra__roi_default", "extra__tenure_default"],
        "sections": {
            "Defaults": [
                {"name": "extra__product_code", "type": "char"},
                {"name": "extra__tenure_default", "type": "int"},
                {"name": "extra__roi_default", "type": "char"},
            ],
            "Limits": [
                {"name": "extra__min_amount", "type": "int"},
                {"name": "extra__max_amount", "type": "int"},
            ],
        },
    },

    # ───────────────── KYC DOCUMENTS ─────────────────
    # Basis: ID proof capture, linkage to party, verification workflow.
    "KYCDocument": {
        "grid": ["extra__party_name", "extra__doc_type", "extra__doc_no", "extra__expiry_date"],
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
            ],
        },
    },

    # ───────────────── ALERT RULES ─────────────────
    # Basis: event condition, recipients, delivery, status.
    "AlertRule": {
        "grid": ["extra__name", "extra__channel", "extra__is_active"],
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
            ],
        },
    },

    # ───────────────── HR: APPOINTMENT ─────────────────
    # Basis: offer details, compensation, docs, probation.
    "Appointment": {
        "grid": ["extra__employee_name", "extra__appointment_date", "extra__designation"],
        "sections": {
            "Appointment": [
                {"name": "extra__employee_id", "type": "char"},
                {"name": "extra__employee_name", "type": "char"},
                {"name": "extra__appointment_date", "type": "date", "required": True},
                {"name": "extra__designation", "type": "char"},
                {"name": "extra__department", "type": "char"},
                {"name": "extra__reporting_manager", "type": "char"},
            ],
            "Compensation": [
                {"name": "extra__pay_grade", "type": "char"},
                {"name": "extra__ctc", "type": "int"},
            ],
            "Documents": [
                {"name": "extra__offer_letter", "type": "file"},
                {"name": "extra__joining_report", "type": "file"},
            ],
            "Meta": [
                {"name": "extra__probation_months", "type": "int"},
                {"name": "extra__remarks", "type": "char"},
            ],
        },
    },

    # ───────────────── HR: SALARY STATEMENT ─────────────────
    # Basis: monthly payroll with bank and payout info.
    "SalaryStatement": {
        "grid": ["extra__employee_name", "extra__month", "extra__net_pay"],
        "sections": {
            "Payroll": [
                {"name": "extra__employee_id", "type": "char"},
                {"name": "extra__employee_name", "type": "char"},
                {"name": "extra__month", "type": "char"},       # e.g., 2025-08
                {"name": "extra__year", "type": "int"},
                {"name": "extra__gross", "type": "int"},
                {"name": "extra__deductions", "type": "int"},
                {"name": "extra__net_pay", "type": "int"},
            ],
            "Bank": [
                {"name": "extra__bank_account", "type": "char"},
                {"name": "extra__ifsc", "type": "char"},
                {"name": "extra__payment_date", "type": "date"},
                {"name": "extra__payment_mode", "type": "char"},  # NEFT/Cash/UPI
            ],
            "Notes": [
                {"name": "extra__remarks", "type": "char"},
            ],
        },
    },

    # ───────────────── LOAN LIFECYCLE (ADDED) ─────────────────
    "LoanApplication": {
        "grid": ["application_number", "client", "product", "amount_requested", "status"],
        "sections": {
            "Application": [
                {"name": "application_number", "type": "char"},
                {"name": "client", "type": "char"},
                {"name": "product", "type": "char"},
                {"name": "amount_requested", "type": "char"},
                {"name": "interest_rate", "type": "char"},
                {"name": "tenure_months", "type": "int"},
                {"name": "applied_date", "type": "date"},
                {"name": "status", "type": "char"},
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
        "grid": ["loan_application", "approved_amount", "approval_date", "approver"],
        "sections": {
            "Approval": [
                {"name": "loan_application", "type": "char"},
                {"name": "approved_amount", "type": "char"},
                {"name": "approval_date", "type": "date"},
                {"name": "approver", "type": "char"},
                {"name": "status", "type": "char"},
            ],
            "Notes": [
                {"name": "extra__conditions", "type": "char"},
                {"name": "extra__remarks", "type": "char"},
            ],
        },
    },

    "Disbursement": {
        "grid": ["loan_application", "amount", "disbursement_date", "channel"],
        "sections": {
            "Disbursement": [
                {"name": "loan_application", "type": "char"},
                {"name": "amount", "type": "char"},
                {"name": "disbursement_date", "type": "date"},
                {"name": "channel", "type": "char"},
                {"name": "status", "type": "char"},
            ],
            "Proof": [
                {"name": "extra__utr_no", "type": "char"},
                {"name": "extra__receipt", "type": "file"},
            ],
        },
    },

    # ───────────────── PAYMENTS / REPAYMENTS (ADDED) ─────────────────
    "Payment": {
        "grid": ["loan_application", "amount", "gateway", "status", "order_id"],
        "sections": {
            "Intent": [
                {"name": "loan_application", "type": "char"},
                {"name": "amount", "type": "char"},
                {"name": "gateway", "type": "char"},
                {"name": "order_id", "type": "char"},
                {"name": "status", "type": "char"},
            ],
            "Gateway": [
                {"name": "txn_ref", "type": "char"},
                {"name": "extra__redirect_url", "type": "char"},
            ],
            "Meta": [
                {"name": "extra__payer_name", "type": "char"},
                {"name": "extra__payer_phone", "type": "char"},
                {"name": "extra__notes", "type": "char"},
            ],
        },
    },

    "Repayment": {
        "grid": ["loan_application", "paid_on", "amount", "mode", "reference"],
        "sections": {
            "Repayment": [
                {"name": "loan_application", "type": "char"},
                {"name": "paid_on", "type": "date"},
                {"name": "amount", "type": "char"},
                {"name": "mode", "type": "char"},          # cash|upi|neft|auto
                {"name": "reference", "type": "char"},
                {"name": "status", "type": "char"},
            ],
            "Notes": [
                {"name": "notes", "type": "char"},
                {"name": "extra__collector", "type": "char"},
            ],
        },
    },

    "LoanRestructure": {
        "grid": ["loan_application", "effective_from", "new_tenure", "new_rate"],
        "sections": {
            "Terms": [
                {"name": "loan_application", "type": "char"},
                {"name": "effective_from", "type": "date"},
                {"name": "old_tenure", "type": "int"},
                {"name": "old_rate", "type": "char"},
                {"name": "new_tenure", "type": "int"},
                {"name": "new_rate", "type": "char"},
                {"name": "reason", "type": "char"},
                {"name": "status", "type": "char"},
            ],
            "Audit": [
                {"name": "extra__approved_by", "type": "char"},
                {"name": "extra__approval_note", "type": "char"},
            ],
        },
    },

    # ───────────────── EVENTS / NOTIFICATIONS / RISK (ADDED) ─────────────────
    "Notification": {
        "grid": ["channel", "to_address", "status", "sent_at"],
        "sections": {
            "Message": [
                {"name": "channel", "type": "char"},
                {"name": "to_address", "type": "char"},
                {"name": "subject", "type": "char"},
                {"name": "body", "type": "char"},
                {"name": "status", "type": "char"},
                {"name": "sent_at", "type": "date"},
            ],
            "Meta": [
                {"name": "extra__template", "type": "char"},
                {"name": "extra__params", "type": "char"},
            ],
        },
    },

    "GatewayEvent": {
        "grid": ["gateway", "event", "received_at", "signature_ok"],
        "sections": {
            "Event": [
                {"name": "gateway", "type": "char"},
                {"name": "event", "type": "char"},
                {"name": "signature_ok", "type": "char"},
                {"name": "received_at", "type": "date"},
            ],
            "Payload": [
                {"name": "extra__raw", "type": "char"},
            ],
        },
    },

    "EWIFlag": {
        "grid": ["loan_application", "code", "active", "raised_at"],
        "sections": {
            "Flag": [
                {"name": "loan_application", "type": "char"},
                {"name": "code", "type": "char"},
                {"name": "detail", "type": "char"},
                {"name": "active", "type": "char"},
                {"name": "raised_at", "type": "date"},
                {"name": "cleared_at", "type": "date"},
            ],
            "Meta": [
                {"name": "extra__source", "type": "char"},
                {"name": "extra__severity", "type": "char"},
            ],
        },
    },

    # ───────────────── FIELD REPORTS (OPTIONAL) ─────────────────
    "FieldReport": {
        "grid": ["report_date", "schedule", "summary"],
        "sections": {
            "Report": [
                {"name": "report_date", "type": "date"},
                {"name": "schedule", "type": "char"},
                {"name": "summary", "type": "char"},
            ],
            "Attachments": [
                {"name": "extra__photo_1", "type": "image"},
                {"name": "extra__photo_2", "type": "image"},
            ],
        },
    },

    # ───────────────── USER PERMISSIONS (OPTIONAL) ─────────────────
    "UserPermission": {
        "grid": ["user_profile", "is_admin", "is_manager", "status"],
        "sections": {
            "Permissions": [
                {"name": "user_profile", "type": "char"},
                {"name": "is_admin", "type": "char"},
                {"name": "is_master", "type": "char"},
                {"name": "is_data_entry", "type": "char"},
                {"name": "is_accounting", "type": "char"},
                {"name": "is_recovery_agent", "type": "char"},
                {"name": "is_auditor", "type": "char"},
                {"name": "is_manager", "type": "char"},
                {"name": "status", "type": "char"},
            ],
            "Meta": [
                {"name": "extra__scope_branch", "type": "char"},
                {"name": "extra__scope_role", "type": "char"},
            ],
        },
    },

    # ───────────────── SAVINGS / PREPAID / MORTGAGE (NEW) ─────────────────
    "Prepaid": {
        "grid": ["code", "voucher_no", "member_code", "head", "amount", "date"],
        "sections": {
            "Prepaid Details": [
                {"name": "code", "type": "char"},
                {"name": "voucher_no", "type": "char"},          # model field (added)
                {"name": "member_code", "type": "char"},
                {"name": "head", "type": "char"},                # model field (added)
                {"name": "amount", "type": "char"},
                {"name": "date", "type": "date"},
            ],
            "Notes": [
                {"name": "remarks", "type": "char"},
                {"name": "extra__company_id", "type": "char"},
            ],
        },
    },

    "Mortgage": {
        "grid": ["code", "member_code", "mortgage_date", "mortgage_amount"],
        "sections": {
            "Mortgage": [
                {"name": "code", "type": "char"},
                {"name": "member_code", "type": "char"},
                {"name": "mortgage_date", "type": "date"},
                {"name": "property_desc", "type": "char"},
                {"name": "deed_no", "type": "char"},
            ],
            "Amounts": [
                {"name": "mortgage_amount", "type": "char"},
                {"name": "collateral_val", "type": "char"},
            ],
            "Notes": [
                {"name": "remarks", "type": "char"},
                {"name": "extra__company_id", "type": "char"},
            ],
        },
    },

    "ExSaving": {
        "grid": ["code", "account_no", "member_code", "open_date", "amount", "status"],
        "sections": {
            "Account": [
                {"name": "code", "type": "char"},
                {"name": "account_no", "type": "char"},
                {"name": "member_code", "type": "char"},
                {"name": "open_date", "type": "date"},
            ],
            "Status": [
                {"name": "amount", "type": "char"},
                {"name": "status", "type": "char"},
            ],
            "Notes": [
                {"name": "remarks", "type": "char"},
                {"name": "extra__company_id", "type": "char"},
            ],
        },
    },
}
