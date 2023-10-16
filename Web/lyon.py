# lyon.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
import pydeck as pdk
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import seaborn as sns
import bar_chart_race as bcr

def app():

    # Grand titre stylisé
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0px; '>Analyse de la DVF à Lyon 🦁</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style= 'border-bottom: 5px solid white;margin-bottom: 100px; '</h1>", unsafe_allow_html=True)


    @st.cache_data

    def load_data():
        # Charger les données du subset_78 ici, par exemple depuis un fichier CSV
        return pd.read_json('Datasets/finished_subset_lyon_surrounding_all_years.jsonl', lines = True)
    df = load_data()
    df = df.dropna(subset=['latitude', 'longitude'])

    selected_year = st.sidebar.slider("Sélectionnez une année:", min_value=2018, max_value=2022)



    # Filtrer le dataframe pour cette année
    df_year = df[df['Year'] == selected_year]

    # Calculer le nombre total de mutations
    total_mutations = df.shape[0]

    # Calculer le nombre de mutations par an
    mutations_by_year = df['Year'].value_counts().sort_index()

    st.markdown(
        f"""
        <div style='text-align: center; margin-bottom: 20px;'>
            <h2>Nombre total de mutations:</h2>
            <h1><span>{total_mutations}</span></h1>
        </div>
        """,
        unsafe_allow_html=True,
    )



    
    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################



    # Afficher une métrique pour chaque année
    years_to_display = [2018, 2019, 2020, 2021, 2022]
    # Créer des colonnes pour les métriques annuelles et les variations
    cols = st.columns(len(years_to_display))

    # Afficher une métrique pour chaque année
    years_to_display = [2018, 2019, 2020, 2021, 2022]

    # Calculer les mutations par année
    mutations_by_year = df.groupby('Year').size()

    for i, year in enumerate(years_to_display):
        with cols[i]:
            # Afficher les mutations pour l'année courante
            if year in mutations_by_year.index:
                st.metric(label=f"Mutations en {year}", value=mutations_by_year[year])
            else:
                st.metric(label=f"Mutations en {year}", value=0)

            # Afficher les variations si on n'est pas à la première année
            if i != 0:
                prev_year = years_to_display[i - 1]
                if prev_year in mutations_by_year.index and year in mutations_by_year.index:
                    change = int(mutations_by_year[year] - mutations_by_year[prev_year])
                    percentage_change = (change / mutations_by_year[prev_year]) * 100

                    # Sélectionnez une flèche et une couleur en fonction de la direction du changement
                    if change >= 0:
                        arrow = "↑"
                        color = "green"
                    else:
                        arrow = "↓"
                        color = "red"

                    st.markdown(
                        f"Changement de {prev_year} à {year}: <span style='font-size:48px; color: {color};'>{arrow}</span> "
                        f"{abs(percentage_change):.2f}% ({change})", 
                        unsafe_allow_html=True
                    )

                    st.write("---")  # Ligne de séparation

    
    st.markdown("<div style='font-size: 1.5em;'>Maintenant, nous allons passer à l'analyse de la demande de valeur foncière à Lyon. Car en effet, nous devons nous demander où c'est que on va déménager ? À Lyon. Le marché de l'immobilier est bien différent puisqu'il est en plein essor. Il n'a baissé que de 5,64% pendant le COVID mais est en train de continuellement progresser. Il stagne autour des 15000 nombres de mutations par an, augmentant donc de 4000 par rapport à 2018.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)

    ############################################
    ############################################

    #           Où sont les endroits où il y a le plus de vente?

    ############################################
    ############################################

    st.header("Endroits avec le plus de ventes")
    
    # Créer une carte centrée autour de Lyon
    m = folium.Map(location=[45.75, 4.85], zoom_start=12)
    
    # Utilisation de MarkerCluster pour regrouper les ventes proches les unes des autres
    marker_cluster = MarkerCluster().add_to(m)

    # Ajouter des points pour chaque vente
    for idx, row in df.iterrows():
        folium.Marker([row['latitude'], row['longitude']]).add_to(marker_cluster)

    # Afficher la carte
    folium_static(m)

     ############################################
    ############################################

    #           Où sont les endroits où les maisons sont les moins chères?

    ############################################
    ############################################

    st.header("Endroits où les maisons sont les moins chères")
    
    # Filtrer pour ne sélectionner que les maisons et exclure les rangées avec des NaNs dans 'latitude' ou 'longitude'
    df_houses = df[df['Type local'] == 'Maison'].dropna(subset=['latitude', 'longitude'])
    
    # Trier le dataframe par 'Valeur fonciere' et prendre les 100 premiers
    df_cheapest = df_houses.sort_values(by="Valeur fonciere", ascending=True).head(100)

    m_cheapest = folium.Map(location=[45.75, 4.85], zoom_start=12)

    for idx, row in df_cheapest.iterrows():
        folium.Marker(
            [row['latitude'], row['longitude']], 
            popup=f"{row['Valeur fonciere']}€",
            icon=folium.Icon(color="green")
        ).add_to(m_cheapest)

    folium_static(m_cheapest)

    ############################################
    ############################################

    #           Où sont les endroits où les maisons sont les plus chères?

    ############################################
    ############################################

    st.header("Endroits où les maisons sont les plus chères")
    
    # Trier le dataframe par 'Valeur fonciere' pour les maisons et prendre les 100 plus chers
    df_expensive = df_houses.sort_values(by="Valeur fonciere", ascending=False).head(100)

    m_expensive = folium.Map(location=[45.75, 4.85], zoom_start=12)

    for idx, row in df_expensive.iterrows():
        folium.Marker(
            [row['latitude'], row['longitude']], 
            popup=f"{row['Valeur fonciere']}€",
            icon=folium.Icon(color="red")
        ).add_to(m_expensive)

    folium_static(m_expensive)



    st.markdown("<div style='font-size: 1.5em;'>Avec les 3 graphes suivants, nous allons essayer de regarder où c'est qu'il y a le plus de ventes à Lyon et ses alentours et où se trouvent les maisons les moins chères et les maisons les plus chères. Ces 3 graphes, bien qu'ils nous apportent des informations sur le fait que le centre de Lyon est l'endroit où il y a le plus de ventes, que les maisons les moins chères se trouvent au nord de Lyon, et que les maisons les plus chères se trouvent vers Lyon Centre et sa périphérie, ne nous permettent pas de voir clairement ce que cela représente. C'est pourquoi nous devons en faire plus.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)


    ############################################
    ############################################

    #           Heatmap du nombre de ventes

    ############################################
    ############################################

    st.header("Heatmap du nombre de ventes")

    # Groupez les données par latitude et longitude et comptez le nombre de ventes pour chaque paire unique
    df_sales_count = df_year.groupby(['latitude', 'longitude']).size().reset_index(name='counts')

    view_state = pdk.ViewState(
        latitude=45.75,
        longitude=4.85,
        zoom=10,
        pitch=0
    )

    heatmap_layer_sales = pdk.Layer(
        "HeatmapLayer",
        df_sales_count,
        get_position=["longitude", "latitude"],
        get_weight="counts",
        radius_pixels=50
    )

    map_sales = pdk.Deck(layers=[heatmap_layer_sales], initial_view_state=view_state)

    st.pydeck_chart(map_sales)


    ############################################
    ############################################

    #           Heatmap du de la valeur foncière

    ############################################
    ############################################

    st.header("Heatmap de la valeur foncière")

    # Groupez les données par latitude et longitude et sommez la valeur foncière pour chaque paire unique
    df_fonciere_sum = df.groupby(['latitude', 'longitude'])['Valeur fonciere'].sum().reset_index(name='sum_fonciere')

    view_state = pdk.ViewState(
        latitude=45.75,
        longitude=4.85,
        zoom=10,
        pitch=0
    )

    heatmap_layer_fonciere = pdk.Layer(
        "HeatmapLayer",
        df_fonciere_sum,
        get_position=["longitude", "latitude"],
        get_weight="sum_fonciere",
        radius_pixels=50
    )

    map_fonciere = pdk.Deck(layers=[heatmap_layer_fonciere], initial_view_state=view_state)

    st.pydeck_chart(map_fonciere)

    st.markdown("<div style='font-size: 1.5em;'>Avec les 2 heatmaps suivants, nous pouvons identifier les endroits avec le plus de ventes grâce au heatmap du nombre de ventes et les endroits avec le plus de valeur foncière grâce au heatmap de la valeur foncière. À partir de ces données, nous cherchons une maison avec 5 pièces principales ou plus, une surface réelle bâtie d'environ 150 m² et un terrain d'environ 500 m². Nous utilisons alors des heatmaps hexagonales pour repérer les zones avec le plus de ce type de maison. Une zone se démarque particulièrement : le nord de Lyon. Nous allons donc explorer les communes les plus intéressantes pour nous dans cette zone.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)


     ############################################
    ############################################

    #      Haxagonal chart

    ############################################
    ############################################




    def create_hexagon_layer(dataframe):
        hexagon_layer = pdk.Layer(
            "HexagonLayer",
            dataframe,
            get_position=["longitude", "latitude"],
            auto_highlight=True,
            elevation_scale=2,
            pickable=True,
            elevation_range=[0, 3000],
            extruded=True,
            coverage=0.7,
            radius=1000,
            get_elevation="Valeur fonciere",
            get_fill_color="[255, (1 - elevationValue / 50) * 255, 255, 128]",  # Ajout de 128 pour l'alpha
            # Ajouter tooltips ici
            tooltips=[
                {"html": "<b>Somme Valeur Foncière:</b> {elevationValue}", "style": {"backgroundColor": "steelblue", "color": "white"}}
            ]
        )
        return hexagon_layer
    

    df1  = df[(df['Type local'] == 'Maison') & (df['Nombre pieces principales'] >= 5)]
    df2  = df[(df['Type local'] == 'Maison') & (df['Surface reelle bati'] >= 130) & (df['Surface reelle bati'] <= 170)]
    df3  = df[(df['Type local'] == 'Maison') & (df['Surface terrain'] >= 400) & (df['Surface terrain'] <= 600)]

    df4 =  df[(df['Type local'] == 'Maison') 
              & (df['Nombre pieces principales'] >= 5)
              & (df['Surface reelle bati'] >= 130) 
              & (df['Surface reelle bati'] <= 170)
              & (df['Surface terrain'] >= 400)
              & (df['Surface terrain'] <= 600)]

 # Combinaison des trois critères

    view_state = pdk.ViewState(
           latitude=45.75,
           longitude=4.85,
           zoom=10,
           pitch=45
       )

    # Carte 1
    st.markdown("## Heatmap des maisons avec 5 pièces principales ou plus")
    deck1 = pdk.Deck(layers=[create_hexagon_layer(df1)], initial_view_state=view_state)
    st.pydeck_chart(deck1, use_container_width=True)

    # Carte 2
    st.markdown("## Heatmap des maisons avec une surface réelle bâtie entre 130 et 170 m²")
    deck2 = pdk.Deck(layers=[create_hexagon_layer(df2)], initial_view_state=view_state)
    st.pydeck_chart(deck2, use_container_width=True)

    # Carte 3
    st.markdown("## Heatmap des maisons avec une surface de terrain entre 400 et 600 m²")
    deck3 = pdk.Deck(layers=[create_hexagon_layer(df3)], initial_view_state=view_state)
    st.pydeck_chart(deck3, use_container_width=True)

    # Carte 4
    st.markdown("## Heatmap des maisons qui combinent les trois critères")
    deck4 = pdk.Deck(layers=[create_hexagon_layer(df4)], initial_view_state=view_state)
    st.pydeck_chart(deck4, use_container_width=True)


    # Mise en page avec 2 colonnes : la première pour la carte et la seconde pour les metrics des communes

    # Dans la première colonne : Affichage de la carte
    
    # Création d'une carte centrée sur la moyenne des latitudes et longitudes des maisons filtrées
    m = folium.Map(location=[df4['latitude'].mean(), 
                             df4['longitude'].mean()], 
                   zoom_start=12)

    # Ajout de marqueurs pour chaque maison
    for _, row in df4.iterrows():
        tooltip = f"Commune: {row['Commune']}"
        popup = f"Valeur foncière: {row['Valeur fonciere']} €"
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            tooltip=tooltip,
            popup=popup
        ).add_to(m)

    # Affichage de la carte dans Streamlit
    folium_static(m)

    # Dans la deuxième colonne : Affichage des metrics des communes

    st.markdown(f"<h2 style='text-align: center;'>🏡 Metrics des communes :</h2>", unsafe_allow_html=True)
    # Calcul du nombre de maisons par commune
    # Calcul du nombre de maisons par commune et sélection des 5 premières communes avec le plus de maisons
    communes_counts = df4['Commune'].value_counts()
    
    # Utilisation de colonnes pour afficher les metrics en ligne
    cols = st.columns(5)  # Ajustez le nombre en fonction de combien vous voulez afficher sur une ligne
    
    for index, (commune, count) in enumerate(communes_counts.items()):
        if index != 5:
            with cols[index]:
                # Affichage du metric pour chaque commune
                st.metric(label=f"{commune}", value=f"{count} maisons")
        else:
            break


    st.markdown("<div style='font-size: 1.5em;'>Parmi ces communes, nous retrouvons Saint-Genis-Laval, Écully, Caluire-et-Cuire, Rillieux-le-Pape, entre autres. Ceci n'est que le top 5 parmi de nombreuses autres communes. En conclusion, si nous envisageons de déménager, Lyon semble être un excellent choix vu l'essor du marché immobilier local. Il serait néanmoins judicieux d'examiner plus en détail les différents heatmaps du nombre de ventes et de la valeur foncière pour choisir le lieu idéal. Nous avons désormais une liste de communes potentiellement intéressantes pour nous.</div>", unsafe_allow_html=True)


