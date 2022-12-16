import streamlit as st
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

def mise_en_forme(curseur):
    """
    fonction qui met en forme les elements d'un cureseur mongodb
    """
    ## Class css
    css_com= "border: dashed black 1px;border-radius:30px;margin:0 0 20px 0;padding: 0 15px;"
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
database = client.scrapyPipeline
db_movies = database.movies



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
tab1,tab2 = st.tabs(["Question","Recherche"])

with tab1:
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
    dict_mean = {"France":france,"United States":us,"Autre":100-france-us}
    fig= plt.figure()
    ax = fig.add_axes([0,0,2,2])
    ax.set_title("Pays des 100 films les mieux notés du top 250 d'imdb")
    names = list(dict_mean.keys())
    values = list(dict_mean.values())
    ax.pie(values,labels=names,autopct= '%1.0f%%')
    st.pyplot(fig)
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
    fig, ax = plt.subplots()
    names = list(dict_temps_genre.keys())
    values = list(dict_temps_genre.values())
    ax.bar(range(len(dict_temps_genre)), values, tick_label=names)
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)
    st.pyplot(fig)

    duree_par_genre = st.selectbox(
        'Choisi un genre de film :',
        liste_genre,key="duree_par_genre")

    if st.button("valider le genre"):
        st.markdown(f"La duree moyennne des films du genre {duree_par_genre} est {round(dict_temps_genre[duree_par_genre],2)} min ")





with tab2:
    with open('style.css') as line:
        st.markdown(f"<style>{line.read()}</style>", unsafe_allow_html=True)

    st.sidebar.markdown("# Recherche")

    titre_selectbox = st.sidebar.multiselect(
        'Choisi un titre de film :',
        liste_titre)
    titre_df= st.sidebar.checkbox('En dataframe',key="titre")
    if st.sidebar.button("Selectionner le titre"):
        if titre_df:
            df= pd.DataFrame(list(db_movies.find({"titre":{"$in":titre_selectbox}})))
            df.drop(columns="_id",inplace=True)
            st.dataframe(df)
        else:
            mise_en_forme(db_movies.find({"titre":{"$in":titre_selectbox}}))

    genre_selectbox = st.sidebar.multiselect(
        'Choisi un genre de film :',
        liste_genre)
    genre_df= st.sidebar.checkbox('En dataframe',key="genre")
    pour_le_meme_film= st.sidebar.checkbox('Les films avec exactement ces genres')
    if st.sidebar.button("Selectionner le genre"):
        if not pour_le_meme_film:
            try : 
                if genre_df:
                    df= pd.DataFrame(list(db_movies.find({"genre":{"$in":genre_selectbox}})))
                    df.drop(columns="_id",inplace=True)
                    st.markdown(f"### Voici les films avec pour le ou les genre(s) {' , '.join(genre_selectbox)} :")
                    st.dataframe(df)
                else:
                    st.markdown(f"### Voici les films avec pour le ou les genre(s) {' , '.join(genre_selectbox)} :")
                    mise_en_forme(db_movies.find({"genre":{"$in":genre_selectbox}}))
            except:
                st.markdown(f"### Il n'y a pas de films avec les genres {' , '.join(genre_selectbox)} :")
        else:
            try :
                if genre_df:
                    df= pd.DataFrame(list(db_movies.find({"genre":{"$all":genre_selectbox}})))
                    df.drop(columns="_id",inplace=True)
                    st.markdown(f"### Voici les films avec pour le ou les genres {' , '.join(genre_selectbox)} :")
                    st.dataframe(df)
                else:
                    st.markdown(f"### Voici les films avec pour le ou les genre(s) {' , '.join(genre_selectbox)} :")
                    mise_en_forme(db_movies.find({"genre":{"$all":genre_selectbox}}))
            except:
                st.markdown(f"### Il n'y a pas de films avec les genre(s) {' , '.join(genre_selectbox)} :")
        
        



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
                    st.markdown(f"### Voici les films avec l'acteur ou les acteurs {' , '.join(acteur_selectbox)} :")
                    st.dataframe(df)
                else:
                    st.markdown(f"### Voici les films avec l'acteur ou les acteurs {' , '.join(acteur_selectbox)} :")
                    mise_en_forme(db_movies.find({"acteurs":{"$in":acteur_selectbox}}))
            except:
                st.markdown(f"### Il n'y a pas de films avec l'acteur ou les acteurs {' , '.join(acteur_selectbox)} :")
        else:
            try :
                if acteur_df:
                    df= pd.DataFrame(list(db_movies.find({"acteurs":{"$all":acteur_selectbox}})))
                    df.drop(columns="_id",inplace=True)
                    st.markdown(f"### Voici les films avec les acteurs {' , '.join(acteur_selectbox)} dans le même film :")
                    st.dataframe(df)
                else:
                    st.markdown(f"### Voici les films avec l'acteur ou les acteurs {' , '.join(acteur_selectbox)} :")
                    mise_en_forme(db_movies.find({"acteurs":{"$all":acteur_selectbox}}))
            except:
                st.markdown(f"### Il n'y a pas de films avec l'acteur ou les acteurs {' , '.join(acteur_selectbox)} :")


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

    sup_duree = st.sidebar.slider('Selectionner une duree superieur à:',value=0,max_value=300,min_value=0,step=1,key="sup_duree")
    inf_duree = st.sidebar.slider('Selectionner une duree inferieur à:',value=300,max_value=300,min_value=0,step=1,key="inf_duree")
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
    

    