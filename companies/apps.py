from django.apps import AppConfig


class CompaniesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'companies'
    
    def ready(self):
        """Run when Django starts up."""
        import os
        
        # Only run in production or when explicitly requested
        if os.environ.get('RUN_MAIN') != 'true':
            try:
                # Import and run database schema check
                from .management.commands.check_db_schema import Command
                command = Command()
                command.handle(fix=True, verbose=False)
            except Exception as e:
                # Log the error but don't crash the app
                print(f"Warning: Could not auto-fix database schema: {e}")
                pass
