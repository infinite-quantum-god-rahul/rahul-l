# import_full_dump.py
# ─────────────────────────────────────────────────────────────────────────────
# ZERO-ERROR CSV → DB IMPORTER for your models and your CSV dump.
# Preserves your prior logic. Adds:
#   • Column introspection so we only write existing DB columns
#   • FK resolution using model.to_field / db_column metadata
#   • CharField length trimming to model max_length
#   • Safe decimal/int/float/date/bool parsing
#   • Robust upsert on natural unique keys when present
#   • Full log, continue-on-error
#   • Generic importer for ALL remaining CSVs that match models
# ─────────────────────────────────────────────────────────────────────────────

import os, sys, io, csv, json, zipfile, re
from datetime import datetime, date
from decimal import Decimal, InvalidOperation

# ── Django bootstrapping
try:
    from django.conf import settings  # noqa
except Exception:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spoorthi_macs.settings")
    import django
    django.setup()

from django.db import IntegrityError, connection, transaction, models
from django.apps import apps

# Import concrete models referenced by your original logic
from companies.models import (
    Company, Branch, Village, Center, Group, Cadre, Staff,
    Client, AccountHead, Voucher, Posting
)

# For generic import we will reflect models from the 'companies' app
COMPANIES_APP_LABEL = "companies"

# ─────────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────────
INPUT_FOLDER = "full_dump_csv"          # folder name if extracted
INPUT_ZIP    = "full_dump_csv.zip"      # zip name if not extracted
LOG_FILE     = "import_log.txt"

# Skip files that your explicit importers already consume
EXPLICITLY_HANDLED = {
    "branch.csv","village.csv","center.csv","groups.csv",
    "staff.csv","members.csv","acc_heads.csv","acc_cashbook.csv","aadhar.csv"
}

# ─────────────────────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────────────────────
LOGS = []
def log(msg):
    print(msg)
    LOGS.append(str(msg))

def write_log():
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(LOGS))
    except Exception:
        pass

# ─────────────────────────────────────────────────────────────────────────────
# CSV access
# ─────────────────────────────────────────────────────────────────────────────
def _folder_csv_path(name):
    return os.path.join(".", INPUT_FOLDER, name)

def open_csv(name_candidates):
    """
    Return (reader, headers, src_name) for the first matching CSV found.
    Tries folder first, then zip. Case-insensitive.
    """
    # Folder
    for cand in name_candidates:
        path = _folder_csv_path(cand)
        if os.path.exists(path):
            f = open(path, "r", encoding="utf-8", errors="replace", newline="")
            rdr = csv.DictReader(f)
            return rdr, rdr.fieldnames, path

    # Zip
    if os.path.exists(INPUT_ZIP):
        try:
            with zipfile.ZipFile(INPUT_ZIP, "r") as z:
                names = z.namelist()
                for cand in name_candidates:
                    for nm in names:
                        if os.path.basename(nm).lower() == cand.lower():
                            data = z.read(nm).decode("utf-8", errors="replace")
                            rdr = csv.DictReader(io.StringIO(data))
                            return rdr, rdr.fieldnames, f"{INPUT_ZIP}:{nm}"
        except zipfile.BadZipFile:
            pass
    return None, None, None

def list_all_csvs():
    """Return lowercased basenames for every CSV in folder or zip."""
    seen = set()
    if os.path.isdir(INPUT_FOLDER):
        for nm in os.listdir(INPUT_FOLDER):
            if nm.lower().endswith(".csv"):
                seen.add(nm.lower())
    if os.path.exists(INPUT_ZIP):
        try:
            with zipfile.ZipFile(INPUT_ZIP, "r") as z:
                for nm in z.namelist():
                    if nm.lower().endswith(".csv"):
                        seen.add(os.path.basename(nm).lower())
        except zipfile.BadZipFile:
            pass
    return sorted(seen)

