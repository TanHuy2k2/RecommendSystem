from convert_quantity import convert_quantity

def recommend_dishes(user_ingredients, df, limit, threshold=0.5):
     recommended_dishes = []
     
     # Duyệt qua từng món ăn
     for _, row in df.iterrows():
         dish_id = row['recipe_id']
         ingredients = row['ingredients_processed']
         
         matched_count = 0  # Đếm số nguyên liệu phù hợp
         total_ingredients = len(user_ingredients)  # Tổng số nguyên liệu đầu vào
         
         for user_ingredient in user_ingredients:
             user_name = user_ingredient['name'].lower()
             user_qty = convert_quantity(user_ingredient['quantity'])
             
             for ingredient in ingredients:
                ingredient_name = ingredient['name'].lower()
                ingredient_qty = convert_quantity(ingredient['quantity'])
                 
                if user_name == ingredient_name and ingredient_qty <= user_qty:
                     matched_count += 1
                     break  # Chỉ cần tìm thấy 1 lần thì dừng vòng lặp
 
         # Kiểm tra tỷ lệ nguyên liệu phù hợp
         match_ratio = matched_count / total_ingredients
         
         if match_ratio >= threshold:
             recommended_dishes.append(dish_id)
         
         if len(recommended_dishes) >= limit:
             break
     
     return recommended_dishes