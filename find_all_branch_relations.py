#!/usr/bin/env python
"""
Find All Branch Relations Script
This script scans the database to find ALL tables and models that have
relationships with the Branch model to ensure we don't miss any during deletion.
"""

import os
import sys
import django
from django.db import connection

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

def find_all_branch_relations():
    """Find all tables and models that reference the Branch model."""
    print("🔍 SCANNING FOR ALL BRANCH RELATIONSHIPS")
    print("=" * 60)
    
    # Get all tables in the database
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tables = [row[0] for row in cursor.fetchall()]
    
    print(f"Found {len(tables)} tables in database")
    print()
    
    branch_relations = []
    
    for table in tables:
        try:
            # Check if table has a branch_id or branch column
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            
            branch_columns = []
            for col in columns:
                col_name = col[1]
                if 'branch' in col_name.lower():
                    branch_columns.append(col_name)
            
            if branch_columns:
                # Check if there are actual records with branch references
                for col in branch_columns:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} IS NOT NULL")
                        count = cursor.fetchone()[0]
                        if count > 0:
                            branch_relations.append({
                                'table': table,
                                'column': col,
                                'record_count': count
                            })
                    except Exception as e:
                        print(f"⚠️  Error checking {table}.{col}: {e}")
                        
        except Exception as e:
            print(f"⚠️  Error examining table {table}: {e}")
    
    # Display results
    if branch_relations:
        print("📋 TABLES WITH BRANCH RELATIONSHIPS:")
        print("=" * 60)
        
        total_records = 0
        for relation in branch_relations:
            print(f"  {relation['table']:<30} | {relation['column']:<20} | {relation['record_count']:>5} records")
            total_records += relation['record_count']
        
        print("=" * 60)
        print(f"Total tables with branch relations: {len(branch_relations)}")
        print(f"Total records with branch references: {total_records}")
        
        # Group by record count
        print("\n📊 GROUPED BY RECORD COUNT:")
        print("-" * 40)
        
        high_count = [r for r in branch_relations if r['record_count'] > 100]
        medium_count = [r for r in branch_relations if 10 < r['record_count'] <= 100]
        low_count = [r for r in branch_relations if 0 < r['record_count'] <= 10]
        
        if high_count:
            print(f"🔴 HIGH COUNT (>100): {len(high_count)} tables")
            for r in high_count:
                print(f"     {r['table']} ({r['record_count']} records)")
        
        if medium_count:
            print(f"🟡 MEDIUM COUNT (10-100): {len(medium_count)} tables")
            for r in medium_count:
                print(f"     {r['table']} ({r['record_count']} records)")
        
        if low_count:
            print(f"🟢 LOW COUNT (1-10): {len(low_count)} tables")
            for r in low_count:
                print(f"     {r['table']} ({r['record_count']} records)")
        
        # Show sample records for high-count tables
        if high_count:
            print(f"\n🔍 SAMPLE RECORDS FROM HIGH-COUNT TABLES:")
            print("-" * 50)
            
            for relation in high_count[:3]:  # Show first 3 high-count tables
                try:
                    cursor.execute(f"SELECT * FROM {relation['table']} WHERE {relation['column']} IS NOT NULL LIMIT 3")
                    samples = cursor.fetchall()
                    
                    print(f"\n{relation['table']} (showing first 3 records):")
                    for i, sample in enumerate(samples, 1):
                        print(f"  Record {i}: {sample}")
                        
                except Exception as e:
                    print(f"  Error getting samples from {relation['table']}: {e}")
        
    else:
        print("✅ No branch relationships found in database")
    
    return branch_relations

def check_specific_branch(branch_code):
    """Check a specific branch for all its related records."""
    print(f"\n🔍 CHECKING SPECIFIC BRANCH: {branch_code}")
    print("=" * 60)
    
    try:
        from companies.models import Branch
        branch = Branch.objects.get(code=branch_code)
        print(f"✅ Found branch: {branch.code} - {branch.name}")
        
        # Get all related records using our comprehensive method
        from companies.management.commands.delete_branch_complete import Command
        cmd = Command()
        related_data = cmd._get_all_related_records(branch)
        
        print(f"\n📊 RELATED RECORDS FOR BRANCH '{branch_code}':")
        print("-" * 50)
        
        total_records = 0
        for model_name, queryset in related_data.items():
            count = queryset.count()
            total_records += count
            print(f"  {model_name.replace('_', ' ').title():<30}: {count:>5}")
        
        print("-" * 50)
        print(f"Total related records: {total_records}")
        
        if total_records == 0:
            print("✅ This branch has no related records and can be deleted safely!")
        else:
            print("⚠️  This branch has related records that need to be deleted first.")
        
        return related_data
        
    except Branch.DoesNotExist:
        print(f"❌ Branch '{branch_code}' not found")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Main function."""
    print("🔧 BRANCH RELATIONSHIP SCANNER")
    print("This script finds ALL tables and models that reference the Branch model")
    print()
    
    # Get branch code if provided
    if len(sys.argv) > 1:
        branch_code = sys.argv[1]
        print(f"Checking specific branch: {branch_code}")
        check_specific_branch(branch_code)
    else:
        # Scan all tables
        find_all_branch_relations()
        
        # Ask if user wants to check a specific branch
        print(f"\n" + "=" * 60)
        response = input("Enter a branch code to check specific branch (or press Enter to exit): ").strip()
        
        if response:
            check_specific_branch(response)

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
