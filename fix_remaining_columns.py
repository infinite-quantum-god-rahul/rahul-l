#!/usr/bin/env python
"""
Fix Remaining Missing Database Columns Script
Adds the remaining missing columns that were identified.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from django.db import connection

def fix_remaining_columns():
    """Fix the remaining missing database columns."""
    
    print("🔧 Fixing remaining missing columns...")
    print("=" * 50)
    
    # Define the remaining missing columns
    remaining_columns = [
        # FieldSchedule table - fieldreport field
        {
            'table': 'companies_fieldschedule',
            'column': 'fieldreport',
            'type': 'INTEGER',
            'nullable': True,
            'description': 'Field report foreign key'
        },
        # FieldReport table - schedule field
        {
            'table': 'companies_fieldreport',
            'column': 'schedule',
            'type': 'INTEGER',
            'nullable': True,
            'description': 'Schedule foreign key'
        },
        # Users table - staff field
        {
            'table': 'companies_users',
            'column': 'staff',
            'type': 'INTEGER',
            'nullable': True,
            'description': 'Staff foreign key'
        },
        # UserPermission table - user_profile field
        {
            'table': 'companies_userpermission',
            'column': 'user_profile',
            'type': 'INTEGER',
            'nullable': True,
            'description': 'User profile foreign key'
        },
    ]
    
    total_fixed = 0
    
    for column_info in remaining_columns:
        table_name = column_info['table']
        column_name = column_info['column']
        column_type = column_info['type']
        nullable = column_info['nullable']
        description = column_info['description']
        
        try:
            # Check if column already exists
            with connection.cursor() as cursor:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                
                if column_name in column_names:
                    print(f"✅ {table_name}.{column_name}: Column already exists, skipping...")
                    continue
                
                # Add the missing column
                null_constraint = "" if nullable else " NOT NULL"
                sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}{null_constraint}"
                
                print(f"🔧 Adding column {table_name}.{column_name}...")
                cursor.execute(sql)
                
                # Verify the column was added
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns_after = cursor.fetchall()
                column_names_after = [col[1] for col in columns_after]
                
                if column_name in column_names_after:
                    print(f"✅ {table_name}.{column_name}: Successfully added")
                    total_fixed += 1
                else:
                    print(f"❌ {table_name}.{column_name}: Failed to add column")
                    
        except Exception as e:
            print(f"❌ {table_name}.{column_name}: Error - {e}")
            continue
    
    print("=" * 50)
    print(f"🎉 Remaining column fixes completed!")
    print(f"📊 Total columns fixed: {total_fixed}")
    
    # Test if the FieldSchedule page now works
    print("\n🧪 Testing if FieldSchedule page now works...")
    try:
        from companies.models import FieldSchedule
        # Try to query the FieldSchedule model
        count = FieldSchedule.objects.count()
        print(f"✅ FieldSchedule query successful! Found {count} records")
    except Exception as e:
        print(f"❌ FieldSchedule still has issues: {e}")
    
    print("\n🎯 Remaining column fixes completed!")

if __name__ == "__main__":
    try:
        fix_remaining_columns()
    except KeyboardInterrupt:
        print("\n❌ Column fixes interrupted by user")
    except Exception as e:
        print(f"\n💥 Fatal error during column fixes: {e}")
        import traceback
        traceback.print_exc()
