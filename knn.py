from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from load_food import load_foods
import pandas as pd

foods = load_foods()

df_main = pd.DataFrame(foods)
df_main.head()

df = df_main[["recipe_id", "ingredients"]]

df['ingredients'] = df['ingredients'].apply(lambda x: ', '.join(x))


# Sử dụng TfidfVectorizer để chuyển đổi nguyên liệu thành đặc trưng
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['ingredients'])

# Tạo mô hình Nearest Neighbors
knn = NearestNeighbors(n_neighbors=5, metric='cosine')
knn.fit(X)

# Hàm dự đoán món ăn dựa trên nguyên liệu nhập vào
def predict_recipe(input_ingredients):
    input_vector = vectorizer.transform([input_ingredients])
    distance, indices = knn.kneighbors(input_vector)
    recommendations = df_main.iloc[indices[0]]
    return recommendations[['recipe_id']]