# companies/views_sml.py
# SML Project Views
# Integrates with existing Django system
# Preserves all existing functionality

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator
from django.utils import timezone
from django.template.loader import render_to_string
import json
import logging

# Import existing models and functions
from .models import *
from .views import role_flags, can_user_delete_entity
from .forms_spec import get_form_spec

logger = logging.getLogger(__name__)

# ========================================
# SML PROJECT DASHBOARD VIEWS
# ========================================

@login_required
def sml_dashboard(request):
    """SML Project Main Dashboard"""
    try:
        # Get user role flags
        user_roles = role_flags(request.user)
        
        # Get dashboard data
        dashboard_data = get_sml_dashboard_data(request.user)
        
        context = {
            'user_roles': user_roles,
            'dashboard_data': dashboard_data,
            'page_title': 'SML Project Dashboard',
            'breadcrumb': [
                {'name': 'Home', 'url': '/'},
                {'name': 'SML Project', 'url': '#'},
                {'name': 'Dashboard', 'url': '#'}
            ]
        }
        
        return render(request, 'sml_dashboard.html', context)
        
    except Exception as e:
        logger.error(f"Error in SML dashboard: {str(e)}")
        messages.error(request, f"Error loading dashboard: {str(e)}")
        return redirect('/')

@login_required
def sml_overview(request):
    """SML Project Overview Page"""
    try:
        user_roles = role_flags(request.user)
        
        context = {
            'user_roles': user_roles,
            'page_title': 'SML Project Overview',
            'breadcrumb': [
                {'name': 'Home', 'url': '/'},
                {'name': 'SML Project', 'url': '#'},
                {'name': 'Overview', 'url': '#'}
            ]
        }
        
        return render(request, 'sml_overview.html', context)
        
    except Exception as e:
        logger.error(f"Error in SML overview: {str(e)}")
        messages.error(request, f"Error loading overview: {str(e)}")
        return redirect('/')

# ========================================
# LOAN MANAGEMENT SYSTEM VIEWS
# ========================================

@login_required
def loan_list(request):
    """List all loans"""
    try:
        user_roles = role_flags(request.user)
        
        # Get loans based on user permissions
        if user_roles.get('admin') or user_roles.get('master'):
            loans = LoanApplication.objects.all().order_by('-created_at')
        elif user_roles.get('manager'):
            loans = LoanApplication.objects.filter(branch=request.user.userprofile.branch).order_by('-created_at')
        else:
            loans = LoanApplication.objects.filter(created_by=request.user).order_by('-created_at')
        
        # Pagination
        paginator = Paginator(loans, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'user_roles': user_roles,
            'loans': page_obj,
            'page_title': 'Loan Applications',
            'breadcrumb': [
                {'name': 'Home', 'url': '/'},
                {'name': 'SML Project', 'url': '#'},
                {'name': 'Loans', 'url': '#'}
            ]
        }
        
        return render(request, 'sml_loan_list.html', context)
        
    except Exception as e:
        logger.error(f"Error in loan list: {str(e)}")
        messages.error(request, f"Error loading loans: {str(e)}")
        return redirect('/')

@login_required
def loan_create(request):
    """Create new loan application"""
    try:
        user_roles = role_flags(request.user)
        
        if request.method == 'POST':
            # Handle loan creation
            loan_data = request.POST.dict()
            loan_data['created_by'] = request.user
            loan_data['branch'] = request.user.userprofile.branch
            
            # Create loan application
            with transaction.atomic():
                loan = LoanApplication.objects.create(**loan_data)
                
                # Create loan schedule
                create_loan_schedule(loan)
                
                messages.success(request, f'Loan application {loan.application_id} created successfully!')
                return redirect('loan_detail', loan_id=loan.id)
        
        context = {
            'user_roles': user_roles,
            'page_title': 'Create Loan Application',
            'breadcrumb': [
                {'name': 'Home', 'url': '/'},
                {'name': 'SML Project', 'url': '#'},
                {'name': 'Loans', 'url': '#'},
                {'name': 'Create', 'url': '#'}
            ]
        }
        
        return render(request, 'sml_loan_create.html', context)
        
    except Exception as e:
        logger.error(f"Error in loan create: {str(e)}")
        messages.error(request, f"Error creating loan: {str(e)}")
        return redirect('loan_list')

