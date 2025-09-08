# companies/urls_sml.py
# SML Project URL Configuration
# Integrates with existing Django system
# Preserves all existing functionality

from django.urls import path
from . import views

# SML Project specific URL patterns
urlpatterns = [
    # ========================================
    # SML PROJECT DASHBOARD
    # ========================================
    path('sml-dashboard/', views.sml_dashboard, name='sml_dashboard'),
    path('sml-overview/', views.sml_overview, name='sml_overview'),
    
    # ========================================
    # LOAN MANAGEMENT SYSTEM
    # ========================================
    path('loans/', views.loan_list, name='loan_list'),
    path('loans/create/', views.loan_create, name='loan_create'),
    path('loans/<int:loan_id>/', views.loan_detail, name='loan_detail'),
    path('loans/<int:loan_id>/edit/', views.loan_edit, name='loan_edit'),
    path('loans/<int:loan_id>/delete/', views.loan_delete, name='loan_delete'),
    path('loans/<int:loan_id>/restructure/', views.loan_restructure, name='loan_restructure'),
    path('loans/<int:loan_id>/approve/', views.loan_approve, name='loan_approve'),
    path('loans/<int:loan_id>/reject/', views.loan_reject, name='loan_reject'),
    
    # ========================================
    # CLIENT MANAGEMENT SYSTEM
    # ========================================
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.client_create, name='client_create'),
    path('clients/<int:client_id>/', views.client_detail, name='client_detail'),
    path('clients/<int:client_id>/edit/', views.client_edit, name='client_edit'),
    path('clients/<int:client_id>/delete/', views.client_delete, name='client_delete'),
    path('clients/<int:client_id>/kyc/', views.client_kyc, name='client_kyc'),
    path('clients/<int:client_id>/kyc/upload/', views.kyc_upload, name='kyc_upload'),
    path('clients/<int:client_id>/kyc/verify/', views.kyc_verify, name='kyc_verify'),
    
    # ========================================
    # FIELD OPERATIONS SYSTEM
    # ========================================
    path('field-schedule/', views.field_schedule_list, name='field_schedule_list'),
    path('field-schedule/create/', views.field_schedule_create, name='field_schedule_create'),
    path('field-schedule/<int:schedule_id>/', views.field_schedule_detail, name='field_schedule_detail'),
    path('field-schedule/<int:schedule_id>/edit/', views.field_schedule_edit, name='field_schedule_edit'),
    path('field-schedule/<int:schedule_id>/delete/', views.field_schedule_delete, name='field_schedule_delete'),
    path('field-visits/', views.field_visit_list, name='field_visit_list'),
    path('field-visits/<int:visit_id>/complete/', views.field_visit_complete, name='field_visit_complete'),
    
    # ========================================
    # NPA MANAGEMENT SYSTEM
    # ========================================
    path('npa/', views.npa_list, name='npa_list'),
    path('npa/analysis/', views.npa_analysis, name='npa_analysis'),
    path('npa/reports/', views.npa_reports, name='npa_reports'),
    path('npa/<int:npa_id>/', views.npa_detail, name='npa_detail'),
    path('npa/<int:npa_id>/resolve/', views.npa_resolve, name='npa_resolve'),
    
    # ========================================
    # CREDIT BUREAU INTEGRATION
    # ========================================
    path('credit-bureau/', views.credit_bureau_dashboard, name='credit_bureau_dashboard'),
    path('credit-bureau/pull-report/', views.credit_bureau_pull_report, name='credit_bureau_pull_report'),
    path('credit-bureau/reports/<int:report_id>/', views.credit_bureau_report_detail, name='credit_bureau_report_detail'),
    
    # ========================================
    # FINANCIAL REPORTS SYSTEM
    # ========================================
    path('financial-reports/', views.financial_reports_list, name='financial_reports_list'),
    path('financial-reports/portfolio/', views.portfolio_report, name='portfolio_report'),
    path('financial-reports/collection/', views.collection_report, name='collection_report'),
    path('financial-reports/disbursement/', views.disbursement_report, name='disbursement_report'),
    path('financial-reports/export/<str:report_type>/', views.export_report, name='export_report'),
    
    # ========================================
    # AI ANALYTICS SYSTEM
    # ========================================
    path('ai-analytics/', views.ai_analytics_dashboard, name='ai_analytics_dashboard'),
    path('ai-analytics/credit-risk/', views.ai_credit_risk_analysis, name='ai_credit_risk_analysis'),
    path('ai-analytics/portfolio-optimization/', views.ai_portfolio_optimization, name='ai_portfolio_optimization'),
    path('ai-analytics/collection-strategy/', views.ai_collection_strategy, name='ai_collection_strategy'),
    
    # ========================================
    # API ENDPOINTS FOR SML PROJECT
    # ========================================
    path('api/loans/', views.api_loan_list, name='api_loan_list'),
    path('api/loans/<int:loan_id>/', views.api_loan_detail, name='api_loan_detail'),
    path('api/clients/', views.api_client_list, name='api_client_list'),
    path('api/clients/<int:client_id>/', views.api_client_detail, name='api_client_detail'),
    path('api/field-schedule/', views.api_field_schedule_list, name='api_field_schedule_list'),
    path('api/npa/', views.api_npa_list, name='api_npa_list'),
    path('api/reports/', views.api_reports_list, name='api_reports_list'),
    path('api/credit-bureau/', views.api_credit_bureau, name='api_credit_bureau'),
    
    # ========================================
    # SML PROJECT UTILITIES
    # ========================================
    path('sml-utils/calculate-emi/', views.calculate_emi, name='calculate_emi'),
    path('sml-utils/credit-score-calculator/', views.credit_score_calculator, name='credit_score_calculator'),
    path('sml-utils/loan-eligibility/', views.loan_eligibility_check, name='loan_eligibility_check'),
    path('sml-utils/risk-assessment/', views.risk_assessment, name='risk_assessment'),
    
    # ========================================
    # SML PROJECT SETTINGS
    # ========================================
    path('sml-settings/', views.sml_settings, name='sml_settings'),
    path('sml-settings/loan-types/', views.loan_types_settings, name='loan_types_settings'),
    path('sml-settings/interest-rates/', views.interest_rates_settings, name='interest_rates_settings'),
    path('sml-settings/credit-bureau/', views.credit_bureau_settings, name='credit_bureau_settings'),
    path('sml-settings/ai-models/', views.ai_models_settings, name='ai_models_settings'),
]


