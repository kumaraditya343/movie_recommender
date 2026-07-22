import streamlit as st
import pickle 
import pandas as pd

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    indices = top_indices[movie_index][:5]   # top 5 similar movie indices

    recommended_movies = []
    for idx in indices:
        recommended_movies.append(movies.iloc[idx].title)
    return recommended_movies

movies_dict = pickle.load(open('model/movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity_data = pickle.load(open('model/similarity_top.pkl','rb'))
top_indices = similarity_data['indices']
top_scores = similarity_data['scores']

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie from the list:', movies['title'].values
)

if st.button('Show Recommendations'):
    recommendations = recommend(selected_movie_name)
    for i in recommendations:
        st.write(i)
    st.write(selected_movie_name)