from flask import Flask, request, jsonify
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

col_names = ['index', 'budget', 'genres', 'homepage', 'id', 'keywords', 'original_language', 'original_title', 'overview', 'popularity', 'production_companies', 'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages', 'status', 'tagline', 'title', 'vote_average', 'vote_count', 'cast', 'crew', 'director']

try:
    import os
    movies_data = pd.read_csv(os.path.join(os.path.dirname(__file__), "data/movies.csv"), header=0, names=col_names)

except Exception as e:
    print(f"Error loading movie data: {e}")
    movies_data = pd.DataFrame()  

def load_data():
    selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']
    for feature in selected_features:
        movies_data[feature] = movies_data[feature].fillna(' ')
    
    comb_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + movies_data['tagline'] + ' ' + movies_data['cast'] + ' ' + movies_data['director']
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(comb_features)
    similarity = cosine_similarity(feature_vectors)
    return similarity

similarity = load_data()

@app.route('/recommend', methods=['GET'])
def recommend_movies():
    movie_name = request.args.get('movie_name')
    
    if not movie_name:
        return jsonify({"error": "No movie name provided"}), 400
    
    list_of_all_titles = movies_data['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
    
    if not find_close_match:
        return jsonify({"error": "Movie not found in the database"}), 404

    close_match = find_close_match[0]
    index = movies_data[movies_data.title == close_match]['index'].values[0]
    similarity_score = list(enumerate(similarity[index]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    recommendations = [movies_data[movies_data.index == movie[0]]['title'].values[0] for movie in sorted_similar_movies[1:11]]
    
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
