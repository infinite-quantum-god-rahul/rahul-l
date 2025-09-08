#!/usr/bin/env python
"""
Fix Missing Database Columns Script
Adds all missing columns that are causing OperationalError issues.
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
from django.db import migrations, models
from django.db.migrations.operations import AddField

def fix_missing_columns():
    """Fix all missing database columns that are causing errors."""
    
    print("🔧 Starting database column fixes...")
    print("=" * 50)
    
    # Define all missing columns that need to be added
    missing_columns = [
        # FieldSchedule table
        {
            'table': 'companies_fieldschedule',
            'column': 'CenterCode',
            'type': 'VARCHAR(50)',
            'nullable': True,
            'description': 'Center code for field schedule'
        },
        # Group table
        {
            'table': 'companies_group',
            'column': 'CenterCode',
            'type': 'VARCHAR(50)',
            'nullable': True,
            'description': 'Center code for group'
        },
        # Client table
        {
            'table': 'companies_client',
            'column': 'GCode',
            'type': 'VARCHAR(50)',
            'nullable': True,
            'description': 'Group code for client'
        },
        # Add any other missing columns here
    ]
    
    total_fixed = 0
    
    for column_info in missing_columns:
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
    print(f"🎉 Column fixes completed!")
    print(f"📊 Total columns fixed: {total_fixed}")
    
    # Now let's also check for any other potential missing columns by examining the models
    print("\n🔍 Checking for other potential missing columns...")
    
    try:
        from companies.models import (
            Branch, Company, Village, Center, Group, Role, Staff,
            Product, Client, LoanApplication, FieldSchedule, FieldReport,
            WeeklyReport, MonthlyReport, AccountHead, Voucher, Posting,
            RecoveryPosting, Appointment, SalaryStatement, Payment,
            Repayment, LoanRestructure, Notification, GatewayEvent,
            EWIFlag, KYCDocument, AlertRule, Column, Cadre, Users, UserPermission
        )
        
        # Check all models for potential column mismatches
        models_to_check = [
            Branch, Company, Village, Center, Group, Role, Staff,
            Product, Client, LoanApplication, FieldSchedule, FieldReport,
            WeeklyReport, MonthlyReport, AccountHead, Voucher, Posting,
            RecoveryPosting, Appointment, SalaryStatement, Payment,
            Repayment, LoanRestructure, Notification, GatewayEvent,
            EWIFlag, KYCDocument, AlertRule, Column, Cadre, Users, UserPermission
        ]
        
        for model_class in models_to_check:
            try:
                model_name = model_class.__name__
                table_name = model_class._meta.db_table
                
                # Get model fields
                model_fields = model_class._meta.get_fields()
                field_names = [field.name for field in model_fields if hasattr(field, 'name')]
                
                # Check database table structure
                with connection.cursor() as cursor:
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    db_columns = cursor.fetchall()
                    db_column_names = [col[1] for col in db_columns]
                    
                    # Check for missing columns
                    missing_in_db = []
                    for field in model_fields:
                        if hasattr(field, 'db_column') and field.db_column:
                            if field.db_column not in db_column_names:
                                missing_in_db.append(field.db_column)
                        elif hasattr(field, 'name') and field.name not in db_column_names:
                            # Skip some Django internal fields
                            if field.name not in ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']:
                                missing_in_db.append(field.name)
                    
                    if missing_in_db:
                        print(f"⚠️  {model_name}: Missing columns in DB: {missing_in_db}")
                    else:
                        print(f"✅ {model_name}: All columns present")
                        
            except Exception as e:
                print(f"❌ {model_class.__name__}: Error checking columns - {e}")
                continue
                
    except Exception as e:
        print(f"⚠️  Could not check model columns: {e}")
    
    # Optimize database after changes
    print("\n🔧 Optimizing database...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("VACUUM;")
            cursor.execute("ANALYZE;")
            print("✅ Database optimized (VACUUM and ANALYZE)")
    except Exception as e:
        print(f"⚠️  Could not optimize database: {e}")
    
    print("\n🎯 Database column fixes and optimization completed successfully!")

if __name__ == "__main__":
    try:
        fix_missing_columns()
    except KeyboardInterrupt:
        print("\n❌ Column fixes interrupted by user")
    except Exception as e:
        print(f"\n💥 Fatal error during column fixes: {e}")
        import traceback
        traceback.print_exc()
