import streamlit as st
from pymongo import MongoClient
import pandas as pd


def mise_en_forme(curseur):
    """
    fonction qui met en forme les elements d'un cureseur mongodb
    """
    ## Class css
    css_com= "border: solid black 1px;border-radius:30px;margin:0 0 20px 0;padding: 0 15px;"
    flex =  f"{css_com} display : flex;flex-flow: row;"
    flex_reverse = f"{css_com} display : flex;flex-flow: row-reverse; "
    flex_column= "display:flex; flex-flow: column;"
    ## fin class css

    count=0
    for elements in curseur:
        affichage_elt= f"""
        <figure style="width:50%;display:flex;align-item:center;justify-content:center;margin:auto;">
            <img  src="{elements["url"]}">
        </figure>
        <article style="width:50%;{flex_column}">
            <h2>Titre : {elements["titre"]}</h2>
            <p>Date de sortie : {elements["date"]}</p>
            <p>Durée : {elements["duree"]} min</p>
            <p>Genre(s) : {' , '.join(elements["genre"])} </p>
            <p>Acteurs : {' , '.join(elements["acteurs"])}</p>
            <p>Note : {elements["score"]}</p>
            <p>Description:
                <span style="display:block;color:blue;">{elements["descriptions"]}<span>
            </p>
        </article>
        """

        if count%2 == 0:
            html_elt = f"""
            <section class="test" style="{flex}">
                {affichage_elt}
            </section>
            """
        else:
            html_elt = f"""
            <section class="test" style="{flex_reverse}">
                {affichage_elt}
            </section>
            """
        count +=1
        st.markdown(html_elt, unsafe_allow_html=True)

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
with open('style.css') as line:
    st.markdown(f"<style>{line.read()}</style>", unsafe_allow_html=True)

st.sidebar.markdown("# Recherche")

titre_selectbox = st.sidebar.selectbox(
    'Choisi un titre de film :',
    liste_titre)
titre_df= st.sidebar.checkbox('En dataframe',key="titre")
if st.sidebar.button("Selectionner le titre"):
    if titre_df:
        df= pd.DataFrame(list(db_movies.find({"titre":titre_selectbox})))
        df.drop(columns="_id",inplace=True)
        st.dataframe(df)
    else:
        mise_en_forme(db_movies.find({"titre":titre_selectbox}))

genre_selectbox = st.sidebar.selectbox(
    'Choisi un genre de film :',
    liste_genre)
genre_df= st.sidebar.checkbox('En dataframe',key="genre")
if st.sidebar.button("Selectionner le genre"):
    if genre_df:
        df= pd.DataFrame(list(db_movies.find({"genre":genre_selectbox})))
        df.drop(columns="_id",inplace=True)
        st.markdown(f"### Voici les films avec pour genre {genre_selectbox} :")
        st.dataframe(df)
    else:
        st.markdown(f"### Voici les films avec pour genre {genre_selectbox} :")
        mise_en_forme(db_movies.find({"genre":genre_selectbox}))
    



acteur_selectbox = st.sidebar.multiselect(
    'Choisi un ou des acteur(s) :',
    liste_acteur)

dans_le_meme_film= st.sidebar.checkbox('Dans le même film')
acteur_df= st.sidebar.checkbox('En dataframe',key="acteur")
if st.sidebar.button("Selectionner l'acteur"):
    if not dans_le_meme_film:
        try : 
            if acteur_df:
                df= pd.DataFrame(list(db_movies.find({"acteurs":{"$in":acteur_selectbox}})))
                df.drop(columns="_id",inplace=True)
                st.markdown(f"### Voici les films avec l'acteur ou les acteurs {acteur_selectbox} :")
                st.dataframe(df)
            else:
                st.markdown(f"### Voici les films avec l'acteur ou les acteurs {acteur_selectbox} :")
                mise_en_forme(db_movies.find({"acteurs":{"$in":acteur_selectbox}}))
        except:
            st.markdown(f"### Il n'y a pas de films avec l'acteur ou les acteurs {acteur_selectbox} :")
    else:
        try :
            if acteur_df:
                df= pd.DataFrame(list(db_movies.find({"acteurs":{"$all":acteur_selectbox}})))
                df.drop(columns="_id",inplace=True)
                st.markdown(f"### Voici les films avec les acteurs {acteur_selectbox} dans le même film :")
                st.dataframe(df)
            else:
                st.markdown(f"### Voici les films avec l'acteur ou les acteurs {acteur_selectbox} :")
                mise_en_forme(db_movies.find({"acteurs":{"$all":acteur_selectbox}}))
        except:
            st.markdown(f"### Il n'y a pas de films avec l'acteur ou les acteurs {acteur_selectbox} :")


sup_note = st.sidebar.slider('Selectionner une note superieur à:',value=0.0,max_value=10.,min_value=0.,step=0.1,format="%.2f",key="sup_note")
inf_note = st.sidebar.slider('Selectionner une note inferieur à:',value=10.0,max_value=10.,min_value=0.,step=0.1,format="%.2f",key="inf_note")
note_df= st.sidebar.checkbox('En dataframe',key="note")
if st.sidebar.button("Selectionner par note"):
    try:
        if note_df:
            df= pd.DataFrame(list(db_movies.find({"score":{"$gte":sup_note,"$lte":inf_note}})))
            df.drop(columns="_id",inplace=True)
            st.markdown(f"### Voici les films dont la note est superieur à {sup_note} et inferieur à {inf_note} :")
            st.dataframe(df)
        else:
            st.markdown(f"### Voici les films dont la note est superieur à {sup_note} et inferieur à {inf_note} :")
            mise_en_forme(db_movies.find({"score":{"$gte":sup_note,"$lte":inf_note}}))
    except:
        st.markdown(f"### Il n'y a pas de film dont la note est superieur à {sup_note} et inferieur à {inf_note} :")

sup_duree = st.sidebar.slider('Selectionner une note superieur à:',value=0,max_value=1000,min_value=0,step=1,key="sup_duree")
inf_duree = st.sidebar.slider('Selectionner une note inferieur à:',value=1000,max_value=1000,min_value=0,step=1,key="inf_duree")
duree_df= st.sidebar.checkbox('En dataframe',key="duree")
if st.sidebar.button("Selectionner par duree"):
    try:
        if duree_df:
            df= pd.DataFrame(list(db_movies.find({"duree":{"$gte":sup_duree,"$lte":inf_duree}})))
            df.drop(columns="_id",inplace=True)
            st.markdown(f"### Voici les films dont la note est superieur à {sup_duree} et inferieur à {inf_duree} :")
            st.dataframe(df)
        else:
            st.markdown(f"### Voici les films dont la duree est superieur à {sup_duree} et inferieur à {inf_duree} min:")
            mise_en_forme(db_movies.find({"duree":{"$gte":sup_duree,"$lte":inf_duree}}))
    except:
        st.markdown(f"### Il n'y a pas de film dont la duree est superieur à {sup_duree} et inferieur à {inf_duree} min")