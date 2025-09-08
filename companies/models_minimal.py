"""
SML777 Companies Models - Minimal Version
=========================================

Minimal models for deployment testing.
"""

from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    """Simple Company model for testing"""
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
