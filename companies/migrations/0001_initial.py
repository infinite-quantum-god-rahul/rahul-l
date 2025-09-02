# Generated manually for fresh start

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_data', models.JSONField(blank=True, default=dict, null=True)),
                ('raw_csv_data', models.JSONField(blank=True, null=True)),
                ('code', models.CharField(blank=True, max_length=50, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('opening_date', models.DateField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='company_logos/')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending'), ('blocked', 'Blocked')], default='active', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_data', models.JSONField(blank=True, default=dict, null=True)),
                ('raw_csv_data', models.JSONField(blank=True, null=True)),
                ('code', models.CharField(blank=True, max_length=50, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('open_date', models.DateField(blank=True, null=True)),
                ('address1', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('district', models.CharField(blank=True, max_length=100, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='companies.company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_data', models.JSONField(blank=True, default=dict, null=True)),
                ('raw_csv_data', models.JSONField(blank=True, null=True)),
                ('staffcode', models.CharField(blank=True, max_length=50, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('joining_date', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending'), ('blocked', 'Blocked')], default='active', max_length=20)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_members', to='companies.branch')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_data', models.JSONField(blank=True, default=dict, null=True)),
                ('raw_csv_data', models.JSONField(blank=True, null=True)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_master', models.BooleanField(default=False)),
                ('is_data_entry', models.BooleanField(default=False)),
                ('is_reports', models.BooleanField(default=False)),
                ('is_accounting', models.BooleanField(default=False)),
                ('is_recovery_agent', models.BooleanField(default=False)),
                ('is_auditor', models.BooleanField(default=False)),
                ('is_manager', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending'), ('blocked', 'Blocked')], default='active', max_length=20)),
                ('password', models.CharField(blank=True, help_text='Hashed password for non-Django auth use', max_length=128, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user')),
                ('staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='companies.staff')),
                ('branch', models.ForeignKey(blank=True, db_column='branch', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='companies.branch')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
