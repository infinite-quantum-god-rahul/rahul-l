"""
SML777 Companies Admin - Minimal Version
========================================

Minimal admin configuration for deployment testing.
"""

from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Simple admin for Company model"""
    list_display = ['name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']


