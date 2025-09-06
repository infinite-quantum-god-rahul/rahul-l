from django.urls import path
from django.http import HttpResponse
from . import views

# TEMPORARY TEST - REPLACE ALL URLS
urlpatterns = [
    path("test-simple/", lambda request: HttpResponse("SIMPLE TEST WORKS!"), name="simple_test"),
    path("emergency-test/",             views.basic_test_view, name="emergency_test"),
    path("test123456789/",              views.basic_test_view, name="basic_test"),
    path("__test__/",                   views.basic_test_view, name="basic_test"),
    path("basic-test/",                 views.basic_test_view, name="basic_test"),
    path("test/",                       views.simple_test_view, name="test"),
    path("userprofile-direct/",         views.emergency_userprofile_view, name="userprofile_direct"),
    path("emergency/userprofile/",      views.emergency_userprofile_view, name="emergency_userprofile"),
    path("direct-userprofile/",         views.emergency_userprofile_view, name="direct_userprofile"),
    path("create/userprofile/",         views.emergency_userprofile_view, name="create_userprofile"),
    path("add/userprofile/",            views.emergency_userprofile_view, name="add_userprofile"),
    path("new/userprofile/",            views.emergency_userprofile_view, name="new_userprofile"),
    # BULLETPROOF backup endpoints - NEVER fail
    path("bulletproof/userprofile/",    views.bulletproof_userprofile_view, name="bulletproof_userprofile"),
    path("nuclear/userprofile/",        views.nuclear_userprofile_view, name="nuclear_userprofile"),
    path("",                    views.home_view,       name="home"),
    path("login/",              views.login_view,      name="login"),
    path("logout/",             views.logout_view,     name="logout"),
    path("dashboard/",          views.dashboard_view,  name="dashboard"),
    path("switch-account/",     views.switch_account,  name="switch_account"),

    path("next_code/",                views.next_code_view,         name="next_code"),
    path("search/client/aadhar/",     views.search_aadhar,          name="search_aadhar"),
    path("search/aadhar/",            views.search_client_aadhar,   name="search_client_aadhar"),

    path("permission-group/",         views.permission_group,       name="permission_group"),
    path("user-permissions/",         views.entity_list, {"entity": "userpermission"}, name="user_permissions"),
    path("choices/<str:entity>/",     views.choices_api,            name="choices_api"),

    path("api/credit-bureau/pull/",       views.credit_bureau_pull,     name="credit_bureau_pull"),
    path("api/credit-bureau/pull-json/",  views.credit_bureau_pull_api, name="credit_bureau_pull_api"),
    path("api/portfolio-dashboard/",      views.portfolio_dashboard,    name="portfolio_dashboard"),
    path("npa/",                           views.npa_dashboard,          name="npa_dashboard"),
    path("api/borrower/login/request/",   views.borrower_login_request,  name="borrower_login_request"),
    path("api/borrower/login/verify/",    views.borrower_login_verify,   name="borrower_login_verify"),
    path("api/repay/record/",             views.repay_record,            name="repay_record"),
    path("api/loan/restructure/",         views.restructure_apply,       name="restructure_apply"),

    path("hrpm/",                      views.entity_list, {"entity": "staff"},            name="hrpm_home"),
    path("hrpm/staff/",                views.entity_list, {"entity": "staff"},            name="hrpm_staff"),
    path("hrpm/appointment/",          views.entity_list, {"entity": "appointment"},      name="hrpm_appointment"),
    path("hrpm/salary-statement/",     views.entity_list, {"entity": "salarystatement"},  name="hrpm_salary_statement"),

    # Users specific URLs - PERFECT ROUTING
    path("users/",               views.entity_list, {"entity": "Users"}, name="users_list"),
    path("users/get/",           views.entity_form, {"entity": "Users"}, name="users_get_form"),
    path("users/form/",          views.entity_form, {"entity": "Users"}, name="users_form"),
    path("users/create/",        views.entity_create, {"entity": "Users"}, name="users_create"),
    path("users/<int:pk>/",      views.entity_get, {"entity": "Users"}, name="users_detail"),
    path("users/<int:pk>/edit/", views.entity_update, {"entity": "Users"}, name="users_edit"),
    path("users/<int:pk>/delete/", views.entity_delete, {"entity": "Users"}, name="users_delete"),
    
    # explicit aliases mapped to generic handlers
    path("Users/get/",           views.entity_get,    {"entity": "Users"}, name="users_get"),
    path("Users/create/",        views.entity_create, {"entity": "Users"}, name="users_create"),

    # Custom Fields functionality is now integrated into entity_list view
    # No separate custom-fields URL needed
    
    # Generic entity patterns - MUST BE LAST to avoid catching specific URLs
    path("<str:entity>/form/",               views.entity_form,   name="entity_form"),
    path("<str:entity>/form/<int:pk>/",      views.entity_get,    name="entity_form_edit"),
    path("<str:entity>/get/",                views.entity_get,    name="entity_get_new"),
    path("<str:entity>/get/<int:pk>/",       views.entity_get,    name="entity_get"),
    path("<str:entity>/create/",             views.entity_create, name="entity_create"),
    path("<str:entity>/update/<int:pk>/",    views.entity_update, name="entity_update"),
    path("<str:entity>/delete/<int:pk>/",    views.entity_delete, name="entity_delete"),
    path("<str:entity>/debug/",              views.debug_grid_view, name="entity_debug"),
    path("<str:entity>/edit/<int:pk>/",      views.entity_update, name="entity_edit_dashboard"),

    path("<str:entity>/",                    views.entity_list,   name="entity_list"),
]
