# companies/utils/emi.py
from datetime import date, datetime
from calendar import monthrange

def add_months(d, m):
    """Return date d advanced by m months, clamped to month-end."""
    y = d.year + (d.month - 1 + m) // 12
    m2 = (d.month - 1 + m) % 12 + 1
    day = min(d.day, monthrange(y, m2)[1])
    return date(y, m2, day)

def _to_date(d):
    """Accept date or str in dd/mm/YYYY or YYYY-mm-dd."""
    if isinstance(d, date):
        return d
    if isinstance(d, str):
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(d.strip(), fmt).date()
            except Exception:
                continue
    raise ValueError("start_date must be date or 'dd/mm/YYYY' or 'YYYY-mm-dd' string")

def _r2(x):
    """Round to 2 decimals with tiny epsilon to tame float noise."""
    return round(float(x) + 1e-9, 2)

def pmt(principal, annual_rate, months):
    """Monthly EMI for principal at annual_rate% over months."""
    principal = float(principal or 0)
    annual_rate = float(annual_rate or 0)
    months = int(months or 0)
    if months <= 0 or principal <= 0:
        return 0.0
    r = (annual_rate / 100.0) / 12.0
    if r == 0:
        return _r2(principal / months)
    return _r2(principal * r * (1 + r) ** months / ((1 + r) ** months - 1))

def build_emi_schedule(principal, annual_rate, months, start_date):
    """
    Return list of rows with keys:
      n, due_date(dd/mm/YYYY), emi, principal, interest, balance
    Preserves original structure and behavior.
    """
    principal = max(0.0, float(principal or 0))
    annual_rate = max(0.0, float(annual_rate or 0))
    months = int(months or 0)
    if months <= 0 or principal <= 0:
        return []

    start_date = _to_date(start_date)
    r = (annual_rate / 100.0) / 12.0
    emi = pmt(principal, annual_rate, months)
    bal = _r2(principal)
    out = []

    for n in range(1, months + 1):
        interest = _r2(bal * r)
        principal_comp = _r2(emi - interest)
        if principal_comp > bal:
            principal_comp = _r2(bal)
            emi = _r2(interest + principal_comp)
        due_date = add_months(start_date, n)
        bal = _r2(bal - principal_comp)
        if abs(bal) < 0.01:
            bal = 0.0
        out.append({
            "n": n,
            "due_date": due_date.strftime("%d/%m/%Y"),
            "emi": emi,
            "principal": principal_comp,
            "interest": interest,
            "balance": bal,
        })
    return out
