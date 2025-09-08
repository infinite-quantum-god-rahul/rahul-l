#!/usr/bin/env python
"""
Fix Group Columns Script
Fixes the remaining "group" columns that failed due to SQL reserved keyword.
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

def fix_group_columns():
    """Fix the group columns that failed due to reserved keyword."""
    
    print("🔧 Fixing Group Columns (Reserved Keyword Issue)")
    print("=" * 50)
    
    # Define the group columns that failed
    group_columns = [
        {
            'table': 'companies_prepaid',
            'column': 'group',
            'type': 'INTEGER',
            'nullable': True,
            'description': 'Group foreign key'
        },
        {
            'table': 'companies_mortgage',
            'column': 'group',
            'type': 'INTEGER',
            'nullable': True,
            'description': 'Group foreign key'
        },
        {
            'table': 'companies_exsaving',
            'column': 'group',
            'type': 'INTEGER',
            'nullable': True,
            'description': 'Group foreign key'
        },
        {
            'table': 'companies_kycdocument',
            'column': 'group',
            'type': 'INTEGER',
            'nullable': True,
            'description': 'Group foreign key'
        },
        {
            'table': 'companies_ewiflag',
            'column': 'group',
            'type': 'INTEGER',
            'nullable': True,
            'description': 'Group foreign key'
        },
        {
            'table': 'companies_members',
            'column': 'group',
            'type': 'INTEGER',
            'nullable': True,
            'description': 'Group foreign key'
        },
        {
            'table': 'companies_memberskaikaluru',
            'column': 'group',
            'type': 'INTEGER',
            'nullable': True,
            'description': 'Group foreign key'
        },
    ]
    
    total_fixed = 0
    total_skipped = 0
    total_errors = 0
    
    for column_info in group_columns:
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
                    print(f"✅ {table_name}.{column_name}: Already exists, skipping...")
                    total_skipped += 1
                    continue
                
                # Add the missing column with proper escaping for reserved keywords
                null_constraint = "" if nullable else " NOT NULL"
                sql = f"ALTER TABLE {table_name} ADD COLUMN `{column_name}` {column_type}{null_constraint}"
                
                print(f"🔧 Adding {table_name}.`{column_name}` ({description})...")
                cursor.execute(sql)
                
                # Verify the column was added
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns_after = cursor.fetchall()
                column_names_after = [col[1] for col in columns_after]
                
                if column_name in column_names_after:
                    print(f"✅ {table_name}.`{column_name}`: Successfully added")
                    total_fixed += 1
                else:
                    print(f"❌ {table_name}.`{column_name}`: Failed to add column")
                    total_errors += 1
                    
        except Exception as e:
            print(f"❌ {table_name}.`{column_name}`: Error - {e}")
            total_errors += 1
            continue
    
    print("=" * 50)
    print(f"🎉 Group column fixes completed!")
    print(f"📊 Results:")
    print(f"   ✅ Columns fixed: {total_fixed}")
    print(f"   ⏭️  Columns skipped (already exist): {total_skipped}")
    print(f"   ❌ Errors: {total_errors}")
    
    # Final Django check
    print("\n🧪 Final Django check...")
    try:
        from django.core.management import execute_from_command_line
        import io
        import sys
        
        # Capture Django check output
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        try:
            execute_from_command_line(['manage.py', 'check', '--deploy'])
        except SystemExit:
            pass  # Django check exits with code 0 or 1
        
        output = buffer.getvalue()
        sys.stdout = old_stdout
        
        # Check for remaining column issues
        if "missing columns" in output:
            print("⚠️  Some columns may still be missing.")
            print("Output:", output)
        else:
            print("✅ All column issues resolved!")
            
    except Exception as e:
        print(f"❌ Error running Django check: {e}")
    
    print("\n🎯 Group column fixes completed!")
    return total_fixed, total_skipped, total_errors

if __name__ == "__main__":
    try:
        fix_group_columns()
    except KeyboardInterrupt:
        print("\n❌ Group column fixes interrupted by user")
    except Exception as e:
        print(f"\n💥 Fatal error during group column fixes: {e}")
        import traceback
        traceback.print_exc()
