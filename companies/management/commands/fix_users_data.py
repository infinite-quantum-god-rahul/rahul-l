from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Fix corrupted user_id data in companies_users table'

    def handle(self, *args, **options):
        self.stdout.write("Fixing corrupted user_id data...")
        
        with connection.cursor() as cursor:
            # Find corrupted records
            cursor.execute("SELECT id, user_id FROM companies_users WHERE user_id NOT REGEXP '^[0-9]+$' AND user_id IS NOT NULL")
            corrupted = cursor.fetchall()
            
            if not corrupted:
                self.stdout.write(self.style.SUCCESS("No corrupted data found!"))
                return
            
            self.stdout.write(f"Found {len(corrupted)} corrupted records:")
            for record in corrupted:
                self.stdout.write(f"  ID: {record[0]}, user_id: '{record[1]}'")
            
            # Fix by setting user_id to NULL
            cursor.execute("UPDATE companies_users SET user_id = NULL WHERE user_id NOT REGEXP '^[0-9]+$' AND user_id IS NOT NULL")
            self.stdout.write(f"Fixed {cursor.rowcount} records")
            
            # Verify fix
            cursor.execute("SELECT COUNT(*) FROM companies_users WHERE user_id NOT REGEXP '^[0-9]+$' AND user_id IS NOT NULL")
            remaining = cursor.fetchone()[0]
            self.stdout.write(f"Remaining corrupted: {remaining}")
            
            if remaining == 0:
                self.stdout.write(self.style.SUCCESS("✅ All corrupted data fixed successfully!"))
            else:
                self.stdout.write(self.style.ERROR("❌ Some corrupted data remains"))