@login_required
def loan_detail(request, loan_id):
    """View loan details"""
    try:
        user_roles = role_flags(request.user)
        loan = get_object_or_404(LoanApplication, id=loan_id)
        
        # Check permissions
        if not (user_roles.get('admin') or user_roles.get('master') or 
                loan.created_by == request.user or 
                loan.branch == request.user.userprofile.branch):
            messages.error(request, "You don't have permission to view this loan.")
            return redirect('loan_list')
        
        context = {
            'user_roles': user_roles,
            'loan': loan,
            'page_title': f'Loan {loan.application_id}',
            'breadcrumb': [
                {'name': 'Home', 'url': '/'},
                {'name': 'SML Project', 'url': '#'},
                {'name': 'Loans', 'url': '#'},
                {'name': loan.application_id, 'url': '#'}
            ]
        }
        
        return render(request, 'sml_loan_detail.html', context)
        
    except Exception as e:
        logger.error(f"Error in loan detail: {str(e)}")
        messages.error(request, f"Error loading loan: {str(e)}")
        return redirect('loan_list')

@login_required
def loan_approve(request, loan_id):
    """Approve loan application"""
    try:
        user_roles = role_flags(request.user)
        loan = get_object_or_404(LoanApplication, id=loan_id)
        
        # Check permissions
        if not (user_roles.get('admin') or user_roles.get('master') or user_roles.get('manager')):
            messages.error(request, "You don't have permission to approve loans.")
            return redirect('loan_detail', loan_id=loan.id)
        
        if request.method == 'POST':
            with transaction.atomic():
                loan.status = 'approved'
                loan.approved_by = request.user
                loan.approved_at = timezone.now()
                loan.save()
                
                # Create disbursement record
                create_disbursement_record(loan)
                
                messages.success(request, f'Loan {loan.application_id} approved successfully!')
                return redirect('loan_detail', loan_id=loan.id)
        
        context = {
            'user_roles': user_roles,
            'loan': loan,
            'page_title': f'Approve Loan {loan.application_id}'
        }
        
        return render(request, 'sml_loan_approve.html', context)
        
    except Exception as e:
        logger.error(f"Error in loan approve: {str(e)}")
        messages.error(request, f"Error approving loan: {str(e)}")
        return redirect('loan_detail', loan_id=loan.id)

# ========================================
# CLIENT MANAGEMENT SYSTEM VIEWS
# ========================================

@login_required
def client_list(request):
    """List all clients"""
    try:
        user_roles = role_flags(request.user)
        
        # Get clients based on user permissions
        if user_roles.get('admin') or user_roles.get('master'):
            clients = Client.objects.all().order_by('-created_at')
        elif user_roles.get('manager'):
            clients = Client.objects.filter(branch=request.user.userprofile.branch).order_by('-created_at')
        else:
            clients = Client.objects.filter(created_by=request.user).order_by('-created_at')
        
        # Pagination
        paginator = Paginator(clients, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'user_roles': user_roles,
            'clients': page_obj,
            'page_title': 'Clients',
            'breadcrumb': [
                {'name': 'Home', 'url': '/'},
                {'name': 'SML Project', 'url': '#'},
                {'name': 'Clients', 'url': '#'}
            ]
        }
        
        return render(request, 'sml_client_list.html', context)
        
    except Exception as e:
        logger.error(f"Error in client list: {str(e)}")
        messages.error(request, f"Error loading clients: {str(e)}")
        return redirect('/')

