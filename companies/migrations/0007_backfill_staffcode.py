from django.db import migrations
from django.db.models import Q

def backfill_staffcode(apps, schema_editor):
    Staff = apps.get_model('companies', 'Staff')
    existing = set(
        Staff.objects.exclude(staffcode__isnull=True)
                     .exclude(staffcode='')
                     .values_list('staffcode', flat=True)
    )
    for s in Staff.objects.filter(Q(staffcode__isnull=True) | Q(staffcode='')):
        base = f"STA{s.pk:06d}"
        code = base
        i = 1
        while code in existing:
            code = f"{base}-{i}"
            i += 1
        s.staffcode = code
        s.save(update_fields=['staffcode'])
        existing.add(code)

class Migration(migrations.Migration):
    dependencies = [
        ('companies', '0006_alter_fieldschedule_staff_alter_staff_branch_and_more'),
    ]
    operations = [
        migrations.RunPython(backfill_staffcode, migrations.RunPython.noop),
    ]

