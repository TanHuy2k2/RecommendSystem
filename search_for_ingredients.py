from convert_quantity import convert_quantity

def recommend_dishes(user_ingredients, df, threshold=0.5):
    recommended_dishes = []
    
    # Tiền xử lý danh sách nguyên liệu của người dùng để giảm số lần gọi hàm
    user_ingredient_dict = {
        ing['name'].lower(): convert_quantity(ing['quantity']) if 'quantity' in ing and ing['quantity'] else None
        for ing in user_ingredients
    }
    total_ingredients = len(user_ingredient_dict)

    for _, row in df.iterrows():
        dish_id = row['recipe_id']
        ingredients = row['ingredients_processed']

        matched_count = 0
        for ing in ingredients:
            ing_name = ing['name'].lower()
            ing_quantity = convert_quantity(ing['quantity']) if 'quantity' in ing and ing['quantity'] else None
            
            for key in user_ingredient_dict.keys():
                if key in ing_name:
                    user_quantity = user_ingredient_dict[key]
                    if user_quantity is None or (ing_quantity is not None and user_quantity >= ing_quantity):
                        matched_count += 1

        if matched_count / total_ingredients >= threshold:
            recommended_dishes.append(dish_id)

    return recommended_dishes