@login_required
def client_detail(request, client_id):
    """View client details"""
    try:
        user_roles = role_flags(request.user)
        client = get_object_or_404(Client, id=client_id)
        
        # Check permissions
        if not (user_roles.get('admin') or user_roles.get('master') or 
                client.created_by == request.user or 
                client.branch == request.user.userprofile.branch):
            messages.error(request, "You don't have permission to view this client.")
            return redirect('client_list')
        
        # Get client loans
        loans = LoanApplication.objects.filter(client=client).order_by('-created_at')
        
        context = {
            'user_roles': user_roles,
            'client': client,
            'loans': loans,
            'page_title': f'Client: {client.full_name}',
            'breadcrumb': [
                {'name': 'Home', 'url': '/'},
                {'name': 'SML Project', 'url': '#'},
                {'name': 'Clients', 'url': '#'},
                {'name': client.full_name, 'url': '#'}
            ]
        }
        
        return render(request, 'sml_client_detail.html', context)
        
    except Exception as e:
        logger.error(f"Error in client detail: {str(e)}")
        messages.error(request, f"Error loading client: {str(e)}")
        return redirect('client_list')

@login_required
def kyc_upload(request, client_id):
    """Upload KYC documents"""
    try:
        user_roles = role_flags(request.user)
        client = get_object_or_404(Client, id=client_id)
        
        if request.method == 'POST':
            # Handle KYC document upload
            document_type = request.POST.get('document_type')
            document_file = request.FILES.get('document_file')
            document_number = request.POST.get('document_number')
            
            if document_file and document_type:
                # Create KYC document record
                kyc_doc = KYCDocument.objects.create(
                    client=client,
                    document_type=document_type,
                    document_number=document_number,
                    document_file=document_file,
                    uploaded_by=request.user,
                    status='pending'
                )
                
                messages.success(request, 'KYC document uploaded successfully!')
                return redirect('client_detail', client_id=client.id)
            else:
                messages.error(request, 'Please provide document type and file.')
        
        context = {
            'user_roles': user_roles,
            'client': client,
            'page_title': f'Upload KYC - {client.full_name}'
        }
        
        return render(request, 'sml_kyc_upload.html', context)
        
    except Exception as e:
        logger.error(f"Error in KYC upload: {str(e)}")
        messages.error(request, f"Error uploading KYC: {str(e)}")
        return redirect('client_detail', client_id=client_id)

# ========================================
# FIELD OPERATIONS SYSTEM VIEWS
# ========================================

@login_required
def field_schedule_list(request):
    """List field schedules"""
    try:
        user_roles = role_flags(request.user)
        
        # Get field schedules based on user permissions
        if user_roles.get('admin') or user_roles.get('master'):
            schedules = FieldSchedule.objects.all().order_by('-scheduled_date')
        elif user_roles.get('manager'):
            schedules = FieldSchedule.objects.filter(branch=request.user.userprofile.branch).order_by('-scheduled_date')
        else:
            schedules = FieldSchedule.objects.filter(assigned_to=request.user).order_by('-scheduled_date')
        
        # Pagination
        paginator = Paginator(schedules, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'user_roles': user_roles,
            'schedules': page_obj,
            'page_title': 'Field Schedules',
            'breadcrumb': [
                {'name': 'Home', 'url': '/'},
                {'name': 'SML Project', 'url': '#'},
                {'name': 'Field Operations', 'url': '#'},
                {'name': 'Schedules', 'url': '#'}
            ]
        }
        
        return render(request, 'sml_field_schedule_list.html', context)
        
    except Exception as e:
        logger.error(f"Error in field schedule list: {str(e)}")
        messages.error(request, f"Error loading field schedules: {str(e)}")
        return redirect('/')