# ─────────────────────────────────────────────────────────────────────────────
# Parsers / Normalizers
# ─────────────────────────────────────────────────────────────────────────────
def ci_get(row, *keys, default=None):
    if not row:
        return default
    # exact keys first
    for k in keys:
        if k is None: continue
        for cand in (k, k.lower(), k.upper(), k.title(), k.capitalize()):
            if cand in row:
                v = row[cand]
                return v if v not in ("", None, "NULL", "null", "NaN") else default
    # case-insensitive scan
    low = {k.lower(): v for k, v in row.items()}
    for k in keys:
        if k is None: continue
        v = low.get(k.lower())
        if v not in ("", None, "NULL", "null", "NaN"):
            return v
    return default

def parse_date(val):
    if val in (None, "", "NULL", "null"): return None
    s = str(val).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d-%m-%y", "%Y/%m/%d", "%d.%m.%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    if re.fullmatch(r"\d{8}", s):
        try:
            return datetime.strptime(s, "%Y%m%d").date()
        except Exception:
            pass
    return None

def parse_decimal(val):
    if val in (None, "", "NULL", "null"): return None
    try:
        return Decimal(str(val).replace(",", "").strip())
    except (InvalidOperation, ValueError):
        return None

def parse_int(val):
    if val in (None, "", "NULL", "null"): return None
    try:
        return int(str(val).strip())
    except ValueError:
        try:
            return int(float(str(val).strip()))
        except Exception:
            return None

def parse_float(val):
    if val in (None, "", "NULL", "null"): return None
    try:
        return float(str(val).strip())
    except ValueError:
        return None

def parse_bool(val):
    s = str(val).strip().lower() if val is not None else ""
    if s in {"1","true","yes","y","t"}: return True
    if s in {"0","false","no","n","f"}: return False
    return None

def norm_phone(v):
    if not v: return None
    d = re.sub(r"\D", "", str(v))
    return d if len(d) == 10 else None

def norm_aadhaar(v):
    if not v: return None
    d = re.sub(r"\D", "", str(v))
    return f"{d[0:4]} {d[4:8]} {d[8:12]}" if len(d) == 12 else None

def trim_to_max(field, val):
    if val is None: return None
    if hasattr(field, "max_length") and field.max_length:
        return str(val)[: field.max_length]
    return val

# ─────────────────────────────────────────────────────────────────────────────
# FK helpers
# ─────────────────────────────────────────────────────────────────────────────
def resolve_fk_value(field, raw_value):
    """
    Given a ForeignKey field and a raw CSV value, return the related object or None.
    Respects to_field if set. Tries common fallbacks like 'code' or 'smtcode'.
    """
    if raw_value in (None, "", "NULL", "null"): return None
    model = field.remote_field.model
    to_field = field.remote_field.field_name or model._meta.pk.name  # Django uses 'field_name' as to_field
    val = str(raw_value).strip()

    # Try exact to_field
    try:
        return model.objects.filter(**{to_field: val}).first()
    except Exception:
        pass

    # Try common keys
    for key in ("code", "smtcode", "staffcode", "VCode", "voucher_no", model._meta.pk.name):
        if key == to_field:
            continue
        try:
            obj = model.objects.filter(**{key: val}).first()
            if obj:
                return obj
        except Exception:
            continue
    return None

# ─────────────────────────────────────────────────────────────────────────────
# Explicit importers (preserve your prior flow and outputs)
# ─────────────────────────────────────────────────────────────────────────────

def get_default_company():
    comp = Company.objects.order_by("id").first()
    if comp:
        return comp
    return Company.objects.create(code="CMP001", name="GUDIVADA")

def import_company_default():
    comp = get_default_company()
    log(f"[Company] Using/created default company: {comp.code} - {comp.name}")

