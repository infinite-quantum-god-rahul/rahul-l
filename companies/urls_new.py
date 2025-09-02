from django.urls import path
from django.http import HttpResponse
from . import views

# COMPLETELY NEW URL FILE FOR TESTING
urlpatterns = [
    path("SUPER-TEST-123/", lambda request: HttpResponse("SUPER TEST WORKS!"), name="super_test"),
    path("new-test/", lambda request: HttpResponse("NEW TEST WORKS!"), name="new_test"),
    path("test-simple/", lambda request: HttpResponse("SIMPLE TEST WORKS!"), name="simple_test"),
    path("emergency-test/", views.basic_test_view, name="emergency_test"),
    path("", views.home_view, name="home"),
]
