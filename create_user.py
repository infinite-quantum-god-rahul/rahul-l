#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser
username = 'jagadeesh'
email = 'jagadeesh@example.com'
password = 'jaga1234'

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f"User '{username}' already exists!")
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"Updated password for user '{username}'")
else:
    # Create new superuser
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_staff=True,
        is_superuser=True
    )
    print(f"Created superuser '{username}' with password '{password}'")

print("Login credentials:")
print(f"Username: {username}")
print(f"Password: {password}")







