import re
from collections import Counter
from load_food import load_foods

processed_data = load_foods()

# Nhóm nguyên liệu với từ điển ánh xạ
ingredient_groups = {
    "Trứng": ["Trứng gà", "Trứng vịt", "trứng cút", "trứng ngỗng", "trứng muối"],
    "Thịt gà": ["thịt gà", "cánh gà", "đùi gà", "ức gà", "lòng gà", "chân gà", "mề gà", "gan gà"],
    "Thịt heo": ["thịt heo", "sườn heo", "ba chỉ heo", "giò heo", "móng giò", "nạc heo", "lưỡi heo", "tim heo", "gan heo"],
    "Thịt bò": ["thịt bò", "bắp bò", "gân bò", "đuôi bò", "sườn bò", "bò viên"],
    "Thịt vịt": ["thịt vịt", "đùi vịt", "cánh vịt", "lòng vịt", "mề vịt", "gan vịt"],
    "Cá": ["cá hồi", "cá basa", "cá thu", "cá lóc", "cá chép", "cá rô", "cá trê", "cá ngừ", "cá bống", "cá nục"],
    "Hải sản": ["tôm", "cua", "ghẹ", "mực", "bạch tuộc", "nghêu", "sò", "ốc", "hàu"],
    "Củ & Khoai": ["cà rốt", "su hào", "củ cải", "củ dền", "khoai tây", "khoai lang", "khoai môn"],
    "Trái cây": ["xoài", "dưa hấu", "chuối", "bơ", "ổi", "cam", "chanh", "bưởi", "táo", "lê", "nho", "dứa"],
    "Tinh bột": ["gạo", "nếp", "bún", "phở", "miến", "bánh mì"],
}

# Tạo từ điển ánh xạ nguyên liệu -> nhóm
ingredient_to_group = {keyword: group for group, keywords in ingredient_groups.items() for keyword in keywords}

# Bộ đếm nguyên liệu
ingredient_count = {group: Counter() for group in ingredient_groups}

def classify_ingredient(ingredient_name):
    """Xác định nhóm nguyên liệu dựa trên từ điển tra cứu nhanh."""
    for keyword, group in ingredient_to_group.items():
        if keyword in ingredient_name.lower():
            return group, keyword
    return None, None

def get_categories():
    """Phân loại và đếm nguyên liệu theo nhóm."""
    for recipe in processed_data:
        for ingredient in recipe.get("ingredients_processed", []):
            ingredient_name = ingredient["name"]
            group, keyword = classify_ingredient(ingredient_name)
            if group:
                ingredient_count[group][keyword] += 1

    # Lọc ra top 5 nguyên liệu phổ biến nhất cho mỗi nhóm
    final_result = {
        category: [ingredient.capitalize() for ingredient, _ in count.most_common(5)]
        for category, count in ingredient_count.items()
        if count
    }

    return final_result
