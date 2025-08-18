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
}
