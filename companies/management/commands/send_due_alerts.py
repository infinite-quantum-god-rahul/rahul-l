# companies/management/commands/send_due_alerts.py
from django.core.management.base import BaseCommand
from django.utils.timezone import localdate
from django.apps import apps

EPS = 1e-2  # float tolerance

def parse_dt(s):
    from datetime import datetime
    if not s:
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(str(s).strip(), fmt).date()
        except Exception:
            pass
    return None

def _f(v):
    try:
        return float(v or 0)
    except Exception:
        return 0.0

def _fmt_amt(v):
    return f"₹{_f(v):.2f}"

class Command(BaseCommand):
    help = "Send upcoming/overdue EMI alerts derived from extra_data.emi_schedule"

    def handle(self, *args, **opts):
        LoanApplication = apps.get_model("companies", "LoanApplication")
        today = localdate()
        qs = LoanApplication.objects.all()

        sent = 0
        for la in qs:
            ex = la.extra_data or {}
            schedule = ex.get("emi_schedule", []) or []
            payments = ex.get("payments", []) or []

            # Aggregate payments by date (ISO)
            paid_map = {}
            for p in payments:
                d = parse_dt(p.get("date", "")) or today
                amt = _f(p.get("amount", 0))
                k = d.isoformat()
                paid_map[k] = paid_map.get(k, 0.0) + amt

            for row in schedule:
                due = parse_dt(row.get("due_date", ""))
                if not due:
                    continue
                emi_amt = _f(row.get("emi", 0))

                # Upcoming / due / overdue checks
                if due == today:
                    self._notify(la, f"EMI due today: {_fmt_amt(emi_amt)}")
                    sent += 1
                    continue

                days_to_due = (due - today).days
                if days_to_due in (3, 1):
                    self._notify(la, f"Upcoming EMI on {due.strftime('%d/%m/%Y')}: {_fmt_amt(emi_amt)}")
                    sent += 1
                    continue

                if due < today:
                    # naive overdue if no payment recorded on/after due date for >= emi
                    paid_after = 0.0
                    for k, v in paid_map.items():
                        kd = parse_dt(k)
                        if kd and kd >= due:
                            paid_after += v
                    if paid_after + EPS < emi_amt:
                        dpd = (today - due).days
                        pending = max(emi_amt - paid_after, 0.0)
                        self._notify(la, f"Overdue {dpd} days. Pending {_fmt_amt(pending)}")
                        sent += 1

        self.stdout.write(self.style.SUCCESS(f"Alerts processed: {sent}"))

    def _notify(self, loan_obj, message):
        # placeholder: integrate your SMS/email adapter here
        # e.g., sms.send(loan_obj.client.contact1, message)
        print(f"[ALERT] Loan #{loan_obj.id}: {message}")
