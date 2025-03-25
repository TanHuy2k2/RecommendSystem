from convert_quantity import convert_quantity

def recommend_dishes(user_ingredients, df):
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

        matched_ingredients = set()  # Dùng set để đảm bảo không tính trùng
        for ing in ingredients:
            ing_name = ing['name'].lower()
            ing_quantity = convert_quantity(ing['quantity']) if 'quantity' in ing and ing['quantity'] else None

            for key, user_quantity in user_ingredient_dict.items():
                if key in ing_name:  
                    # Nếu số lượng nguyên liệu hợp lệ
                    if user_quantity is None or (ing_quantity is not None and user_quantity >= ing_quantity):
                        matched_ingredients.add(key)  # Chỉ thêm nếu hợp lệ

        # Kiểm tra xem có đủ tất cả nguyên liệu người dùng nhập không
        if len(matched_ingredients) == total_ingredients:
            recommended_dishes.append(dish_id)

    return recommended_dishes

