from convert_quantity import convert_quantity

def recommend_dishes(user_ingredients, df, threshold=0.5):
    recommended_dishes = []
    for _, row in df.iterrows():
        dish_id = row['recipe_id']
        ingredients = row['ingredients_processed']
        
        matched_count = 0

        total_ingredients = len(user_ingredients)

        for user_ingredient in user_ingredients:
             user_name = user_ingredient['name'].lower()
             user_qty = convert_quantity(user_ingredient['quantity'])

             for ingredient in ingredients:
                ingredient_name = ingredient['name'].lower()
                ingredient_qty = convert_quantity(ingredient['quantity'])

                if user_name in ingredient_name and ingredient_qty <= user_qty:
                    matched_count += 1

                    match_ratio = matched_count / total_ingredients

                    if match_ratio >= threshold:
                          recommended_dishes.append(dish_id)
    return recommended_dishes