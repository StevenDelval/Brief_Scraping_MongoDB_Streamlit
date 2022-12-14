import streamlit as st
from pymongo import MongoClient
import pandas as pd

## connection Mongodb
client = MongoClient("localhost:27017")
database = client.scrapy
db_movies = database.movies
db_serie = database.serie



## Creation des liste d'acteur et de genre de film
liste_genre =[]
liste_acteur = []
liste_titre = []
for movie in db_movies.find():
    genre_movie = movie["genre"]
    acteur_movie = movie["acteurs"]
    if not movie["titre"] in liste_titre:
            liste_titre.append(movie["titre"])
    for genre in genre_movie:
        if not genre in liste_genre:
            liste_genre.append(genre)
    for acteur in acteur_movie:
        if not acteur in liste_acteur:
            liste_acteur.append(acteur)
    

    



## Creation de l'app
st.sidebar.markdown("# Recherche")

titre_selectbox = st.sidebar.selectbox(
    'Choisi un titre de film :',
    liste_titre)
if st.sidebar.button("Selectionner le titre"):
    df= pd.DataFrame(list(db_movies.find({"titre":titre_selectbox})))
    df.drop(columns="_id",inplace=True)
    st.dataframe(df)

genre_selectbox = st.sidebar.selectbox(
    'Choisi un genre de film :',
    liste_genre)
if st.sidebar.button("Selectionner le genre"):
    df= pd.DataFrame(list(db_movies.find({"genre":genre_selectbox})))
    df.drop(columns="_id",inplace=True)
    st.markdown(f"### Voici les films avec pour genre {genre_selectbox} :")
    st.dataframe(df)
    



acteur_selectbox = st.sidebar.multiselect(
    'Choisi un ou des acteur(s) :',
    liste_acteur)

dans_le_meme_film= st.sidebar.checkbox('Dans le même film ?')
if st.sidebar.button("Selectionner l'acteur"):
    if not dans_le_meme_film:
        try : 
            df= pd.DataFrame(list(db_movies.find({"acteurs":{"$in":acteur_selectbox}})))
            df.drop(columns="_id",inplace=True)
            st.markdown(f"### Voici les films avec l'acteur ou les acteurs {acteur_selectbox} :")
            st.dataframe(df)
        except:
            st.markdown(f"### Il n'y a pas de films avec l'acteur ou les acteurs {acteur_selectbox} :")
    else:
        try : 
            df= pd.DataFrame(list(db_movies.find({"acteurs":{"$all":acteur_selectbox}})))
            df.drop(columns="_id",inplace=True)
            st.markdown(f"### Voici les films avec les acteurs {acteur_selectbox} dans le même film :")
            st.dataframe(df)
        except:
            st.markdown(f"### Il n'y a pas de films avec l'acteur ou les acteurs {acteur_selectbox} :")


sup_note = st.sidebar.slider('Selectionner une note superieur à:',value=0.0,max_value=10.,min_value=0.,step=0.1,format="%.2f",key="sup_note")
inf_note = st.sidebar.slider('Selectionner une note inferieur à:',value=10.0,max_value=10.,min_value=0.,step=0.1,format="%.2f",key="inf_note")
if st.sidebar.button("Selectionner par note"):
    try:
        df= pd.DataFrame(list(db_movies.find({"score":{"$gte":sup_note,"$lte":inf_note}})))
        df.drop(columns="_id",inplace=True)
        st.markdown(f"### Voici les films dont la note est superieur à {sup_note} et inferieur à {inf_note} :")
        st.dataframe(df)
    except:
        st.markdown(f"### Il n'y a pas de film dont la note est superieur à {sup_note} et inferieur à {inf_note} :")
   