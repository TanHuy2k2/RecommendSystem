from fractions import Fraction
import re

# --- Đơn vị và quy đổi ---
unit_conversion = {
    "g": 1, "gam": 1, "gr": 1,
    "kg": 1000, "kilogam": 1000,
    "ml": 1, "lít": 1000,
    "m": 5, "M": 15, "chén": 240, "chen": 240,
    "xấp": 125, "gói": 10,
    "cây": 30, "cọng": 1, "viên": 10, "tai": 20,
    "quả": 100, "trái": 100,
    "củ nhỏ": 30, "củ lớn": 70, "củ": 50,
    "miếng nhỏ": 30, "miếng": 50,
    "lát": 25, "con": 50
}

# --- Clean string ---
def clean_quantity_str(q_str):
    q_str = q_str.strip()
    q_str = re.sub(r'(\d)([a-zA-ZÀ-Ỵà-ỵ])', r'\1 \2', q_str)  # "1quả" ➜ "1 quả"
    q_str = q_str.split('(')[0].strip()
    q_str = q_str.split(':')[0].strip()
    return q_str


# --- Parse number part ---
def parse_number(num_str):
    try:
        return float(sum(Fraction(s) for s in num_str.strip().split()))
    except:
        return 1.0

# --- Convert quantity ---
def convert_quantity(quantity_str):
    q_str = clean_quantity_str(quantity_str)
    if q_str == "1":
        return 5.0

    pattern = r'^([\d\s./]+)\s+(.+)$'  # e.g. "1/2 củ nhỏ"
    match = re.match(pattern, q_str)

    if match:
        num_part, unit = match.groups()
        num_value = parse_number(num_part)
        unit = unit.lower().strip()
        factor = unit_conversion.get(unit)
        if factor:
            return round(num_value * factor, 2)
        return round(num_value, 2)

    # Try parse full string as a number (fallback)
    try:
        return float(Fraction(q_str))
    except:
        return 5.0  # Default