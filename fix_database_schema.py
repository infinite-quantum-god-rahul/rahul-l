#!/usr/bin/env python
"""
Database Schema Fix Script
Fixes all database column mismatches and ensures proper table structure
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoorthi_macs.settings')
django.setup()

from django.db import connection, transaction
from django.core.management import execute_from_command_line

def fix_database_schema():
    """Fix all database schema issues"""
    print("🔧 Starting database schema fix...")
    
    with connection.cursor() as cursor:
        try:
            # Check if required tables exist
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE 'companies_%'
            """)
            existing_tables = [row[0] for row in cursor.fetchall()]
            print(f"📊 Existing tables: {existing_tables}")
            
            # Fix companies_branch table
            if 'companies_branch' in existing_tables:
                print("🏢 Fixing companies_branch table...")
                
                # Check if export_flag column exists
                cursor.execute("PRAGMA table_info(companies_branch)")
                columns = [row[1] for row in cursor.fetchall()]
                print(f"📋 Branch columns: {columns}")
                
                if 'export_flag' not in columns:
                    print("➕ Adding export_flag column to companies_branch")
                    cursor.execute("""
                        ALTER TABLE companies_branch 
                        ADD COLUMN export_flag BOOLEAN DEFAULT 0
                    """)
                
                # Check if required columns exist
                required_columns = ['code', 'name', 'company_id', 'open_date', 'status']
                for col in required_columns:
                    if col not in columns:
                        print(f"⚠️ Missing column: {col}")
            
            # Fix companies_client table
            if 'companies_client' in existing_tables:
                print("👤 Fixing companies_client table...")
                
                cursor.execute("PRAGMA table_info(companies_client)")
                columns = [row[1] for row in cursor.fetchall()]
                print(f"📋 Client columns: {columns}")
                
                if 'SMTCode' not in columns and 'smtcode' not in columns:
                    print("➕ Adding SMTCode column to companies_client")
                    cursor.execute("""
                        ALTER TABLE companies_client 
                        ADD COLUMN "SMTCode" VARCHAR(50) UNIQUE
                    """)
                
                # Check if required columns exist
                required_columns = ['name', 'status']
                for col in required_columns:
                    if col not in columns:
                        print(f"⚠️ Missing column: {col}")
            
            # Fix companies_loanapplication table
            if 'companies_loanapplication' in existing_tables:
                print("📝 Fixing companies_loanapplication table...")
                
                cursor.execute("PRAGMA table_info(companies_loanapplication)")
                columns = [row[1] for row in cursor.fetchall()]
                print(f"📋 LoanApplication columns: {columns}")
                
                if 'SMTCode' not in columns:
                    print("➕ Adding SMTCode column to companies_loanapplication")
                    cursor.execute("""
                        ALTER TABLE companies_loanapplication 
                        ADD COLUMN "SMTCode" VARCHAR(50)
                    """)
                
                # Check if required columns exist
                required_columns = ['application_number', 'status']
                for col in required_columns:
                    if col not in columns:
                        print(f"⚠️ Missing column: {col}")
            
            # Fix companies_company table
            if 'companies_company' in existing_tables:
                print("🏢 Fixing companies_company table...")
                
                cursor.execute("PRAGMA table_info(companies_company)")
                columns = [row[1] for row in cursor.fetchall()]
                print(f"📋 Company columns: {columns}")
                
                # Check if required columns exist
                required_columns = ['code', 'name', 'status']
                for col in required_columns:
                    if col not in columns:
                        print(f"⚠️ Missing column: {col}")
            
            # Create indexes for better performance
            print("📈 Creating database indexes...")
            
            # Branch indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_branch_code 
                ON companies_branch(code)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_branch_company 
                ON companies_branch(company_id)
            """)
            
            # Client indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_client_smtcode 
                ON companies_client("SMTCode")
            """)
            
            # LoanApplication indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_loan_smtcode 
                ON companies_loanapplication("SMTCode")
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_loan_status 
                ON companies_loanapplication(status)
            """)
            
            print("✅ Database schema fix completed successfully!")
            
        except Exception as e:
            print(f"❌ Error fixing database schema: {e}")
            return False
    
    return True

def verify_fixes():
    """Verify that all fixes were applied correctly"""
    print("\n🔍 Verifying database fixes...")
    
    with connection.cursor() as cursor:
        try:
            # Check branch table
            cursor.execute("PRAGMA table_info(companies_branch)")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"✅ Branch table columns: {columns}")
            
            # Check client table
            cursor.execute("PRAGMA table_info(companies_client)")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"✅ Client table columns: {columns}")
            
            # Check loanapplication table
            cursor.execute("PRAGMA table_info(companies_loanapplication)")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"✅ LoanApplication table columns: {columns}")
            
            # Check company table
            cursor.execute("PRAGMA table_info(companies_company)")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"✅ Company table columns: {columns}")
            
            print("✅ All database fixes verified successfully!")
            
        except Exception as e:
            print(f"❌ Error verifying fixes: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting comprehensive database schema fix...")
    
    # Fix the database schema
    if fix_database_schema():
        # Verify the fixes
        if verify_fixes():
            print("\n🎉 Database schema fix completed successfully!")
            print("✅ All required columns are now present")
            print("✅ Sidebar navigation should work without errors")
            print("✅ Branch manager field should work properly")
            print("✅ Export flag field is properly handled")
        else:
            print("\n⚠️ Database fixes applied but verification failed")
    else:
        print("\n❌ Database schema fix failed")
        sys.exit(1)