def upsert_branch_from_row(row):
    code = ci_get(row, "BranchID", "BranchCode", "code")
    name = ci_get(row, "Branch_Name", "BranchName", "Name", default="Branch")
    comp = get_default_company()
    obj, _ = Branch.objects.get_or_create(code=str(code) if code else None, defaults={
        "name": name, "company": comp
    })
    obj.name = name or obj.name
    obj.company = comp
    obj.open_date = parse_date(ci_get(row, "OpenDate"))
    obj.address1  = ci_get(row, "Address1")
    obj.phone     = norm_phone(ci_get(row, "Phone"))
    obj.district  = ci_get(row, "Dist", "District")
    obj.status    = "active"
    obj.raw_csv_data = row
    try:
        obj.save()
    except IntegrityError:
        obj.phone = None
        obj.save()
    return obj

def import_branches():
    rdr, hdrs, src = open_csv(["Branch.csv", "br.csv"])
    if not rdr:
        log("[Branch] CSV not found; skipping.")
        return
    log(f"[Branch] Import from {src} …")
    cnt = ok = 0
    for row in rdr:
        cnt += 1
        try:
            upsert_branch_from_row(row); ok += 1
        except Exception as e:
            log(f"[Branch] row#{cnt} ERROR: {e}")
    log(f"[Branch] done: {ok}/{cnt} rows")

def import_villages():
    rdr, hdrs, src = open_csv(["Village.csv"])
    if not rdr:
        log("[Village] CSV not found; skipping.")
        return
    log(f"[Village] Import from {src} …")
    cnt = ok = 0
    for row in rdr:
        cnt += 1
        try:
            vcode = ci_get(row, "VCode", "vcode", "Code")
            vname = ci_get(row, "VName", "vname", "Name")
            tdate = parse_date(ci_get(row, "TDate", "Date"))
            obj, _ = Village.objects.get_or_create(VCode=str(vcode) if vcode else None, defaults={"VName": vname or str(vcode)})
            obj.VName = vname or obj.VName
            obj.TDate = tdate
            obj.status = "active"
            obj.raw_csv_data = row
            obj.save(); ok += 1
        except Exception as e:
            log(f"[Village] row#{cnt} ERROR: {e}")
    log(f"[Village] done: {ok}/{cnt} rows")

def import_centers():
    rdr, hdrs, src = open_csv(["Center.csv"])
    if not rdr:
        log("[Center] CSV not found; skipping.")
        return
    log(f"[Center] Import from {src} …")
    cnt = ok = 0
    for row in rdr:
        cnt += 1
        try:
            code = ci_get(row, "CenterCode", "Centercode", "code", "CCode")
            name = ci_get(row, "Name", "CenterName")
            vcode = ci_get(row, "Village", "VCode")
            created = parse_date(ci_get(row, "creat_date", "DOC", "CreatedOn"))
            week = ci_get(row, "Week")
            meet_place = ci_get(row, "MeetPlace", "MeetingPlace")
            obj, _ = Center.objects.get_or_create(code=str(code) if code else None, defaults={"name": name or str(code)})
            if name: obj.name = name
            if vcode:
                vill = Village.objects.filter(VCode=str(vcode)).first()
                if not vill:
                    vill = Village.objects.create(VCode=str(vcode), VName=str(vcode), status="active")
                obj.village = vill
            obj.created_on = created or obj.created_on
            obj.collection_day = week or obj.collection_day
            obj.meet_place = meet_place or obj.meet_place
            obj.status = "active"
            obj.raw_csv_data = row
            obj.save(); ok += 1
        except Exception as e:
            log(f"[Center] row#{cnt} ERROR: {e}")
    log(f"[Center] done: {ok}/{cnt} rows")

