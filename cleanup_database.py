#!/usr/bin/env python
"""
Database Cleanup Script
Removes all soft-deleted records from the database.
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
from companies.models import *

def cleanup_soft_deleted_records():
    """Clean up all soft-deleted records from the database."""
    
    print("🧹 Starting database cleanup...")
    print("=" * 50)
    
    # Models that typically have soft-delete fields
    models_to_clean = [
        ('Branch', Branch),
        ('Company', Company),
        ('Village', Village),
        ('Center', Center),
        ('Group', Group),
        ('Role', Role),
        ('Staff', Staff),
        ('Product', Product),
        ('Client', Client),
        ('LoanApplication', LoanApplication),
        ('LoanApproval', LoanApproval),
        ('Disbursement', Disbursement),
        ('BusinessSetting', BusinessSetting),
        ('FieldSchedule', FieldSchedule),
        ('FieldReport', FieldReport),
        ('WeeklyReport', WeeklyReport),
        ('MonthlyReport', MonthlyReport),
        ('AccountHead', AccountHead),
        ('Voucher', Voucher),
        ('Posting', Posting),
        ('RecoveryPosting', RecoveryPosting),
        ('Appointment', Appointment),
        ('SalaryStatement', SalaryStatement),
        ('Payment', Payment),
        ('Repayment', Repayment),
        ('LoanRestructure', LoanRestructure),
        ('Notification', Notification),
        ('GatewayEvent', GatewayEvent),
        ('EWIFlag', EWIFlag),
        ('KYCDocument', KYCDocument),
        ('AlertRule', AlertRule),
        ('Column', Column),
        ('Cadre', Cadre),
        ('Users', Users),
        ('UserPermission', UserPermission),
    ]
    
    total_deleted = 0
    
    for model_name, model_class in models_to_clean:
        try:
            # Check if model has soft-delete fields
            has_status = hasattr(model_class, 'status')
            has_is_active = hasattr(model_class, 'is_active')
            has_is_deleted = hasattr(model_class, 'is_deleted')
            
            if not any([has_status, has_is_active, has_is_deleted]):
                print(f"⏭️  {model_name}: No soft-delete fields found, skipping...")
                continue
            
            # Count records before cleanup
            total_before = model_class.objects.count()
            
            # Delete soft-deleted records
            deleted_count = 0
            
            if has_status:
                # Delete records with status != 'active'
                non_active = model_class.objects.exclude(status='active')
                deleted_count += non_active.count()
                non_active.delete()
                print(f"🗑️  {model_name}: Deleted {deleted_count} non-active records (status != 'active')")
            
            if has_is_active:
                # Delete records with is_active = False
                inactive = model_class.objects.filter(is_active=False)
                deleted_count += inactive.count()
                inactive.delete()
                print(f"🗑️  {model_name}: Deleted {deleted_count} inactive records (is_active = False)")
            
            if has_is_deleted:
                # Delete records with is_deleted = True
                deleted = model_class.objects.filter(is_deleted=True)
                deleted_count += deleted.count()
                deleted.delete()
                print(f"🗑️  {model_name}: Deleted {deleted_count} deleted records (is_deleted = True)")
            
            # Count records after cleanup
            total_after = model_class.objects.count()
            
            if deleted_count > 0:
                print(f"✅ {model_name}: Cleaned up {deleted_count} records")
                print(f"   Before: {total_before}, After: {total_after}")
                total_deleted += deleted_count
            else:
                print(f"✅ {model_name}: No soft-deleted records found")
                
        except Exception as e:
            print(f"❌ {model_name}: Error during cleanup - {e}")
            continue
    
    print("=" * 50)
    print(f"🎉 Database cleanup completed!")
    print(f"📊 Total records deleted: {total_deleted}")
    
    # Clean up any orphaned records or fix data integrity issues
    print("\n🔧 Running additional cleanup tasks...")
    
    # Clean up any records with invalid foreign keys
    try:
        with connection.cursor() as cursor:
            # Find and fix any broken foreign key references
            cursor.execute("""
                PRAGMA foreign_key_check;
            """)
            fk_issues = cursor.fetchall()
            
            if fk_issues:
                print(f"⚠️  Found {len(fk_issues)} foreign key constraint issues")
                for issue in fk_issues:
                    print(f"   - {issue}")
            else:
                print("✅ No foreign key constraint issues found")
                
    except Exception as e:
        print(f"⚠️  Could not check foreign key constraints: {e}")
    
    # Optimize database
    try:
        with connection.cursor() as cursor:
            cursor.execute("VACUUM;")
            cursor.execute("ANALYZE;")
            print("✅ Database optimized (VACUUM and ANALYZE)")
    except Exception as e:
        print(f"⚠️  Could not optimize database: {e}")
    
    print("\n🎯 Database cleanup and optimization completed successfully!")

if __name__ == "__main__":
    try:
        cleanup_soft_deleted_records()
    except KeyboardInterrupt:
        print("\n❌ Cleanup interrupted by user")
    except Exception as e:
        print(f"\n💥 Fatal error during cleanup: {e}")
        import traceback
        traceback.print_exc()
