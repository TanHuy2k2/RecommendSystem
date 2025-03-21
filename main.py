from flask import Flask, render_template, request, jsonify
import pandas as pd
from extract_ingredients import extract_ingredient
from load_food import load_foods
from knn import predict_recipe
from search_for_ingredients import recommend_dishes

app = Flask(__name__)

foods = load_foods()

df_main = pd.DataFrame(foods)

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the search request
@app.route('/search', methods=['GET'])
def search_food():
    query = request.args.get('query', '').lower()
    recommended = predict_recipe(query)

    quantities, ingredients = extract_ingredient(query)

    X = []
    for i, j in zip(ingredients, quantities):
       X.append({"name": i, "quantity": str(j)})

    recommendations = recommend_dishes(X, df_main, limit=10)
 
    common_ids = list(set(recommendations).intersection(recommended['recipe_id'].values))
    results = [food for food in foods if food['recipe_id'] in common_ids]

    return jsonify(results)

# Route to send the first 10 foods by default
@app.route('/foods', methods=['GET'])
def get_foods():
    return jsonify(foods[:10])

if __name__ == '__main__':
    app.run()
