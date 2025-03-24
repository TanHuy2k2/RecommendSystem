from convert_quantity import convert_quantity

def recommend_dishes(user_ingredients, df, threshold=0.5):
    recommended_dishes = []
    
    # Tiền xử lý danh sách nguyên liệu của người dùng để giảm số lần gọi hàm
    user_ingredient_dict = {
        ing['name'].lower(): convert_quantity(ing['quantity']) 
        for ing in user_ingredients
    }
    total_ingredients = len(user_ingredient_dict)

    for _, row in df.iterrows():
        dish_id = row['recipe_id']
        ingredients = row['ingredients_processed']

        matched_count = sum(
            user_ingredient_dict.get(ing['name'].lower(), float('-inf')) >= convert_quantity(ing['quantity'])
            for ing in ingredients
        )

        if matched_count / total_ingredients >= threshold:
            recommended_dishes.append(dish_id)

    return recommended_dishes
