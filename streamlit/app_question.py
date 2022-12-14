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
list_movies = db_movies.find()
for movie in list_movies:
    genre_movie = movie["genre"]
    for genre in genre_movie:
        if not genre in liste_genre:
            liste_genre.append(genre)

list_movies = db_movies.find()

liste_acteur = []
for movie in list_movies:
    acteur_movie = movie["acteurs"]
    for acteur in acteur_movie:
        if not acteur in liste_acteur:
            liste_acteur.append(acteur)

df= pd.DataFrame(list(db_movies.find()))
df.drop(columns="_id",inplace=True)




## Creation de l'app
st.markdown("# Questions")
st.markdown("## Voici le film le plus long du top 250 d'imdb")
df= pd.DataFrame(list(db_movies.find().sort("duree",-1).limit(1)))
df.drop(columns="_id",inplace=True)
st.dataframe(df)

st.markdown("## Voici les 5 films les mieux notés du top 250 d'imdb")
df= pd.DataFrame(list(db_movies.find().sort("score",-1).limit(5)))
df.drop(columns="_id",inplace=True)
st.dataframe(df)

st.markdown("## Voici les films dans lequel Morgan Freeman a joué qui sont dans le top 250 d'imdb")
df= pd.DataFrame(list(db_movies.find({"acteurs":{"$in":["Morgan Freeman"]}})))
df.drop(columns="_id",inplace=True)
st.dataframe(df)

st.markdown("## Voici les films dans lequel Tom Cruise a joué qui sont dans le top 250 d'imdb")
df= pd.DataFrame(list(db_movies.find({"acteurs":{"$in":["Tom Cruise"]}})))
df.drop(columns="_id",inplace=True)
st.dataframe(df)

st.markdown("## Voici les 3 meilleurs films d’horreur du top 250 d'imdb")
df= pd.DataFrame(list(db_movies.find({"genre":{"$in":["Horror"]}}).sort("score",-1).limit(3)))
df.drop(columns="_id",inplace=True)
st.dataframe(df)

st.markdown("## Voici les 3 meilleurs films dramatique du top 250 d'imdb")
df= pd.DataFrame(list(db_movies.find({"genre":{"$in":["Drama"]}}).sort("score",-1).limit(3)))
df.drop(columns="_id",inplace=True)
st.dataframe(df)

st.markdown("## Voici les 3 meilleurs films Comique du top 250 d'imdb")
df= pd.DataFrame(list(db_movies.find({"genre":{"$in":["Comedy"]}}).sort("score",-1).limit(3)))
df.drop(columns="_id",inplace=True)
st.dataframe(df)

top_100 = db_movies.find().sort("score", -1)[:100]
france = 0
us = 0
for i in top_100:
    if "France" in i['pays']  :
        france += 1
    elif "United States" in i['pays'] :
        us += 1

st.markdown(f"### Parmi les 100 films les mieux notés du top 250 d'imdb il y {us} % de film américains")
st.markdown(f"### Parmi les 100 films les mieux notés du top 250 d'imdb il y {france} % de film français")


dict_temps_genre={}
for genre in liste_genre:
    temps_total = 0
    list_movies = db_movies.find({"genre":{"$in":[genre]}})
    nb_movies=db_movies.count_documents({"genre":{"$in":[genre]}})
    
    for movie in list_movies:
        temps_total = movie["duree"] + temps_total

    dict_temps_genre[genre] =  temps_total/nb_movies

st.markdown(f"## La duree moyennne selon le genre ")
duree_par_genre = st.selectbox(
    'Choisi un genre de film :',
    liste_genre,key="duree_par_genre")

if st.button("valider le genre"):
    st.markdown(f"La duree moyennne des films du genre {duree_par_genre} est {round(dict_temps_genre[duree_par_genre],2)} min ")
