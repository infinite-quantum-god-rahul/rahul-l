#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from django.contrib.auth.models import User

# Fix the user
try:
    user = User.objects.get(username='sml123')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"✅ Fixed: User {user.username} is now superuser: {user.is_superuser}")
    print(f"✅ User {user.username} is now staff: {user.is_staff}")
    
    # Verify the fix
    user.refresh_from_db()
    print(f"✅ Verification: User {user.username} is superuser: {user.is_superuser}")
    
except User.DoesNotExist:
    print("❌ User sml123 not found")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
