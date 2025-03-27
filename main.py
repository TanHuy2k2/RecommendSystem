from flask import Flask, render_template, request, jsonify
import pandas as pd
from extract_ingredients import extract_ingredient
from load_food import load_foods
from knn import predict_recipe
from search_for_ingredients import recommend_dishes
from categories import get_categories
# from flask_cors import CORS

app = Flask(__name__)

# CORS(app)

foods = load_foods()

df_main = pd.DataFrame(foods)

# Route to render the HTML page
@app.route('/')
def index():
    category = get_categories()
    return render_template('index.html', categories=category)

# Route to handle the search request
@app.route('/search', methods=['GET'])
def search_food():
    query = request.args.get('query', '').lower()
    if query == '':
        return jsonify(foods[:12])
    else:
        recommended = predict_recipe(query)

        quantities, ingredients = extract_ingredient(query)

        X = []
        for i, j in zip(ingredients, quantities):
            if j == "":
                X.append({"name": i})
            else:
                X.append({"name": i, "quantity": str(j)})

        filtered_recipes = df_main.loc[df_main["recipe_id"].isin(recommended['recipe_id'].values), ["recipe_id", "ingredients_processed"]]

        recommendations = recommend_dishes(X, filtered_recipes)
    
        results = [food for food in foods if food['recipe_id'] in recommendations]

        if results:
            return jsonify(results)
        return jsonify([])
@app.route('/recommend', methods=['GET'])
def recommend_food():
    query = request.args.get('query', '').lower()

    recommended = predict_recipe(query)

    quantities, ingredients = extract_ingredient(query)

    X = []
    for i, j in zip(ingredients, quantities):
        if j == "":
            X.append({"name": i})
        else:
            X.append({"name": i, "quantity": str(j)})

    filtered_recipes = df_main.loc[df_main["recipe_id"].isin(recommended['recipe_id'].values), ["recipe_id", "ingredients_processed"]]

    recommendations = recommend_dishes(X, filtered_recipes, threshold=0.5)
    
    results = [food for food in foods if food['recipe_id'] in recommendations]

    if results:
        return jsonify(results[:4])
    return jsonify([])
# Route to send the first 10 foods by default
@app.route('/foods', methods=['GET'])
def get_foods():
    return jsonify(foods[:12])

if __name__ == '__main__':
    app.run()
