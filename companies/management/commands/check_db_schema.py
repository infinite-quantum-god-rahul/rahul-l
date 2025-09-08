#!/usr/bin/env python
"""
Django management command to check and fix database schema issues.
Run with: python manage.py check_db_schema
"""

from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps

class Command(BaseCommand):
    help = 'Check and fix database schema issues automatically'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Automatically fix missing columns',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed information',
        )

    def handle(self, *args, **options):
        fix_mode = options['fix']
        verbose = options['verbose']
        
        if fix_mode:
            self.stdout.write(self.style.SUCCESS('🔧 Running in FIX mode - will automatically add missing columns'))
        else:
            self.stdout.write(self.style.WARNING('🔍 Running in CHECK mode - use --fix to automatically fix issues'))
        
        self.stdout.write('=' * 60)
        
        # Get all models
        all_models = apps.get_models()
        
        total_issues = 0
        total_fixed = 0
        
        for model in all_models:
            try:
                # Skip Django internal models
                if model._meta.app_label in ['admin', 'auth', 'contenttypes', 'sessions']:
                    continue
                
                model_name = model.__name__
                table_name = model._meta.db_table
                
                if verbose:
                    self.stdout.write(f"Checking {model_name} ({table_name})...")
                
                # Get model fields
                model_fields = model._meta.get_fields()
                
                # Check database table structure
                with connection.cursor() as cursor:
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    db_columns = cursor.fetchall()
                    db_column_names = [col[1] for col in db_columns]
                    
                    # Check for missing columns
                    missing_columns = []
                    for field in model_fields:
                        if hasattr(field, 'db_column') and field.db_column:
                            if field.db_column not in db_column_names:
                                missing_columns.append({
                                    'name': field.db_column,
                                    'type': self._get_sqlite_type(field),
                                    'nullable': field.null
                                })
                        elif hasattr(field, 'name') and field.name not in db_column_names:
                            # Skip some Django internal fields
                            if field.name not in ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']:
                                missing_columns.append({
                                    'name': field.name,
                                    'type': self._get_sqlite_type(field),
                                    'nullable': field.null
                                })
                    
                    if missing_columns:
                        total_issues += len(missing_columns)
                        self.stdout.write(
                            self.style.ERROR(f"❌ {model_name}: {len(missing_columns)} missing columns")
                        )
                        
                        if verbose:
                            for col in missing_columns:
                                self.stdout.write(f"   - {col['name']} ({col['type']})")
                        
                        # Fix missing columns if in fix mode
                        if fix_mode:
                            fixed_count = self._fix_missing_columns(cursor, table_name, missing_columns)
                            total_fixed += fixed_count
                            if fixed_count > 0:
                                self.stdout.write(
                                    self.style.SUCCESS(f"   ✅ Fixed {fixed_count} columns")
                                )
                    else:
                        if verbose:
                            self.stdout.write(f"✅ {model_name}: All columns present")
                            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ {model.__name__}: Error checking columns - {e}")
                )
                continue
        
        self.stdout.write('=' * 60)
        
        if total_issues == 0:
            self.stdout.write(self.style.SUCCESS('🎉 No database schema issues found!'))
        else:
            if fix_mode:
                self.stdout.write(
                    self.style.SUCCESS(f'🎉 Fixed {total_fixed} out of {total_issues} missing columns!')
                )
                if total_fixed < total_issues:
                    self.stdout.write(
                        self.style.WARNING(f'⚠️  {total_issues - total_fixed} columns could not be fixed automatically')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Found {total_issues} missing columns. Run with --fix to fix them automatically.')
                )
    
    def _get_sqlite_type(self, field):
        """Get the appropriate SQLite type for a Django field."""
        if hasattr(field, 'get_internal_type'):
            field_type = field.get_internal_type()
            
            if field_type in ['CharField', 'TextField']:
                return 'VARCHAR(255)'
            elif field_type in ['IntegerField', 'PositiveIntegerField']:
                return 'INTEGER'
            elif field_type in ['DecimalField', 'FloatField']:
                return 'REAL'
            elif field_type in ['BooleanField']:
                return 'INTEGER'
            elif field_type in ['DateField', 'DateTimeField']:
                return 'TEXT'
            elif field_type in ['ForeignKey', 'OneToOneField']:
                return 'INTEGER'
            else:
                return 'TEXT'
        else:
            return 'TEXT'
    
    def _fix_missing_columns(self, cursor, table_name, missing_columns):
        """Fix missing columns by adding them to the table."""
        fixed_count = 0
        
        for col in missing_columns:
            try:
                column_name = col['name']
                column_type = col['type']
                nullable = col['nullable']
                
                # Add the missing column
                null_constraint = "" if nullable else " NOT NULL"
                sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}{null_constraint}"
                
                cursor.execute(sql)
                fixed_count += 1
                
            except Exception as e:
                # Log the error but continue with other columns
                continue
        
        return fixed_count