def import_groups():
    rdr, hdrs, src = open_csv(["Groups.csv", "Group.csv"])
    if not rdr:
        log("[Group] CSV not found; skipping.")
        return
    log(f"[Group] Import from {src} …")
    cnt = ok = 0
    for row in rdr:
        cnt += 1
        try:
            gcode = ci_get(row, "GCode", "GroupCode", "code", "gcode")
            gname = ci_get(row, "GName", "GroupName", "name", "gname")
            center_code = ci_get(row, "CenterCode", "Cno", "cno")
            wday = ci_get(row, "WDay", "WeekDay", "wday")
            mtime = ci_get(row, "MTime", "MeetingTime")
            nb = ci_get(row, "noofBorrw", "Borrowers", "BorrowerCount", "noofborrw")
            nb = int(nb) if nb and str(nb).replace(".","",1).isdigit() else None

            obj, _ = Group.objects.get_or_create(code=str(gcode) if gcode else None, defaults={"name": gname or (gcode or "Group")})
            if gname: obj.name = gname
            if center_code:
                cen = Center.objects.filter(code=str(center_code)).first()
                if not cen:
                    cen = Center.objects.create(code=str(center_code), name=str(center_code), status="active")
                obj.center = cen
            if wday: obj.week_day = wday
            if mtime: obj.meeting_time = mtime
            if nb is not None: obj.borrower_count = nb
            obj.status = "active"
            obj.raw_csv_data = row
            obj.save(); ok += 1
        except Exception as e:
            log(f"[Group] row#{cnt} ERROR: {e}")
    log(f"[Group] done: {ok}/{cnt} rows")

def import_staff():
    rdr, hdrs, src = open_csv(["staff.csv", "Staff.csv"])
    if not rdr:
        log("[Staff] CSV not found; skipping.")
        return

    # Discover actual DB columns
    table = Staff._meta.db_table
    with connection.cursor() as cur:
        cols = {d.name for d in connection.introspection.get_table_description(cur, table)}

    possible = {c for c in (
        "staffcode","name","cadre_id","branch","branch_id","joining_date",
        "bank","ifsc","contact1","status","raw_csv_data","extra_data","designation"
    ) if c in cols}

    log(f"[Staff] Import from {src} …")
    cnt = ok = 0

    for row in rdr:
        cnt += 1
        try:
            scode = ci_get(row, "StaffCode", "SCode", "Code", "Empcode")
            name  = ci_get(row, "Name")
            cadre_name = ci_get(row, "Cader", "Cadre")
            doj   = parse_date(ci_get(row, "Doj", "JoiningDate"))
            bank  = ci_get(row, "Bank")
            ifsc  = ci_get(row, "IFSC")
            phone = norm_phone(ci_get(row, "Contact1", "Mobile", "Phone", "Contact"))
            status = ci_get(row, "Status") or "active"
            desig = ci_get(row, "Designation", "designation")
            branch_hint = ci_get(row, "Branch", "BranchID", "BranchCode", "Branch_Name", "BranchName")

            # resolve cadre
            cadre_id = None
            if "cadre_id" in possible and cadre_name:
                c = Cadre.objects.filter(name=str(cadre_name)).first()
                if not c:
                    c = Cadre.objects.create(name=str(cadre_name), branch=Branch.objects.first() or upsert_branch_from_row({}), status="active")
                cadre_id = c.id

            # resolve branch as code or id depending on schema
            branch_code_value = None
            branch_id_value = None
            if branch_hint:
                b = Branch.objects.filter(code=str(branch_hint)).first() or Branch.objects.filter(name=str(branch_hint)).first()
                if not b and str(branch_hint).isdigit():
                    b = Branch.objects.filter(code=str(int(branch_hint))).first()
                if b:
                    branch_code_value = b.code
                    branch_id_value = b.id

            # build rowvals constrained to existing columns
            rowvals = {}
            if "staffcode"     in possible: rowvals["staffcode"] = str(scode) if scode else None
            if "name"          in possible: rowvals["name"] = name
            if "designation"   in possible: rowvals["designation"] = desig
            if "cadre_id"      in possible: rowvals["cadre_id"] = cadre_id
            if "branch"        in possible: rowvals["branch"] = branch_code_value
            if "branch_id"     in possible: rowvals["branch_id"] = branch_id_value
            if "joining_date"  in possible: rowvals["joining_date"] = doj
            if "bank"          in possible: rowvals["bank"] = bank
            if "ifsc"          in possible: rowvals["ifsc"] = ifsc
            if "contact1"      in possible: rowvals["contact1"] = phone
            if "status"        in possible: rowvals["status"] = status
            if "raw_csv_data"  in possible: rowvals["raw_csv_data"] = row
            if "extra_data"    in possible: rowvals["extra_data"] = {"src":"staff.csv"}

            # upsert by staffcode if unique
            with connection.cursor() as cur:
                existing_id = None
                if "staffcode" in possible and rowvals.get("staffcode"):
                    cur.execute(f"SELECT id FROM {table} WHERE staffcode=%s LIMIT 1", [rowvals["staffcode"]])
                    r = cur.fetchone()
                    if r: existing_id = r[0]

                if existing_id:
                    sets = ", ".join(f"{k}=%s" for k in rowvals.keys())
                    cur.execute(f"UPDATE {table} SET {sets} WHERE id=%s", list(rowvals.values()) + [existing_id])
                else:
                    keys = list(rowvals.keys())
                    qmarks = ", ".join(["%s"] * len(keys))
                    cols_sql = ", ".join(keys)
                    cur.execute(f"INSERT INTO {table} ({cols_sql}) VALUES ({qmarks})", [rowvals[k] for k in keys])

            ok += 1
        except Exception as e:
            log(f"[Staff] row#{cnt} ERROR: {e}")

    log(f"[Staff] done: {ok}/{cnt} rows")

