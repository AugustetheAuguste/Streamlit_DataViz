# maison_laffite.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
import pydeck as pdk
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static



def app():

    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0px; '>Analyse de la DVF à ML 🏠</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style= 'border-bottom: 5px solid white;margin-bottom: 100px; '</h1>", unsafe_allow_html=True)

    

    @st.cache_data

    def load_data():
        # Charger les données du subset_78 ici, par exemple depuis un fichier CSV
        return pd.read_json('Datasets/subset_specified_all_years.jsonl', lines = True)
    df = load_data()

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
    st.markdown("<div style='font-size: 1.5em;'>Nous allons donc maintenant faire un zoom sur les demandes de valeur foncière pour la ville de maisons Laffitte et ses alentours. Soit avec celle où j'habite et celle d'à côté. Premièrement, on peut voir que vers là où j'habite. Le marché est en train de reprendre de l'ampleur puisqu'il s'est pris un coup pendant le COVID, mais est presque au même niveau qu'en 2019 et a bien dépassé ses niveaux de 2018.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)


    ############################################
    #                   HEATMAP
    ############################################

    selected_year = st.sidebar.slider("Sélectionnez une année:", min_value=2018, max_value=2022)


    # Filtrer le dataframe pour cette année
    df_year = df[df['Year'] == selected_year]

    # Créer une heatmap
    fig = px.density_mapbox(df_year, lat='latitude', lon='longitude', z='Valeur fonciere', radius=30,
                            center=dict(lat=48.91866, lon=2.14072), zoom=12, 
                            mapbox_style="stamen-terrain")
    
    fig.update_layout(height=1000)  # Vous pouvez ajuster la valeur 1000 en fonction de la hauteur souhaitée
    fig.update_layout(title_text="Heatmap de la valeur foncière pour l'année " + str(selected_year), title_x=0.2, title_font=dict(size=36), height=1000)


    
    st.plotly_chart(fig, use_container_width=True)  # Utilisez toute la largeur du conteneur
    
    st.markdown("<div style='font-size: 1.5em;'>Regardons maintenant la Heat Map de la valeur foncière pour l'année 2018. Nous pouvons voir que les demandes de valeur foncière les plus élevées sont aux alentours de Saint-Germain, du Vésinet, de Sartrouville, et de Maisons Laffitte. Ces hotspots évoluent d'année en année, certains endroits reviennent plus souvent que d'autres, indiquant les lieux d'investissements immobiliers intenses. Malheureusement, le Mesnil-le-roi n'en fait rarement partie.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)

    ############################################

    
    # Grouper par latitude, longitude (et potentiellement d'autres colonnes d'adresse) 
    # et compter le nombre de transactions
    df_grouped = df_year.groupby(['latitude', 'longitude', 'No voie', 'Type de voie', 'Voie']).size().reset_index(name='count_transactions')
    
    # Créer une heatmap basée sur le nombre de transactions
    fig = px.density_mapbox(df_grouped, lat='latitude', lon='longitude', z='count_transactions', radius=30,
                            center=dict(lat=48.91866, lon=2.14072), zoom=12, 
                            mapbox_style="carto-positron")
    fig.update_layout(height=1000)  # Vous pouvez ajuster la valeur 800 en fonction de la hauteur souhaitée
    fig.update_layout(title_text="Heatmap du nombre de transactions pour l'année " + str(selected_year), title_x=0.2, title_font=dict(size=36),height=1000)

    
    st.plotly_chart(fig, use_container_width=True)  # Utilisez toute la largeur du conteneur

    st.markdown("<div style='font-size: 1.5em;'>Passons à la Heat Map du nombre de transactions pour les différentes années. On observe une corrélation entre le nombre de transactions et la demande de valeur foncière. Maisons Laffitte, le Vésinet, le Pecq, Sartrouville et Saint Germain en Laye sont des points majeurs de transactions.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)


    ############################################
    #                   HEATMAP
    ############################################

    # Grouper par latitude, longitude (et potentiellement d'autres colonnes d'adresse)
    # et compter le nombre de transactions


    import pydeck as pdk

    # Grouper par latitude, longitude (et potentiellement d'autres colonnes d'adresse)
    # et compter le nombre de transactions
    df_grouped = df_year.groupby(['latitude', 'longitude', 'No voie', 'Type de voie', 'Voie']).size().reset_index(name='count_transactions')

    # Définir la couche de graphiques en barres pour pydeck
    column_layer = pdk.Layer(
        "ColumnLayer",
        data=df_grouped,
        get_position=["longitude", "latitude"],
        get_elevation="count_transactions",
        elevation_scale=25,  # Vous pouvez ajuster cela en fonction de la hauteur souhaitée des barres
        radius=150,  # Rayon des barres, ajustez en fonction de vos préférences
        get_fill_color=[255, 0, 0, 140],  # Couleur des barres
        pickable=True,
        auto_highlight=True
    )

    # Créer la vue avec le centre et le zoom
    view_state = pdk.ViewState(latitude=48.91866, longitude=2.14072, zoom=11, pitch=45,)

    # Créer le deck
    deck = pdk.Deck(
        layers=[column_layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v10",
        tooltip={"text": "Nombre de transactions: {count_transactions}"},  # Info-bulle pour afficher le nombre de transactions lorsque vous survolez une barre
    )

    st.pydeck_chart(deck)



    st.markdown("<div style='font-size: 1.5em;'>Concernant le nombre de transactions par année visualisé via un graphique en barre, nous pouvons identifier des spots majeurs d'investissements immobiliers. </div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)


    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################



    # Définir la couleur basée sur le type de transaction
    df['color'] = df_year['Nature mutation'].map({
        'Vente': [0, 0, 255],
        "Vente en l'état futur d'achèvement": [0, 255, 0],
        'Echange': [255, 0, 0],
        'Adjudication': [128, 0, 128],
        'Vente terrain à bâtir': [255, 255, 0],
        'Expropriation': [255, 165, 0]
    })

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["longitude", "latitude"],
        get_color="color",
        radius_scale=50
    )

    view_state = pdk.ViewState(latitude=48.91866, longitude=2.14072, zoom=11)
    deck = pdk.Deck(layers=[layer], initial_view_state=view_state)

    # Titre centré
    st.markdown("""
        <h2 style="text-align: center;">Titre de votre graphe</h2>
    """, unsafe_allow_html=True)

    # Utilisation de st.columns pour diviser l'écran en deux
    col1, col2 = st.columns(2)

    with col1:
        st.pydeck_chart(deck)

    with col2:
        # Légende manuelle
        st.markdown("""
        <span style="color:blue;">  ⬤</span>   Vente <br>
        <span style="color:green;">  ⬤</span>   Vente en l'état futur d'achèvement <br>
        <span style="color:red;">  ⬤</span>   Echange <br>
        <span style="color:purple;">  ⬤</span>   Adjudication <br>
        <span style="color:yellow;">  ⬤</span>   Vente terrain à bâtir <br>
        <span style="color:orange;">  ⬤</span>   Expropriation
        """, unsafe_allow_html=True)


    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################
    

    # Filtrer les données pour les maisons et dépendances
    df_maison_dependance = df_year[df_year['Type local'].isin(['Maison', 'Dépendance'])]

    # Filtrer les données pour les appartements
    df_appartement = df_year[df_year['Type local'] == 'Appartement']

    # Créer le graphe pour les maisons et dépendances
    layer_maison_dependance = pdk.Layer(
        "ScatterplotLayer",
        data=df_maison_dependance,
        get_position=["longitude", "latitude"],
        get_color=[0, 0, 255],  # bleu
        radius_scale=50
    )
    view_state_maison_dependance = pdk.ViewState(latitude=48.91866, longitude=2.14072, zoom=11)
    deck_maison_dependance = pdk.Deck(layers=[layer_maison_dependance], initial_view_state=view_state_maison_dependance)

    # Créer le graphe pour les appartements
    layer_appartement = pdk.Layer(
        "ScatterplotLayer",
        data=df_appartement,
        get_position=["longitude", "latitude"],
        get_color=[0, 255, 0],  # vert
        radius_scale=50
    )
    view_state_appartement = pdk.ViewState(latitude=48.91866, longitude=2.14072, zoom=11)
    deck_appartement = pdk.Deck(layers=[layer_appartement], initial_view_state=view_state_appartement)

    # Afficher les deux graphes côte à côte
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <h4 style="text-align: center;">Maisons & Dépendances</h4>
        """, unsafe_allow_html=True)
        st.pydeck_chart(deck_maison_dependance)

    with col2:
        st.markdown("""
            <h4 style="text-align: center;">Appartements</h4>
        """, unsafe_allow_html=True)
        st.pydeck_chart(deck_appartement)

    st.markdown("<div style='font-size: 1.5em;'>Ensuite, lorsque nous examinons les ventes, elles sont réparties dans toute la zone choisie, apportant peu d'informations distinctives. La comparaison de la topologie du marché ne montre pas de différence majeure à travers les années.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)

    
    #############################################
    #############################################
#
    ##                   GRAPH
#
    #############################################
    #############################################
    #
    #    
 
    # Titre centré
    st.markdown("""
        <h2 style="text-align: center;">Nombre de Ventes de Maisons par année</h2>
    """, unsafe_allow_html=True)


    # Création d'une carte folium avec une taille spécifiée
    m = folium.Map(location=[48.91866, 2.14072], zoom_start=12)

    # Ajout du MarkerCluster
    marker_cluster = MarkerCluster().add_to(m)

    # Supposons que df contienne les colonnes 'latitude' et 'longitude'
    for idx, row in df_year.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['Nature mutation'],
        ).add_to(marker_cluster)

    # Affichage de la carte dans Streamlit
    folium_static(m)

    
    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################
    


   # Suppression des doublons basée sur la longitude et la latitude
    df_unique = df_year.drop_duplicates(subset=['longitude', 'latitude'])

    # Calcul de la moyenne de la valeur foncière par commune
    df_avg = df_unique.groupby('Commune').agg(
        latitude=('latitude', 'mean'),
        longitude=('longitude', 'mean'),
        valeur_fonciere_avg=('Valeur fonciere', 'mean')
    ).reset_index()


    m = folium.Map(location=[48.91866, 2.14072], zoom_start=12)  # centré sur Paris

    for idx, row in df_avg.iterrows():
        folium.CircleMarker(
            location=(row["latitude"], row["longitude"]),
            radius=row["valeur_fonciere_avg"]/100_000_00,  # Vous pouvez ajuster cette valeur pour modifier la taille des cercles
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.6,
            popup=f"Commune: {row['Commune']}<br>Valeur Foncière Moyenne: {row['valeur_fonciere_avg']:.2f}"
        ).add_to(m)

    # Affichage de la carte dans Streamlit
    folium_static(m)

    st.markdown("<div style='font-size: 1.5em;'>En analysant les graphes axés sur les transactions et la valeur foncière par commune, Sartrouville, Houilles, et le Vésinet sont fréquemment mentionnés comme points chauds. Le Mesnil-Le-roi, ma commune, se situe en 4e ou 5e position sur 8 communes en termes de valeur foncière moyenne.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)


    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    # Filtre pour chaque scénario
    df1 = df[(df['Nature mutation'] == 'Vente') & (df['Type local'] == 'Maison') & (df['Nombre pieces principales'] >= 5)]
    df3 = df[(df['Type local'] == 'Maison') & (df['Surface reelle bati'] >= 170) & (df['Surface reelle bati'] <= 210)]
    df4 = df[(df['Type local'] == 'Maison') & (df['Surface terrain'] >= 480) & (df['Surface terrain'] <= 520)]

    # Fonction pour créer le HexagonLayer
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
            radius=100,
            get_elevation="Valeur fonciere",
            get_fill_color="[255, (1 - elevationValue / 50) * 255, 255]",
            # Ajouter tooltips ici
            tooltips=[
                {"html": "<b>Somme Valeur Foncière:</b> {elevationValue}", "style": {"backgroundColor": "steelblue", "color": "white"}}
            ]
        )
        return hexagon_layer
    # Créer les cartes
    view_state = pdk.ViewState(latitude=48.91866, longitude=2.14072, zoom=11, pitch=45)

    # Carte 1
    st.markdown("## Heatmap des maisons avec 5 ou plus pièces principales")  # Le titre est ajouté ici
    deck1 = pdk.Deck(layers=[create_hexagon_layer(df1)], initial_view_state=view_state)
    st.pydeck_chart(deck1, use_container_width=True)

    # Carte 3
    st.markdown("## Heatmap des maisons avec une surface réelle bâtie entre 170 et 210 m²")
    deck3 = pdk.Deck(layers=[create_hexagon_layer(df3)], initial_view_state=view_state)
    st.pydeck_chart(deck3, use_container_width=True)

    # Carte 4
    st.markdown("## Heatmap des maisons avec une surface de terrain autour de 500 m²")
    deck4 = pdk.Deck(layers=[create_hexagon_layer(df4)], initial_view_state=view_state)
    st.pydeck_chart(deck4, use_container_width=True)

    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    # Maisons avec 5 pièces principales
    maisons_5_pieces = df.loc[(df['Type local'] == 'Maison') & (df['Nombre pieces principales'] == 5)].shape[0]

    # Maisons avec une surface bâtie de 150m²
    maisons_surface_150 = df.loc[(df['Type local'] == 'Maison') & (df['Surface reelle bati'] == 190)].shape[0]

    # Maisons avec 500m² de terrain
    maisons_terrain_500 = df.loc[(df['Type local'] == 'Maison') & (df['Surface terrain'] == 500)].shape[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Utilisez du HTML pour augmenter la taille du texte et ajouter des emojis
        st.markdown("<h2 style='text-align: center; color: white;'>Maisons avec 5 pièces principales</h2>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; color: white;'>🏡 {maisons_5_pieces}</h2>", unsafe_allow_html=True)
        

    with col2:
        st.markdown("<h2 style='text-align: center; color: white;'>Maisons avec une surface bâtie de 159m²</h2>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; color: white;'>📏 {maisons_surface_150}</h2>", unsafe_allow_html=True)
        

    with col3:
        st.markdown("<h2 style='text-align: center; color: white;'>Maisons avec 500m² de terrain</h2>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; color: white;'>🌳 {maisons_terrain_500}</h2>", unsafe_allow_html=True)
        

    # Filtrage des maisons selon les critères donnés
    maisons_filtrees_df = df.loc[
        (df['Type local'] == 'Maison') &
        (df['Nombre pieces principales'] == 5) &
        (df['Surface reelle bati'] >= 170) &
        (df['Surface reelle bati'] <= 210) &
        (df['Surface terrain'] >= 450) &
        (df['Surface terrain'] <= 490)
    ].shape[0]

    with col4:
        # Affichage de la métrique des maisons filtrées avec du HTML pour la taille et l'emoji
        st.markdown("<h2 style='text-align: center; color: white;'>Maisons qui correspond à tout les critères</h2>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; color: white;'>🔍 {maisons_filtrees_df}</h2>", unsafe_allow_html=True)
        
    


    # Filtrage des maisons selon les critères donnés
    maisons_filtrees_df = df.loc[
        (df['Type local'] == 'Maison') &
        (df['Nombre pieces principales'] == 5) &
        (df['Surface reelle bati'] >= 170) &
        (df['Surface reelle bati'] <= 210) &
        (df['Surface terrain'] >= 450) &
        (df['Surface terrain'] <= 490)
    ]

    # Mise en page avec 2 colonnes : la première pour la carte et la seconde pour les noms des communes
    col1, col2 = st.columns(2)

    # Dans la première colonne : Affichage de la carte
    with col1:
        # Création d'une carte centrée sur la moyenne des latitudes et longitudes des maisons filtrées
        m = folium.Map(location=[maisons_filtrees_df['latitude'].mean(), 
                                 maisons_filtrees_df['longitude'].mean()], 
                       zoom_start=12)

        # Ajout de marqueurs pour chaque maison
        for _, row in maisons_filtrees_df.iterrows():
            tooltip = f"Commune: {row['Commune']}"
            popup = f"Valeur foncière: {row['Valeur fonciere']} €"
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                tooltip=tooltip,
                popup=popup
            ).add_to(m)

        # Affichage de la carte dans Streamlit
        folium_static(m)

    # Dans la deuxième colonne : Affichage des noms des communes
    with col2:
        # Utiliser du HTML pour centrer le texte, le rendre plus grand et ajouter un emoji
        st.markdown(f"<h2 style='text-align: center; color: white;'>🏡 Communes avec des maisons répondant aux critères :</h2>", unsafe_allow_html=True)

        # Affichage des noms des communes avec une taille de texte plus grande
        for commune in maisons_filtrees_df['Commune'].unique():
            st.markdown(f"<h3 style='color: white;'>{commune}</h3>", unsafe_allow_html=True)





    st.markdown("<div style='font-size: 1.5em;'>Nous examinons ensuite des Heat Maps spécifiques pour les demandes de maisons, basées sur des caractéristiques concrètes. En analysant ces données, il est évident que nous n'avons pas acquis de maison dans le marché le plus dynamique. Cependant, notre maison a des caractéristiques recherchées dans des communes plus aisées. Ceci pourrait signifier que nous possédons une propriété attrayante pour des acheteurs prêts à payer davantage, située dans une commune où les prix sont généralement plus bas.</div>", unsafe_allow_html=True)





