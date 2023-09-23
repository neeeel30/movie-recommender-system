import pickle
import streamlit as st
import requests

# Load movies and similarity data using pickle
def load_data():
    with open(r"C:\Users\NEEL\Desktop\Coding\Anaconda_Data_Science\Projects\Project-3 - Copy\movies.pkl", "rb") as movies_file, open(r"C:\Users\NEEL\Desktop\Coding\Anaconda_Data_Science\Projects\Project-3 - Copy\similarity.pkl", "rb") as similarity_file:
        movies_data = pickle.load(movies_file)
        similarity_data = pickle.load(similarity_file)
    return movies_data, similarity_data

# Fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

# Recommend movies
def recommend_movies(selected_movie, movies, similarity):
    index = movies[movies['title'] == selected_movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.title('Movie Recommender System')

# Load data
movies, similarity = load_data()

# Sidebar
st.sidebar.header('User Input')
selected_movie = st.sidebar.selectbox("Select a Movie", movies['title'].values)

if st.sidebar.button('Get Recommendations'):
    # Get movie recommendations
    recommended_movie_names, recommended_movie_posters = recommend_movies(selected_movie, movies, similarity)

    # Display recommendations in a grid layout
    num_columns = 5
    num_recommendations = len(recommended_movie_names)
    rows = num_recommendations // num_columns + (1 if num_recommendations % num_columns > 0 else 0)

    for i in range(rows):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            idx = i * num_columns + j
            if idx < num_recommendations:
                cols[j].image(recommended_movie_posters[idx], use_column_width=True)
                cols[j].write(recommended_movie_names[idx])