def import_clients():
    rdr, hdrs, src = open_csv(["members.csv", "Members.csv"])
    if not rdr:
        log("[Client] members.csv not found; skipping.")
        return
    log(f"[Client] Import from {src} …")
    cnt = ok = 0
    for row in rdr:
        cnt += 1
        try:
            smt = ci_get(row, "smtcode", "MemberCode", "SMTCode")
            name = ci_get(row, "name", "Name")
            gcode = ci_get(row, "Groupcode", "GCode")
            doj = parse_date(ci_get(row, "Doj", "JoinDate", "DOJ"))
            aad = norm_aadhaar(ci_get(row, "mAadhar", "AadharNo", "Aadhaar", "Aadhar"))
            ph  = norm_phone(ci_get(row, "Contact", "Mobile", "Phone", "contactno"))
            status = "active" if str(ci_get(row, "flg_active")).strip().lower() in {"1","true","active"} else "active"

            obj, _ = Client.objects.get_or_create(smtcode=str(smt) if smt else None, defaults={"name": name or (smt or "Client")})
            obj.name = name or obj.name
            if gcode:
                grp = Group.objects.filter(code=str(gcode)).first()
                if not grp:
                    grp = Group.objects.create(code=str(gcode), name=str(gcode), status="active")
                obj.group = grp
            obj.join_date = doj
            # unique collision-safe set
            obj.aadhar = aad
            obj.contactno = ph
            obj.status = status
            obj.raw_csv_data = row
            try:
                obj.save()
            except IntegrityError:
                # clear conflicting uniques and save
                try:
                    obj.aadhar = None; obj.save()
                except IntegrityError:
                    pass
                try:
                    obj.contactno = None; obj.save()
                except IntegrityError:
                    obj.aadhar = None; obj.contactno = None; obj.save()
            ok += 1
        except Exception as e:
            log(f"[Client] row#{cnt} ERROR: {e}")
    log(f"[Client] done: {ok}/{cnt} rows")

def import_account_heads():
    rdr, hdrs, src = open_csv(["ACC_Heads.csv"])
    if not rdr:
        log("[AccountHead] ACC_Heads.csv not found; skipping.")
        return
    log(f"[AccountHead] Import from {src} …")
    cnt = ok = 0
    # enforce abbreviation length from model (max 20)
    abbr_max = getattr(AccountHead._meta.get_field("abbreviation"), "max_length", 20)
    for row in rdr:
        cnt += 1
        try:
            acode = ci_get(row, "ACode", "Code")
            abbr  = ci_get(row, "Abbrivetion", "Abbreviation")
            act   = ci_get(row, "ACType", "Type")
            vt    = ci_get(row, "VType")
            name  = ci_get(row, "AName", "Name", "MasterName", "ACode")
            if abbr is not None:
                abbr = str(abbr)[:abbr_max]
            acode = str(acode)[:20] if acode else None

            obj, _ = AccountHead.objects.get_or_create(code=acode or None, defaults={
                "name": name or (acode or "AccountHead"), "abbreviation": abbr, "ac_type": act, "vtype": vt, "status": "active"
            })
            if name is not None: obj.name = name
            if abbr is not None: obj.abbreviation = abbr
            if act  is not None: obj.ac_type = act
            if vt   is not None: obj.vtype = vt
            obj.raw_csv_data = row
            obj.save(); ok += 1
        except Exception as e:
            log(f"[AccountHead] row#{cnt} ERROR: {e}")
    log(f"[AccountHead] done: {ok}/{cnt} rows")

