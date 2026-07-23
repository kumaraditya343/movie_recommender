import streamlit as st
import pickle 
import pandas as pd
import requests
import time

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# --- Load external CSS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# TMDB API configuration
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=748294e42d4de6ddf4804728577582d3&language=en-US".format(movie_id)
    for attempt in range(3):  # try up to 3 times
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 429:  # TMDB rate limit response
                time.sleep(1)  # wait a bit longer before retrying
                continue
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
            else:
                return "https://placehold.co/500x750?text=No+Poster"  # genuinely no poster
        except requests.exceptions.RequestException:
            time.sleep(1)
    return "https://placehold.co/500x750?text=No+Poster"  # gave up after 3 tries

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    indices = top_indices[movie_index][:5]   # top 5 similar movie indices

    recommended_movies = []
    recommended_movies_posters = []
    for idx in indices:
        recommended_movies.append(movies.iloc[idx].title)
        #fetch posterfrom tmdb api
        recommended_movies_posters.append(fetch_poster(movies.iloc[idx].movie_id))
        time.sleep(0.3)  # small delay to avoid hitting TMDB rate limits
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('model/movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity_data = pickle.load(open('model/similarity_top.pkl','rb'))
top_indices = similarity_data['indices']
top_scores = similarity_data['scores']

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie from the list:', movies['title'].values
)


if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)  # changed from st.beta_columns (removed in current Streamlit)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])