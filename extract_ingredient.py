import re
from convert_quantily import convert_quantity

def extract_ingredient(text):
    # Split by commas to process each ingredient separately
    ingredients = text.split(",")
    ingredient_list = []
    quantity_list = []

    for ingredient in ingredients:
        ingredient = ingredient.strip()
        pattern = r"(?P<quantity>\d+(?:\.\d+)?)(?P<unit>[a-zA-Z]*)\s*(?P<ingredient>[a-zA-Z\s]+)"
        match = re.match(pattern, ingredient)
        if match:
            quantity_unit = match.group("quantity") + (match.group("unit") if match.group("unit") else "")
            ingredient_name = match.group("ingredient").strip()
            ingredient_list.append(ingredient_name)
            quantity_list.append(convert_quantity(quantity_unit))

    return ingredient_list, quantity_list
