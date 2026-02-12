from datetime import datetime, date, time as dtime

def parse_date_generic(v):
    if isinstance(v, (datetime, date)):
        return v.date() if isinstance(v, datetime) else v
    if v is None:
        return None

    s = str(v).strip()
    if not s:
        return None

    if " " in s:
        s = s.split()[0].strip()

    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            pass
    try:
        return datetime.fromisoformat(s).date()
    except Exception:
        return None

def parse_time_generic(v):
    if isinstance(v, dtime):
        return v
    if isinstance(v, datetime):
        return v.time()
    if v is None:
        return None

    if isinstance(v, (int, float)):
        total_seg = int(round(float(v) * 24 * 3600))
        total_seg = max(total_seg, 0)
        h = (total_seg // 3600) % 24
        m = (total_seg % 3600) // 60
        s = total_seg % 60
        return dtime(h, m, s)

    s = str(v).strip()
    if not s:
        return None

    s_low = s.lower()
    s_low = s_low.replace("a. m.", "am").replace("p. m.", "pm")
    s_low = s_low.replace("a.m.", "am").replace("p.m.", "pm")
    s_low = s_low.replace(" a. m", "am").replace(" p. m", "pm")
    s_low = s_low.replace(" a.m", "am").replace(" p.m", "pm")
    s_low = s_low.replace(".", "")
    s_norm = s_low.strip().upper()

    for fmt in ("%H:%M", "%H:%M:%S", "%I:%M %p", "%I:%M:%S %p"):
        try:
            return datetime.strptime(s_norm, fmt).time()
        except Exception:
            pass
    try:
        return datetime.fromisoformat(s).time()
    except Exception:
        return None
