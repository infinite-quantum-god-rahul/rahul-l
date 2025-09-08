#!/usr/bin/env python3
"""
Test script to verify that the form fixes are working correctly.
This script tests the fix_required_attributes function and related fixes.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from companies.forms import BranchForm, fix_required_attributes
from companies.models import Branch

def test_fix_required_attributes():
    """Test the fix_required_attributes function."""
    print("🧪 Testing fix_required_attributes function...")
    
    # Create a test form
    form = BranchForm()
    
    # Check if the fix function exists
    if not hasattr(form, 'fields'):
        print("❌ Form has no fields attribute")
        return False
    
    print(f"✅ Form created with {len(form.fields)} fields")
    
    # Check each field for required attributes
    problematic_fields = []
    fixed_fields = []
    
    for field_name, field in form.fields.items():
        if getattr(field, 'required', False):
            print(f"📋 Field '{field_name}' is required")
            
            # Check widget attributes
            if hasattr(field, 'widget') and hasattr(field.widget, 'attrs'):
                required_attr = field.widget.attrs.get('required')
                data_required_attr = field.widget.attrs.get('data-required')
                
                print(f"  - Required attribute: {required_attr}")
                print(f"  - Data required attribute: {data_required_attr}")
                
                if required_attr == 'True':
                    print(f"  ❌ PROBLEM: required=True (Python boolean)")
                    problematic_fields.append(field_name)
                elif required_attr == 'required':
                    print(f"  ✅ GOOD: required='required' (string)")
                    fixed_fields.append(field_name)
                else:
                    print(f"  ⚠️ UNKNOWN: required='{required_attr}'")
                    problematic_fields.append(field_name)
            else:
                print(f"  ❌ PROBLEM: No widget attributes")
                problematic_fields.append(field_name)
    
    print(f"\n📊 Results:")
    print(f"  - Total required fields: {len([f for f in form.fields.values() if getattr(f, 'required', False)])}")
    print(f"  - Fixed fields: {len(fixed_fields)}")
    print(f"  - Problematic fields: {len(problematic_fields)}")
    
    if problematic_fields:
        print(f"  ❌ Problematic fields: {', '.join(problematic_fields)}")
        return False
    else:
        print(f"  ✅ All required fields are properly fixed!")
        return True

def test_form_rendering():
    """Test form rendering to see if the fixes are applied."""
    print("\n🧪 Testing form rendering...")
    
    # Create a test form
    form = BranchForm()
    
    # Try to render the form as HTML
    try:
        html = form.as_p()
        print(f"✅ Form rendered successfully")
        print(f"📋 HTML length: {len(html)} characters")
        
        # Check for problematic patterns in the HTML
        if 'required=True' in html:
            print(f"❌ PROBLEM: Found 'required=True' in HTML")
            return False
        elif 'required="required"' in html:
            print(f"✅ GOOD: Found 'required=\"required\"' in HTML")
            return True
        else:
            print(f"⚠️ WARNING: No required attributes found in HTML")
            return False
            
    except Exception as e:
        print(f"❌ Error rendering form: {e}")
        return False

def test_template_filters():
    """Test if the template filters are working."""
    print("\n🧪 Testing template filters...")
    
    try:
        from django.template import Template, Context
        from companies.templatetags.custom_tags import fix_required_attributes
        
        # Test the template filter directly
        form = BranchForm()
        field = form['code']  # Get a required field
        
        # Apply the filter
        fixed_field = fix_required_attributes(field)
        
        if fixed_field != field:
            print(f"✅ Template filter applied successfully")
            
            # Check if the attributes were fixed
            if hasattr(fixed_field.field.widget, 'attrs'):
                required_attr = fixed_field.field.widget.attrs.get('required')
                if required_attr == 'required':
                    print(f"✅ Required attribute fixed to 'required'")
                    return True
                else:
                    print(f"❌ Required attribute not fixed: {required_attr}")
                    return False
            else:
                print(f"❌ No widget attributes found")
                return False
        else:
            print(f"⚠️ Template filter returned unchanged field")
            return False
            
    except Exception as e:
        print(f"❌ Error testing template filters: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Form Fixes Test Suite")
    print("=" * 50)
    
    tests = [
        ("fix_required_attributes function", test_fix_required_attributes),
        ("form rendering", test_form_rendering),
        ("template filters", test_template_filters),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running test: {test_name}")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The form fixes should work correctly.")
        return True
    else:
        print("🚨 Some tests failed. The form fixes may not work correctly.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
