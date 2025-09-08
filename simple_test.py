import os
import django

print("=== SIMPLE DJANGO TEST ===")

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
    django.setup()
    print("✓ Django setup successful")
    
    from django.urls import get_resolver
    resolver = get_resolver()
    print(f"✓ URL resolver loaded: {resolver.urlconf_name}")
    
    # Test a simple URL
    try:
        match = resolver.resolve('/test-simple/')
        print(f"✓ /test-simple/ resolves to: {match.func}")
    except Exception as e:
        print(f"✗ /test-simple/ failed: {e}")
    
    # Test the problematic URL
    try:
        match = resolver.resolve('/main-test/')
        print(f"✓ /main-test/ resolves to: {match.func}")
    except Exception as e:
        print(f"✗ /main-test/ failed: {e}")
        
except Exception as e:
    print(f"✗ Django setup failed: {e}")








