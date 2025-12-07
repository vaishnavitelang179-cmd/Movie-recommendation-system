Movie Recommendation System

A content-based movie recommendation system built with Python, Streamlit, and scikit-learn.
The app recommends movies similar to a selected title using metadata such as genres, keywords, cast, crew, and plot descriptions.
Movie posters are fetched in real time using the TMDb API.

How It Works

The recommendation engine (see main.py) performs the following:

Loads and merges the TMDb movies and credits datasets

Cleans and extracts relevant metadata fields

Creates a unified tags representation for each movie

Converts text into vectors using CountVectorizer

Computes similarity scores using cosine similarity

Saves movies.pkl and similarity.pkl automatically for fast loading

The Streamlit interface (app.py) lets users pick a movie and view the top 5 recommendations with posters

Dataset

This project uses the TMDb 5000 Movies Dataset from Kaggle:
🔗 https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

Download and place the following files in your project directory:

tmdb_5000_movies.csv

tmdb_5000_credits.csv

Setup & Installation
1. Install dependencies
pip install streamlit pandas numpy scikit-learn requests

2. Run preprocessing to generate .pkl files
python main.py

3. Start the Streamlit app
streamlit run app.py

Project Structure
app.py          
main.py          
movies.pkl       
similarity.pkl   
