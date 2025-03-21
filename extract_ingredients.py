import re
 
def extract_ingredient(text):
    ingredients = text.split(",")  # Tách từng nguyên liệu theo dấu phẩy
    ingredient_list = []
    quantity_list = []

    for ingredient in ingredients:
        ingredient = ingredient.strip()
        pattern = r"^(?P<quantity>\d+(?:\.\d+)?)(?P<unit>[a-zA-Z]*)\s+(?P<ingredient>.+)$"
        match = re.match(pattern, ingredient)

        if match:
            quantity = match.group("quantity") + (match.group("unit") if match.group("unit") else "")
            ingredient_name = match.group("ingredient").strip()
        else:
            pattern = r"^(?P<ingredient>.+?)\s+(?P<quantity>\d+(?:\.\d+)?)(?P<unit>[a-zA-Z]*)$"
            match_1 = re.match(pattern, ingredient)

            if match_1:
                quantity = match_1.group("quantity") + (match_1.group("unit") if match_1.group("unit") else "")
                ingredient_name = match_1.group("ingredient").strip()
            else:
                quantity = ""
                ingredient_name = ingredient   

        quantity_list.append(quantity)
        ingredient_list.append(ingredient_name)

    return quantity_list, ingredient_list