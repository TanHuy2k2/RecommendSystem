from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import json
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

# Sample food data
def load_foods():
    with open('meals_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    
foods = load_foods()

# model knn for food recommendation
recipe_df = pd.DataFrame(foods)

recipe_df["ingredients_text"] = recipe_df["ingredients"].apply(
    lambda x: ", ".join([f"{ing['quantity']} {ing['name']}" for ing in x])
)

# TF-IDF Vectorization of Ingredients
vectorizer = TfidfVectorizer()
X_ingredients = vectorizer.fit_transform(recipe_df["ingredients_text"])

# Train KNN Model
knn = NearestNeighbors(n_neighbors=5, metric="cosine")  # Cosine similarity for text
knn.fit(X_ingredients)

# Function to Recommend Recipe IDs
def recommend_recipe_ids(input_ingredients):
    input_transformed = vectorizer.transform([input_ingredients])
    distances, indices = knn.kneighbors(input_transformed)
    recipe_ids = recipe_df.iloc[indices[0]]["id"].tolist()  # Extract IDs
    return recipe_ids

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the search request
@app.route('/search', methods=['GET'])
def search_food():
    query = request.args.get('query', '').lower()
    recommended_ids = recommend_recipe_ids(query)
    results = [food for food in foods if food['id'] in recommended_ids]
    return jsonify(results)

# Route to send the first 10 foods by default
@app.route('/foods', methods=['GET'])
def get_foods():
    return jsonify(foods[:10])

if __name__ == '__main__':
    app.run(debug=True)
