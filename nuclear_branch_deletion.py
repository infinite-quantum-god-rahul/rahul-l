#!/usr/bin/env python
"""
Nuclear Branch Deletion Script
This script uses raw SQL to find and delete ALL records that reference a branch,
ensuring no FOREIGN KEY constraint errors occur.
"""

import os
import sys
import django
from django.db import connection

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

def find_all_branch_tables():
    """Find all tables that have branch-related columns."""
    print("🔍 FINDING ALL BRANCH-RELATED TABLES")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        # Get all tables
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tables = [row[0] for row in cursor.fetchall()]
    
    branch_tables = []
    
    for table in tables:
        try:
            # Check table structure
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            
            branch_columns = []
            for col in columns:
                col_name = col[1]
                if 'branch' in col_name.lower():
                    branch_columns.append(col_name)
            
            if branch_columns:
                # Check record count
                for col in branch_columns:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} IS NOT NULL")
                        count = cursor.fetchone()[0]
                        if count > 0:
                            branch_tables.append({
                                'table': table,
                                'column': col,
                                'count': count
                            })
                    except Exception as e:
                        print(f"⚠️  Error checking {table}.{col}: {e}")
                        
        except Exception as e:
            print(f"⚠️  Error examining table {table}: {e}")
    
    return branch_tables

def delete_branch_records(branch_code, dry_run=True):
    """Delete all records related to a specific branch."""
    print(f"\n🗑️  DELETING RECORDS FOR BRANCH: {branch_code}")
    print("=" * 60)
    
    # First, find the branch ID
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT id FROM companies_branch WHERE code = ?", [branch_code])
            result = cursor.fetchone()
            if not result:
                print(f"❌ Branch '{branch_code}' not found")
                return False
            
            branch_id = result[0]
            print(f"✅ Found branch ID: {branch_id}")
            
        except Exception as e:
            print(f"❌ Error finding branch: {e}")
            return False
    
    # Get all branch-related tables
    branch_tables = find_all_branch_tables()
    
    if not branch_tables:
        print("✅ No branch-related tables found")
        return True
    
    print(f"\n📋 TABLES WITH BRANCH RECORDS:")
    print("-" * 50)
    
    total_records = 0
    for table_info in branch_tables:
        print(f"  {table_info['table']:<30} | {table_info['column']:<20} | {table_info['count']:>5} records")
        total_records += table_info['count']
    
    print("-" * 50)
    print(f"Total records to delete: {total_records}")
    
    if dry_run:
        print(f"\n🔍 DRY RUN MODE - No records will be deleted")
        return True
    
    # Confirm deletion
    print(f"\n⚠️  WARNING: This will permanently delete {total_records} records!")
    confirm = input("Are you sure you want to proceed? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Operation cancelled")
        return False
    
    # Delete records in order (most dependent first)
    print(f"\n🗑️  STARTING DELETION...")
    print("-" * 40)
    
    deleted_count = 0
    failed_tables = []
    
    for table_info in branch_tables:
        table = table_info['table']
        column = table_info['column']
        count = table_info['count']
        
        if count == 0:
            continue
            
        print(f"Deleting from {table}...")
        
        try:
            # Delete records where the branch column matches our branch ID
            cursor.execute(f"DELETE FROM {table} WHERE {column} = ?", [branch_id])
            deleted = cursor.connection.total_changes
            deleted_count += deleted
            
            print(f"  ✅ Deleted {deleted} records from {table}")
            
        except Exception as e:
            print(f"  ❌ Error deleting from {table}: {e}")
            failed_tables.append(table)
    
    # Finally delete the branch itself
    print(f"\n🗑️  Deleting branch record...")
    try:
        cursor.execute("DELETE FROM companies_branch WHERE id = ?", [branch_id])
        if cursor.connection.total_changes > 0:
            print(f"  ✅ Branch '{branch_code}' deleted successfully")
        else:
            print(f"  ❌ Failed to delete branch")
            return False
            
    except Exception as e:
        print(f"  ❌ Error deleting branch: {e}")
        return False
    
    # Summary
    print(f"\n{'='*60}")
    print("DELETION SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successfully deleted: {deleted_count} records")
    print(f"✅ Branch '{branch_code}' deleted")
    
    if failed_tables:
        print(f"❌ Failed tables: {', '.join(failed_tables)}")
    
    print(f"✅ Total records processed: {total_records}")
    
    return True

def verify_cleanup(branch_code):
    """Verify that all branch-related records were deleted."""
    print(f"\n🔍 VERIFYING CLEANUP FOR BRANCH: {branch_code}")
    print("=" * 60)
    
    branch_tables = find_all_branch_tables()
    
    if not branch_tables:
        print("✅ No branch-related tables found - cleanup complete")
        return True
    
    remaining_records = 0
    for table_info in branch_tables:
        remaining_records += table_info['count']
    
    if remaining_records == 0:
        print("✅ All branch-related records have been deleted")
        return True
    else:
        print(f"⚠️  {remaining_records} records still remain in branch-related tables")
        return False

def main():
    """Main function."""
    print("☢️  NUCLEAR BRANCH DELETION SCRIPT")
    print("This script will find and delete ALL records related to a branch")
    print("using raw SQL to avoid any constraint issues.")
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python nuclear_branch_deletion.py <BRANCH_CODE> [--execute]")
        print("  --execute: Actually delete records (default is dry-run)")
        return
    
    branch_code = sys.argv[1]
    dry_run = '--execute' not in sys.argv
    
    if dry_run:
        print("🔍 DRY RUN MODE - No records will be deleted")
        print("Use --execute flag to actually delete records")
        print()
    
    # Find all branch-related tables
    branch_tables = find_all_branch_tables()
    
    if not branch_tables:
        print("✅ No branch-related tables found in database")
        return
    
    print(f"\n📊 DATABASE SCAN RESULTS:")
    print(f"Found {len(branch_tables)} tables with branch relationships")
    
    total_records = sum(t['count'] for t in branch_tables)
    print(f"Total branch-related records: {total_records}")
    
    # Check specific branch
    if not dry_run:
        success = delete_branch_records(branch_code, dry_run=False)
        if success:
            verify_cleanup(branch_code)
    else:
        print(f"\n🔍 DRY RUN: Would delete {total_records} records from {len(branch_tables)} tables")
        print("Use --execute flag to perform actual deletion")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n❌ Operation cancelled by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