def import_vouchers_and_postings():
    rdr, hdrs, src = open_csv(["ACC_Cashbook.csv", "Acc_Cashbook.csv"])
    if not rdr:
        log("[Voucher/Posting] ACC_Cashbook.csv not found; skipping.")
        return
    log(f"[Voucher/Posting] Import from {src} …")
    cnt = v_ok = p_ok = 0
    seen_v = set()
    auto_idx = 1

    def next_auto_vno():
        nonlocal auto_idx
        while True:
            v = f"VCH{auto_idx:07d}"  # ≤20 chars
            auto_idx += 1
            if (v not in seen_v) and (not Voucher.objects.filter(voucher_no=v).exists()):
                return v

    for row in rdr:
        cnt += 1
        try:
            vno_raw = ci_get(row, "VoucherNo", "VNo", "Voucher", "voucherno")
            vno = str(vno_raw).strip() if vno_raw else None
            if not vno:
                vno = next_auto_vno()
            tdate = parse_date(ci_get(row, "Tdate", "tdate", "Date"))
            acode = ci_get(row, "ACode", "AccountCode", "acode")
            debit = parse_decimal(ci_get(row, "Debit", "debit")) or Decimal("0")
            credit= parse_decimal(ci_get(row, "Credit", "credit")) or Decimal("0")
            ttype = ci_get(row, "TType", "Type")
            narr  = ci_get(row, "Narration")

            ah = AccountHead.objects.filter(code=str(acode)).first()
            if not ah:
                ah = AccountHead.objects.create(code=str(acode)[:20] if acode else "AHAUTO", name=str(acode) if acode else "Auto Account", status="active")

            if vno not in seen_v:
                vobj, _ = Voucher.objects.get_or_create(
                    voucher_no=vno,
                    defaults={
                        "date": tdate or date.today(),
                        "account_head": ah,
                        "narration": narr or "",
                        "status": "active",
                        "raw_csv_data": row,
                    },
                )
                if tdate: vobj.date = tdate
                if narr is not None: vobj.narration = narr
                vobj.account_head = ah
                vobj.raw_csv_data = row
                vobj.save()
                seen_v.add(vno)
                v_ok += 1
            else:
                vobj = Voucher.objects.get(voucher_no=vno)

            Posting.objects.create(
                voucher=vobj,
                account_head=ah,
                debit=debit,
                credit=credit,
                ttype=ttype,
                narration=narr or "",
                raw_csv_data=row,
            )
            p_ok += 1
        except Exception as e:
            log(f"[Voucher/Posting] row#{cnt} ERROR: {e}")
    log(f"[Voucher/Posting] done: vouchers={v_ok}, postings={p_ok}, rows={cnt}")

def patch_aadhaar_from_aadhar_csv():
    rdr, hdrs, src = open_csv(["Aadhar.csv"])
    if not rdr:
        log("[Client Aadhar] Aadhar.csv not found; skipping.")
        return
    log(f"[Client Aadhar] Patching from {src} …")
    cnt = ok = 0
    for row in rdr:
        cnt += 1
        try:
            smt = ci_get(row, "Smtcode", "SMTCode", "smtcode")
            aad = norm_aadhaar(ci_get(row, "AadharNo", "aadharno"))
            if not smt or not aad:
                continue
            try:
                cli = Client.objects.get(smtcode=str(smt))
            except Client.DoesNotExist:
                continue
            if not cli.aadhar:
                cli.aadhar = aad
                try:
                    cli.save()
                except IntegrityError:
                    cli.aadhar = None
                    cli.save()
            ok += 1
        except Exception as e:
            log(f"[Client Aadhar] row#{cnt} ERROR: {e}")
    log(f"[Client Aadhar] patched: {ok}/{cnt}")

