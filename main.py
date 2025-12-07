
import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")


movies = movies.merge(credits, on='title')


movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]


movies.dropna(inplace=True)


def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)


def convert_cast(obj):
    L = []
    for i in ast.literal_eval(obj):
        if len(L) < 3:
            L.append(i['name'])
    return L

movies['cast'] = movies['cast'].apply(convert_cast)


def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

movies['crew'] = movies['crew'].apply(fetch_director)


movies['overview'] = movies['overview'].apply(lambda x: x.split())


movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new_df = movies[['movie_id', 'title', 'tags']]


new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())


cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()


similarity = cosine_similarity(vectors)


def recommend(movie):
    movie = movie.lower()
    if movie not in new_df['title'].str.lower().values:
        return ["Movie not found in database"]
    
    index = new_df[new_df['title'].str.lower() == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    
    for i in distances[1:6]:
        recommended_movies.append(new_df.iloc[i[0]].title)
    return recommended_movies


import pickle
pickle.dump(new_df, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("Data preprocessing complete. Files saved: movies.pkl and similarity.pkl")
