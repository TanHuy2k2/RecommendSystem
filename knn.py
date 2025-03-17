from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from load_food import load_foods
from convert_quantily import convert_quantity
from extract_ingredient import extract_ingredient
import pandas as pd

foods = load_foods()
# Extract relevant information
data = {}
for recipe in foods:
    recipe_id = recipe.get("id")
    ingredients = recipe.get("ingredients", [])

    if recipe_id not in data:
        data[recipe_id] = {"ingredients": []}

    for ingredient in ingredients:
        data[recipe_id]["ingredients"].append(str(ingredient.get("name"))+": "+str(convert_quantity(ingredient.get("quantity"))))

# Convert to DataFrame
df = pd.DataFrame([
    {"id": recipe_id, "ingredients": info["ingredients"]}
    for recipe_id, info in data.items()
])


# Convert the list of ingredients into a single string for each row
df['ingredients_text'] = df['ingredients'].apply(lambda x: ', '.join(x))

# Vectorize the ingredients
vectorizer = TfidfVectorizer()
X_ingredients = vectorizer.fit_transform(df['ingredients_text'])

# Train KNN Model
knn = NearestNeighbors(n_neighbors=10)  # Cosine similarity for text
knn.fit(X_ingredients)

# Function to Recommend Recipes
def recommend_recipes(input_features):
    ingredients, quantities = extract_ingredient(input_features)
    X = []
    for i, j in zip(ingredients, quantities):
      X.append(i+": "+str(j))
    input_ingredients_transformed = vectorizer.transform(X)
    distances, indices = knn.kneighbors(input_ingredients_transformed)
    recommendations = df.iloc[indices[0]]
    return recommendations[['id']]