# ─────────────────────────────────────────────────────────────────────────────
# Generic importer for ALL remaining CSVs → matching models in companies.models
# ─────────────────────────────────────────────────────────────────────────────

def titlecase_model_name(csv_basename_noext):
    """
    Convert 'ACC_Cashbookold' → 'AccCashbookold', 'equityshare31032014' → 'Equityshare31032014'
    """
    s = re.sub(r"[^0-9A-Za-z]+", " ", csv_basename_noext).strip()
    parts = [p for p in re.split(r"\s+", s) if p]
    return "".join(p[:1].upper() + p[1:].lower() for p in parts)

def get_model_for_csv(stem):
    """
    Try exact TitleCase, and a few special shims.
    """
    Model = apps.get_model(COMPANIES_APP_LABEL, titlecase_model_name(stem))
    if Model:
        return Model
    # Special aliases if needed
    aliases = {
        "acc_heads": "AccHeads",
        "acc_cashbook": "AccCashbook",
        "acc_cashbookold": "AccCashbookold",
        "mx_savings": "MXSavings",
        "mx_loans": "MXLoans",
        "mx_loancols": "MXLoancols",
        "mx_member": "MXMember",
        "mx_agent": "MXAgent",
        "mx_code": "MXCode",
        "mx_agriment": "MXAgriment",
        "rpt_daybook": "RptDaybook",
        "securitydeposit": "Securitydeposit",
        "master_loantypes": "MasterLoantypes",
        "master_loanpurposes": "MasterLoanpurposes",
        "equityshare31032014": "Equityshare31032014",
        "equityshare31032015": "Equityshare31032015",
    }
    alias = aliases.get(stem.lower())
    if alias:
        return apps.get_model(COMPANIES_APP_LABEL, alias)
    return None

def cast_value_for_field(field, raw):
    if raw in (None, "", "NULL", "null"): return None
    if isinstance(field, models.ForeignKey):
        return resolve_fk_value(field, raw)
    if isinstance(field, models.DateField):
        return parse_date(raw)
    if isinstance(field, models.DateTimeField):
        d = parse_date(raw)
        if d:
            return datetime(d.year, d.month, d.day)
        return None
    if isinstance(field, models.DecimalField):
        return parse_decimal(raw) or Decimal("0")
    if isinstance(field, models.IntegerField):
        return parse_int(raw)
    if isinstance(field, models.FloatField):
        return parse_float(raw)
    if isinstance(field, models.BooleanField):
        b = parse_bool(raw)
        return False if b is None else b
    if isinstance(field, models.CharField) or isinstance(field, models.TextField):
        return trim_to_max(field, str(raw))
    if isinstance(field, models.JSONField):
        try:
            return json.loads(raw) if isinstance(raw, str) and raw.strip().startswith(("{","[")) else raw
        except Exception:
            return {"value": raw}
    return raw

def unique_key_fields(model):
    """Return a list of unique fields to try for upsert, ordered by preference."""
    prefs = ["code","smtcode","staffcode","VCode","voucher_no","acode","voucherno","gcode","centercode"]
    uniqs = [f for f in model._meta.get_fields() if getattr(f, "unique", False)]
    # Include primary key if user-provided (rare for staging tables)
    if model._meta.pk and getattr(model._meta.pk, "unique", False):
        uniqs.append(model._meta.pk)
    # Order by prefs first
    uniq_by_name = {f.name: f for f in uniqs if hasattr(f, "name")}
    ordered = [uniq_by_name[n] for n in prefs if n in uniq_by_name]
    # Add any remaining unique fields
    for f in uniqs:
        if f not in ordered:
            ordered.append(f)
    return ordered

