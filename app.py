import streamlit as st
import requests
import urllib.parse
import main  # your logic file

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.title("🎥 Movie Recommendation System")


selected_movie = st.selectbox("Select a movie:", main.new_df['title'].values)

def fetch_poster(movie_title):
    api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8'
    query = urllib.parse.quote(movie_title)
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get('results'):
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception as e:
        print("Poster fetch error:", e)

    
    return "https://via.placeholder.com/200x300?text=No+Poster+Found"


if st.button('Recommend'):
    recommendations = main.recommend(selected_movie)
    st.write("### Top 5 Recommended Movies")

    
    cols = st.columns(5)
    for col, movie_title in zip(cols, recommendations):
        poster_url = fetch_poster(movie_title)
        with col:
            st.image(poster_url, width=150)
            st.write(movie_title)