@login_required
def field_visit_complete(request, visit_id):
    """Complete field visit"""
    try:
        user_roles = role_flags(request.user)
        visit = get_object_or_404(FieldVisit, id=visit_id)
        
        # Check permissions
        if not (user_roles.get('admin') or user_roles.get('master') or 
                visit.assigned_to == request.user):
            messages.error(request, "You don't have permission to complete this visit.")
            return redirect('field_schedule_list')
        
        if request.method == 'POST':
            with transaction.atomic():
                visit.status = 'completed'
                visit.completed_at = timezone.now()
                visit.visit_notes = request.POST.get('visit_notes', '')
                visit.save()
                
                messages.success(request, 'Field visit marked as completed!')
                return redirect('field_schedule_list')
        
        context = {
            'user_roles': user_roles,
            'visit': visit,
            'page_title': f'Complete Field Visit'
        }
        
        return render(request, 'sml_field_visit_complete.html', context)
        
    except Exception as e:
        logger.error(f"Error in field visit complete: {str(e)}")
        messages.error(request, f"Error completing field visit: {str(e)}")
        return redirect('field_schedule_list')

# ========================================
# NPA MANAGEMENT SYSTEM VIEWS
# ========================================

@login_required
def npa_list(request):
    """List NPA accounts"""
    try:
        user_roles = role_flags(request.user)
        
        # Get NPA accounts based on user permissions
        if user_roles.get('admin') or user_roles.get('master'):
            npa_accounts = NPAAccount.objects.all().order_by('-days_overdue')
        elif user_roles.get('manager'):
            npa_accounts = NPAAccount.objects.filter(branch=request.user.userprofile.branch).order_by('-days_overdue')
        else:
            npa_accounts = NPAAccount.objects.filter(assigned_to=request.user).order_by('-days_overdue')
        
        # Pagination
        paginator = Paginator(npa_accounts, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'user_roles': user_roles,
            'npa_accounts': page_obj,
            'page_title': 'NPA Accounts',
            'breadcrumb': [
                {'name': 'Home', 'url': '/'},
                {'name': 'SML Project', 'url': '#'},
                {'name': 'NPA Management', 'url': '#'}
            ]
        }
        
        return render(request, 'sml_npa_list.html', context)
        
    except Exception as e:
        logger.error(f"Error in NPA list: {str(e)}")
        messages.error(request, f"Error loading NPA accounts: {str(e)}")
        return redirect('/')

@login_required
def npa_analysis(request):
    """NPA Analysis Dashboard"""
    try:
        user_roles = role_flags(request.user)
        
        # Get NPA analysis data
        npa_data = get_npa_analysis_data(request.user)
        
        context = {
            'user_roles': user_roles,
            'npa_data': npa_data,
            'page_title': 'NPA Analysis',
            'breadcrumb': [
                {'name': 'Home', 'url': '/'},
                {'name': 'SML Project', 'url': '#'},
                {'name': 'NPA Management', 'url': '#'},
                {'name': 'Analysis', 'url': '#'}
            ]
        }
        
        return render(request, 'sml_npa_analysis.html', context)
        
    except Exception as e:
        logger.error(f"Error in NPA analysis: {str(e)}")
        messages.error(request, f"Error loading NPA analysis: {str(e)}")
        return redirect('npa_list')

# ========================================
# CREDIT BUREAU INTEGRATION VIEWS
# ========================================

@login_required
def credit_bureau_dashboard(request):
    """Credit Bureau Dashboard"""
    try:
        user_roles = role_flags(request.user)
        
        # Get credit bureau data
        credit_data = get_credit_bureau_data(request.user)
        
        context = {
            'user_roles': user_roles,
            'credit_data': credit_data,
            'page_title': 'Credit Bureau',
            'breadcrumb': [
                {'name': 'Home', 'url': '/'},
                {'name': 'SML Project', 'url': '#'},
                {'name': 'Credit Bureau', 'url': '#'}
            ]
        }
        
        return render(request, 'sml_credit_bureau.html', context)
        
    except Exception as e:
        logger.error(f"Error in credit bureau dashboard: {str(e)}")
        messages.error(request, f"Error loading credit bureau: {str(e)}")
        return redirect('/')