def import_generic_csv(basename):
    """
    Import a CSV that is not covered by explicit loaders.
    Attempts to map to a model with the same name.
    """
    stem = os.path.splitext(basename)[0]
    Model = get_model_for_csv(stem)
    if not Model:
        log(f"[Generic] {basename}: no matching model; skipping.")
        return

    rdr, hdrs, src = open_csv([basename])
    if not rdr:
        log(f"[Generic] {basename}: not found; skipping.")
        return

    log(f"[Generic:{Model.__name__}] Import from {src} …")

    # Build field map for writable fields
    fields = {f.name: f for f in Model._meta.get_fields() if hasattr(f, "attname") and not getattr(f, "auto_created", False)}
    # Determine unique keys
    uniq_list = unique_key_fields(Model)

    cnt = ok = 0
    for row in rdr:
        cnt += 1
        try:
            # Prepare attrs
            attrs = {}
            for name, field in fields.items():
                if isinstance(field, models.ManyToManyField):
                    continue  # ignore M2M here
                if name in ("id",):
                    continue
                # Prefer exact CSV key or case-insensitive matches
                raw = row.get(name)
                if raw is None:
                    # try common fallbacks: db_column, title-cased, etc.
                    dbcol = getattr(field, "db_column", None)
                    if dbcol:
                        raw = ci_get(row, dbcol)
                if raw is None:
                    # lenient map: strip underscores/case
                    lowmap = {re.sub(r"[^0-9a-z]+","", k.lower()): v for k, v in row.items()}
                    key = re.sub(r"[^0-9a-z]+","", name.lower())
                    raw = lowmap.get(key)
                # Finally cast
                val = cast_value_for_field(field, raw)
                attrs[name] = val

            # Keep original row if model has raw_csv_data
            if "raw_csv_data" in fields:
                attrs["raw_csv_data"] = row

            # Upsert by the first unique field that has a value
            obj = None
            for uf in uniq_list:
                uf_name = getattr(uf, "name", None)
                if not uf_name:
                    continue
                v = attrs.get(uf_name)
                if v not in (None, ""):
                    try:
                        obj = Model.objects.filter(**{uf_name: v}).first()
                    except Exception:
                        obj = None
                    if obj:
                        break

            if obj:
                for k, v in attrs.items():
                    try:
                        setattr(obj, k, v)
                    except Exception:
                        pass
                obj.save()
            else:
                # If any CharField exceeds max_length, trim before save
                for k, v in list(attrs.items()):
                    f = fields.get(k)
                    attrs[k] = trim_to_max(f, v) if isinstance(f, models.CharField) else v
                obj = Model.objects.create(**attrs)

            ok += 1
        except IntegrityError as e:
            log(f"[Generic:{Model.__name__}] row#{cnt} INTEGRITY ERROR: {e}")
        except Exception as e:
            log(f"[Generic:{Model.__name__}] row#{cnt} ERROR: {e}")

    log(f"[Generic:{Model.__name__}] done: {ok}/{cnt} rows")

def import_all_remaining_csvs():
    names = list_all_csvs()
    for nm in names:
        base = os.path.basename(nm).lower()
        if base in EXPLICITLY_HANDLED:
            continue
        # prevent double-run of already handled business CSVs by variants
        if base in {"group.csv","member.csv","voucher.csv"}:
            continue
        import_generic_csv(os.path.basename(nm))

# ─────────────────────────────────────────────────────────────────────────────
# Entry
# ─────────────────────────────────────────────────────────────────────────────
def main():
    log("─── CSV Import Start ───")
    import_company_default()
    import_branches()
    import_villages()
    import_centers()
    import_groups()
    import_staff()
    import_clients()
    import_account_heads()
    import_vouchers_and_postings()
    patch_aadhaar_from_aadhar_csv()
    import_all_remaining_csvs()
    log("─── CSV Import Finished (see import_log.txt) ───")
    write_log()

if __name__ == "__main__":
    main()
