# Generated manually to fix the users.user field conversion

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def convert_user_field_to_foreignkey(apps, schema_editor):
    """
    Convert the user field from CharField (username) to ForeignKey (user_id)
    """
    Users = apps.get_model('companies', 'Users')
    User = apps.get_model('auth', 'User')
    
    # Get the database connection
    db_alias = schema_editor.connection.alias
    
    # First, add the user_id column
    schema_editor.execute("""
        ALTER TABLE companies_users 
        ADD COLUMN user_id INTEGER REFERENCES auth_user(id)
    """)
    
    # Update user_id based on usernames
    for user_record in Users.objects.using(db_alias).all():
        if user_record.user and user_record.user != 'None':
            try:
                django_user = User.objects.using(db_alias).get(username=user_record.user)
                user_record.user_id = django_user.id
                user_record.save(using=db_alias)
            except User.DoesNotExist:
                # If user doesn't exist, leave user_id as NULL
                pass
    
    # Remove the old user column
    schema_editor.execute("""
        ALTER TABLE companies_users 
        DROP COLUMN user
    """)


def reverse_convert_user_field(apps, schema_editor):
    """
    Reverse the conversion (for rollback)
    """
    Users = apps.get_model('companies', 'Users')
    User = apps.get_model('auth', 'User')
    
    db_alias = schema_editor.connection.alias
    
    # Add back the user column
    schema_editor.execute("""
        ALTER TABLE companies_users 
        ADD COLUMN user VARCHAR(150)
    """)
    
    # Populate with usernames
    for user_record in Users.objects.using(db_alias).all():
        if user_record.user_id:
            try:
                django_user = User.objects.using(db_alias).get(id=user_record.user_id)
                user_record.user = django_user.username
                user_record.save(using=db_alias)
            except User.DoesNotExist:
                user_record.user = None
                user_record.save(using=db_alias)
    
    # Remove the user_id column
    schema_editor.execute("""
        ALTER TABLE companies_users 
        DROP COLUMN user_id
    """)


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0008_remove_userpermission_is_admin_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userpermission',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userpermission',
            name='is_auditor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userpermission',
            name='is_reports',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='users',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='users',
            name='is_auditor',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='is_reports',
            field=models.BooleanField(default=False),
        ),
        # Custom operation to handle the user field conversion
        migrations.RunPython(
            convert_user_field_to_foreignkey,
            reverse_convert_user_field,
        ),
    ]