@login_required
def credit_bureau_pull_report(request):
    """Pull credit report from bureau"""
    try:
        user_roles = role_flags(request.user)
        
        if request.method == 'POST':
            client_id = request.POST.get('client_id')
            client = get_object_or_404(Client, id=client_id)
            
            # Simulate credit bureau API call
            credit_report = pull_credit_report_from_bureau(client)
            
            if credit_report:
                messages.success(request, 'Credit report pulled successfully!')
                return JsonResponse({'success': True, 'report': credit_report})
            else:
                messages.error(request, 'Failed to pull credit report.')
                return JsonResponse({'success': False, 'error': 'Failed to pull report'})
        
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
        
    except Exception as e:
        logger.error(f"Error in credit bureau pull report: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)})

# ========================================
# FINANCIAL REPORTS SYSTEM VIEWS
# ========================================

@login_required
def financial_reports_list(request):
    """List financial reports"""
    try:
        user_roles = role_flags(request.user)
        
        context = {
            'user_roles': user_roles,
            'page_title': 'Financial Reports',
            'breadcrumb': [
                {'name': 'Home', 'url': '/'},
                {'name': 'SML Project', 'url': '#'},
                {'name': 'Financial Reports', 'url': '#'}
            ]
        }
        
        return render(request, 'sml_financial_reports.html', context)
        
    except Exception as e:
        logger.error(f"Error in financial reports: {str(e)}")
        messages.error(request, f"Error loading financial reports: {str(e)}")
        return redirect('/')

@login_required
def portfolio_report(request):
    """Portfolio Report"""
    try:
        user_roles = role_flags(request.user)
        
        # Get portfolio data
        portfolio_data = get_portfolio_report_data(request.user)
        
        context = {
            'user_roles': user_roles,
            'portfolio_data': portfolio_data,
            'page_title': 'Portfolio Report',
            'breadcrumb': [
                {'name': 'Home', 'url': '/'},
                {'name': 'SML Project', 'url': '#'},
                {'name': 'Financial Reports', 'url': '#'},
                {'name': 'Portfolio', 'url': '#'}
            ]
        }
        
        return render(request, 'sml_portfolio_report.html', context)
        
    except Exception as e:
        logger.error(f"Error in portfolio report: {str(e)}")
        messages.error(request, f"Error loading portfolio report: {str(e)}")
        return redirect('financial_reports_list')

# ========================================
# AI ANALYTICS SYSTEM VIEWS
# ========================================

@login_required
def ai_analytics_dashboard(request):
    """AI Analytics Dashboard"""
    try:
        user_roles = role_flags(request.user)
        
        # Get AI analytics data
        ai_data = get_ai_analytics_data(request.user)
        
        context = {
            'user_roles': user_roles,
            'ai_data': ai_data,
            'page_title': 'AI Analytics',
            'breadcrumb': [
                {'name': 'Home', 'url': '/'},
                {'name': 'SML Project', 'url': '#'},
                {'name': 'AI Analytics', 'url': '#'}
            ]
        }
        
        return render(request, 'sml_ai_analytics.html', context)
        
    except Exception as e:
        logger.error(f"Error in AI analytics: {str(e)}")
        messages.error(request, f"Error loading AI analytics: {str(e)}")
        return redirect('/')

# ========================================
# API ENDPOINTS FOR SML PROJECT
# ========================================

@login_required
def api_loan_list(request):
    """API endpoint for loan list"""
    try:
        user_roles = role_flags(request.user)
        
        # Get loans based on user permissions
        if user_roles.get('admin') or user_roles.get('master'):
            loans = LoanApplication.objects.all()
        elif user_roles.get('manager'):
            loans = LoanApplication.objects.filter(branch=request.user.userprofile.branch)
        else:
            loans = LoanApplication.objects.filter(created_by=request.user)
        
        # Serialize loans
        loans_data = []
        for loan in loans:
            loans_data.append({
                'id': loan.id,
                'application_id': loan.application_id,
                'client_name': loan.client.full_name if loan.client else 'N/A',
                'loan_amount': str(loan.loan_amount),
                'status': loan.status,
                'created_at': loan.created_at.isoformat() if loan.created_at else None
            })
        
        return JsonResponse({'success': True, 'loans': loans_data})
        
    except Exception as e:
        logger.error(f"Error in API loan list: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def api_client_list(request):
    """API endpoint for client list"""
    try:
        user_roles = role_flags(request.user)
        
        # Get clients based on user permissions
        if user_roles.get('admin') or user_roles.get('master'):
            clients = Client.objects.all()
        elif user_roles.get('manager'):
            clients = Client.objects.filter(branch=request.user.userprofile.branch)
        else:
            clients = Client.objects.filter(created_by=request.user)
        
        # Serialize clients
        clients_data = []
        for client in clients:
            clients_data.append({
                'id': client.id,
                'full_name': client.full_name,
                'aadhaar_number': client.aadhaar_number,
                'contact_number': client.contact_number,
                'status': client.status,
                'created_at': client.created_at.isoformat() if client.created_at else None
            })
        
        return JsonResponse({'success': True, 'clients': clients_data})
        
    except Exception as e:
        logger.error(f"Error in API client list: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)})

# ========================================
# SML PROJECT UTILITY VIEWS
# ========================================

@login_required
def calculate_emi(request):
    """Calculate EMI for loan"""
    try:
        if request.method == 'POST':
            loan_amount = float(request.POST.get('loan_amount', 0))
            interest_rate = float(request.POST.get('interest_rate', 0))
            tenure_months = int(request.POST.get('tenure_months', 0))
            
            if loan_amount > 0 and interest_rate > 0 and tenure_months > 0:
                # Calculate EMI
                monthly_rate = interest_rate / (12 * 100)
                emi = loan_amount * monthly_rate * (1 + monthly_rate) ** tenure_months / ((1 + monthly_rate) ** tenure_months - 1)
                
                return JsonResponse({
                    'success': True,
                    'emi': round(emi, 2),
                    'total_amount': round(emi * tenure_months, 2),
                    'total_interest': round(emi * tenure_months - loan_amount, 2)
                })
            else:
                return JsonResponse({'success': False, 'error': 'Invalid input parameters'})
        
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
        
    except Exception as e:
        logger.error(f"Error in EMI calculation: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def credit_score_calculator(request):
    """Calculate credit score"""
    try:
        if request.method == 'POST':
            # Get client data
            income = float(request.POST.get('income', 0))
            employment_years = float(request.POST.get('employment_years', 0))
            credit_history_years = float(request.POST.get('credit_history_years', 0))
            existing_loans = int(request.POST.get('existing_loans', 0))
            
            # Calculate credit score (simplified algorithm)
            score = 500  # Base score
            
            if income > 50000:
                score += 100
            if employment_years > 2:
                score += 50
            if credit_history_years > 3:
                score += 75
            if existing_loans < 2:
                score += 50
            
            score = min(score, 900)  # Cap at 900
            
            # Determine risk level
            if score > 700:
                risk_level = 'Low'
            elif score > 500:
                risk_level = 'Medium'
            else:
                risk_level = 'High'
            
            return JsonResponse({
                'success': True,
                'credit_score': score,
                'risk_level': risk_level,
                'recommendations': get_credit_recommendations(score)
            })
        
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
        
    except Exception as e:
        logger.error(f"Error in credit score calculation: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)})

# ========================================
# SML PROJECT SETTINGS VIEWS
# ========================================

@login_required
def sml_settings(request):
    """SML Project Settings"""
    try:
        user_roles = role_flags(request.user)
        
        # Only admin and master can access settings
        if not (user_roles.get('admin') or user_roles.get('master')):
            messages.error(request, "You don't have permission to access settings.")
            return redirect('/')
        
        context = {
            'user_roles': user_roles,
            'page_title': 'SML Project Settings',
            'breadcrumb': [
                {'name': 'Home', 'url': '/'},
                {'name': 'SML Project', 'url': '#'},
                {'name': 'Settings', 'url': '#'}
            ]
        }
        
        return render(request, 'sml_settings.html', context)
        
    except Exception as e:
        logger.error(f"Error in SML settings: {str(e)}")
        messages.error(request, f"Error loading settings: {str(e)}")
        return redirect('/')

# ========================================
# HELPER FUNCTIONS
# ========================================

def get_sml_dashboard_data(user):
    """Get dashboard data for SML Project"""
    try:
        # Get user branch
        branch = user.userprofile.branch if hasattr(user, 'userprofile') else None
        
        # Portfolio data
        portfolio_data = {
            'total_portfolio': 0,
            'active_clients': 0,
            'npa_amount': 0,
            'collection_efficiency': 0
        }
        
        # Calculate portfolio metrics
        if branch:
            loans = LoanApplication.objects.filter(branch=branch, status='approved')
            portfolio_data['total_portfolio'] = sum(loan.loan_amount for loan in loans)
            portfolio_data['active_clients'] = Client.objects.filter(branch=branch, status='active').count()
            
            # Calculate NPA
            overdue_loans = loans.filter(status='overdue')
            portfolio_data['npa_amount'] = sum(loan.loan_amount for loan in overdue_loans)
            
            # Calculate collection efficiency
            total_collection = sum(loan.loan_amount for loan in loans if loan.status == 'closed')
            if portfolio_data['total_portfolio'] > 0:
                portfolio_data['collection_efficiency'] = (total_collection / portfolio_data['total_portfolio']) * 100
        
        return portfolio_data
        
    except Exception as e:
        logger.error(f"Error getting dashboard data: {str(e)}")
        return {}

def create_loan_schedule(loan):
    """Create loan repayment schedule"""
    try:
        # Calculate EMI
        monthly_rate = loan.interest_rate / (12 * 100)
        emi = loan.loan_amount * monthly_rate * (1 + monthly_rate) ** loan.tenure / ((1 + monthly_rate) ** loan.tenure - 1)
        
        # Create schedule entries
        for month in range(1, loan.tenure + 1):
            LoanSchedule.objects.create(
                loan=loan,
                installment_number=month,
                due_date=loan.disbursement_date + timezone.timedelta(days=30*month),
                emi_amount=emi,
                status='pending'
            )
        
    except Exception as e:
        logger.error(f"Error creating loan schedule: {str(e)}")

def create_disbursement_record(loan):
    """Create disbursement record"""
    try:
        DisbursementRecord.objects.create(
            loan=loan,
            disbursement_amount=loan.loan_amount,
            disbursement_date=timezone.now(),
            disbursed_by=loan.approved_by
        )
    except Exception as e:
        logger.error(f"Error creating disbursement record: {str(e)}")

def get_npa_analysis_data(user):
    """Get NPA analysis data"""
    try:
        branch = user.userprofile.branch if hasattr(user, 'userprofile') else None
        
        npa_data = {
            'total_npa': 0,
            'npa_by_age': {},
            'npa_by_amount': {},
            'recovery_strategies': []
        }
        
        if branch:
            # Get NPA accounts
            npa_accounts = NPAAccount.objects.filter(branch=branch)
            npa_data['total_npa'] = sum(account.overdue_amount for account in npa_accounts)
            
            # Group by age
            for account in npa_accounts:
                age_group = get_age_group(account.days_overdue)
                if age_group not in npa_data['npa_by_age']:
                    npa_data['npa_by_age'][age_group] = 0
                npa_data['npa_by_age'][age_group] += account.overdue_amount
        
        return npa_data
        
    except Exception as e:
        logger.error(f"Error getting NPA analysis data: {str(e)}")
        return {}

def get_credit_bureau_data(user):
    """Get credit bureau data"""
    try:
        branch = user.userprofile.branch if hasattr(user, 'userprofile') else None
        
        credit_data = {
            'total_reports': 0,
            'average_score': 0,
            'score_distribution': {},
            'recent_pulls': []
        }
        
        if branch:
            # Get credit reports
            credit_reports = CreditReport.objects.filter(branch=branch)
            credit_data['total_reports'] = credit_reports.count()
            
            if credit_data['total_reports'] > 0:
                credit_data['average_score'] = sum(report.credit_score for report in credit_reports) / credit_data['total_reports']
        
        return credit_data
        
    except Exception as e:
        logger.error(f"Error getting credit bureau data: {str(e)}")
        return {}

def get_portfolio_report_data(user):
    """Get portfolio report data"""
    try:
        branch = user.userprofile.branch if hasattr(user, 'userprofile') else None
        
        portfolio_data = {
            'total_disbursed': 0,
            'total_collected': 0,
            'outstanding_amount': 0,
            'monthly_trends': {}
        }
        
        if branch:
            # Get loan data
            loans = LoanApplication.objects.filter(branch=branch, status='approved')
            portfolio_data['total_disbursed'] = sum(loan.loan_amount for loan in loans)
            
            # Calculate collections
            collections = LoanCollection.objects.filter(loan__branch=branch)
            portfolio_data['total_collected'] = sum(collection.amount for collection in collections)
            portfolio_data['outstanding_amount'] = portfolio_data['total_disbursed'] - portfolio_data['total_collected']
        
        return portfolio_data
        
    except Exception as e:
        logger.error(f"Error getting portfolio report data: {str(e)}")
        return {}

def get_ai_analytics_data(user):
    """Get AI analytics data"""
    try:
        ai_data = {
            'credit_risk_insights': [],
            'portfolio_optimization': [],
            'collection_strategies': [],
            'risk_alerts': []
        }
        
        # Generate AI insights (simplified)
        ai_data['credit_risk_insights'].append({
            'insight': 'Clients with credit scores above 750 show 23% lower default rates',
            'confidence': 87,
            'action': 'Consider higher loan amounts for high-credit clients'
        })
        
        ai_data['portfolio_optimization'].append({
            'insight': 'Agriculture loans in monsoon season show 15% higher repayment rates',
            'confidence': 78,
            'action': 'Increase agriculture loan disbursement during monsoon'
        })
        
        ai_data['collection_strategies'].append({
            'insight': 'Morning collection visits (9-11 AM) show 23% higher success rate',
            'confidence': 82,
            'action': 'Schedule more collection visits in morning hours'
        })
        
        return ai_data
        
    except Exception as e:
        logger.error(f"Error getting AI analytics data: {str(e)}")
        return {}

def pull_credit_report_from_bureau(client):
    """Pull credit report from credit bureau (simulated)"""
    try:
        # Simulate credit bureau API call
        import random
        
        credit_report = {
            'client_id': client.id,
            'credit_score': random.randint(300, 900),
            'payment_history': random.randint(70, 100),
            'credit_utilization': random.randint(10, 80),
            'credit_history_length': random.randint(1, 10),
            'recent_inquiries': random.randint(0, 5),
            'pulled_at': timezone.now().isoformat()
        }
        
        # Save credit report
        CreditReport.objects.create(
            client=client,
            credit_score=credit_report['credit_score'],
            payment_history=credit_report['payment_history'],
            credit_utilization=credit_report['credit_utilization'],
            credit_history_length=credit_report['credit_history_length'],
            recent_inquiries=credit_report['recent_inquiries'],
            report_data=json.dumps(credit_report)
        )
        
        return credit_report
        
    except Exception as e:
        logger.error(f"Error pulling credit report: {str(e)}")
        return None

def get_age_group(days_overdue):
    """Get age group for NPA classification"""
    if days_overdue <= 30:
        return '0-30 days'
    elif days_overdue <= 60:
        return '31-60 days'
    elif days_overdue <= 90:
        return '61-90 days'
    else:
        return '90+ days'

def get_credit_recommendations(credit_score):
    """Get credit recommendations based on score"""
    if credit_score > 700:
        return ['Approve loan with standard terms', 'Consider higher loan amount']
    elif credit_score > 500:
        return ['Approve with additional collateral', 'Reduce loan amount', 'Higher interest rate']
    else:
        return ['Require additional collateral', 'Consider co-signer', 'Strict monitoring required']


