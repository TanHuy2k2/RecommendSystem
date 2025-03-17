import re
from fractions import Fraction

def convert_quantity(quantity_str):
    unit_conversion = {
        "g": 1, "grams": 1,
        "kg": 1000, "kilograms": 1000,
        "oz": 28.35, "ounce": 28.35, "ounces": 28.35,
        "lb": 453.592, "lbs": 453.592,
        "tsp": 5, "teaspoon": 5, "teaspoons": 5,
        "tbsp": 15, "tablespoon": 15, "tablespoons": 15, "tbs": 15,
        "cup": 125, "cups": 125,
        "ml": 1,
        "pinch": 0.5, "handful": 30, "dash": 0.6
    }

    unicode_fractions = {
        '½': '1/2', '⅓': '1/3', '⅔': '2/3', '¼': '1/4', '¾': '3/4',
        '⅕': '1/5', '⅖': '2/5', '⅗': '3/5', '⅘': '4/5',
        '⅙': '1/6', '⅚': '5/6', '⅛': '1/8', '⅜': '3/8', '⅝': '5/8', '⅞': '7/8'
    }

    quantity_str = quantity_str.strip().lower()

    # Thay thế các ký hiệu phân số Unicode
    for uf, frac in unicode_fractions.items():
        quantity_str = quantity_str.replace(uf, frac)

    # Xóa phần trong ngoặc
    quantity_str = re.sub(r'\(.*?\)', '', quantity_str).strip()

    # Nếu số nguyên dính liền với phân số (ví dụ "2½" -> "2 1/2")
    quantity_str = re.sub(r'(\d)(\d+/\d+)', r'\1 \2', quantity_str)

    # Nếu có ký tự "/" trong cụm đơn vị, chia nhỏ và lấy giá trị lớn nhất
    if " / " in quantity_str or re.search(r'[a-zA-Z]/', quantity_str):
        parts = re.split(r'\s*/\s*', quantity_str)
        try:
            values = [convert_quantity(part.strip()) for part in parts]
            return max(values)
        except:
            pass

    match = re.match(r'^([\d\s./]+)?\s*([a-zA-Z.]*)$', quantity_str)
    if match:
        num_part, unit = match.groups()
        try:
            num_value = sum(Fraction(s) for s in num_part.split()) if num_part else 1
        except:
            num_value = 1

        unit = unit.rstrip(".")
        if unit in unit_conversion:
            return round(float(num_value) * unit_conversion[unit], 2)
        else:
            return round(float(num_value), 2)
    
    return 1.0