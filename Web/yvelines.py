# yvelines.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import folium
from folium.plugins import FastMarkerCluster
import seaborn as sns
import bar_chart_race as bcr


def app():
    # Grand titre stylisé
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0px; '>Analyse de la DVF dans les Yvelines 🌲</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style= 'border-bottom: 5px solid white;margin-bottom: 100px; '</h1>", unsafe_allow_html=True)
    

    @st.cache_data

    def load_data():
        # Charger les données du subset_78 ici, par exemple depuis un fichier CSV
        return pd.read_json('Datasets/subset_78_all_years.jsonl', lines = True)
    df = load_data()

    

    selected_year = st.sidebar.slider("Sélectionnez une année:", min_value=2018, max_value=2022)


    # Filtrer le dataframe pour cette année
    df_year = df[df['Year'] == selected_year]

  
    # Agencement
    st.title("Analyse des mutations immobilières")

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



        # Ajout d'une ligne blanche avec une marge
    st.markdown("<h3 style= 'border-bottom: 2px solid white;margin-bottom: 20px; '</h3>", unsafe_allow_html=True)
    # Ajout de votre texte en relativement gros
    st.markdown("<div style='font-size: 1.5em;'>Nous pouvons constater, grâce à ces indicateurs, que le marché de l'immobilier dans les Yvelines est passé de 19 966 mutations en 2018 à 12 206 en 2020, puis a rebondi à 15 100 en 2022. Cela démontre qu'à Yvelines, le marché immobilier se remet de la crise du COVID. Néanmoins, il ne s'agit pas d'un marché en croissance constante. En effet, il a connu une baisse de 5,32% en 2022 par rapport à 2021, et n'a jamais retrouvé les chiffres de 2018.</div>", unsafe_allow_html=True)
    # Ajout d'une autre ligne blanche avec une marge
    st.markdown("<h3 style= 'border-bottom: 2px solid white;margin-bottom: 20px; '</h3>", unsafe_allow_html=True)

    
    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################


    # Sunburst Chart
    df_sunburst = df.groupby(['Year', 'Nature mutation']).size().reset_index(name='Counts')
    fig_sunburst = px.sunburst(df_sunburst, path=['Year', 'Nature mutation'], values='Counts')

    # Définir une palette de couleurs pour les types de mutations
    color_map = {
        "Vente": "#1f77b4",
        "Vente en l'état futur d'achèvement": "#ff7f0e",
        "Adjudication": "#2ca02c",
        "Echange": "#d62728",
        "Vente terrain à bâtir": "#9467bd",
        # Ajoutez d'autres types et couleurs si nécessaire
    }

    st.subheader("")  # Un espace vide pour décaler le graphique vers le bas
    

    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("Sunburst Chart - Mutations par année et par type")
        st.plotly_chart(fig_sunburst, use_container_width=True)

    with col2:

            ############################################
            ############################################

            #                   GRAPH

            ############################################
            ############################################

        df_line = df_year[df_year['Year'] == selected_year].groupby(['Month', 'Nature mutation']).size().reset_index(name='Counts')
        st.write(f"Line Plot - Mutations par mois en {selected_year}")
        fig_line = px.line(df_line, x='Month', y='Counts', color='Nature mutation', color_discrete_map=color_map)
        st.plotly_chart(fig_line, use_container_width=True)
    
  
    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    # Groupage des données pour le Pie Chart
    df_pie = df_year['Nature mutation'].value_counts().reset_index()
    df_pie.columns = ['Nature mutation', 'Count']

    # Création du Pie Chart
    fig_pie = px.pie(df_pie, names='Nature mutation', values='Count', title='Nature de Mutation\n\n')

    # Colonnes pour les graphiques
    col1, col2 = st.columns([1, 1])

    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    # Groupage des données pour le Pie Chart
    df_pie = df_year['Nature mutation'].value_counts().reset_index()
    df_pie.columns = ['Nature mutation', 'Count']

    # Initialize session state
    if 'click_data_pie' not in st.session_state:
        st.session_state.click_data_pie = None


    # Création du Pie Chart
    fig_pie = px.pie(df_pie, names='Nature mutation', values='Count', title='Nature de Mutation')

    # Colonnes pour les graphiques
    col1, col2 = st.columns([1, 1])

    # Afficher le Pie Chart et obtenir les données du point cliqué
    # Create Pie chart
    with col1:
        st.write("Pie Chart - Nature de Mutation la Plus Courante")
        st.plotly_chart(fig_pie, use_container_width=True)

    selected_mutation = df_pie['Nature mutation'][0]  # Utiliser la plus fréquente par défaut


    # Check for clickData
    if st.session_state.click_data_pie is not None:
        selected_mutation = st.session_state.click_data_pie['points'][0]['label']
    else:
        selected_mutation = df_pie['Nature mutation'][0]  # Use the most frequent by default

    with col2:
        # Group the data by 'Year' and compute the average of 'Valeur fonciere'
        df_valeur_fonciere_by_year = df.groupby('Year')['Valeur fonciere'].mean().reset_index()

        # Create a line plot to visualize the evolution of 'Valeur fonciere' over the years
        fig_valeur_fonciere = px.line(df_valeur_fonciere_by_year, 
                                      x='Year', 
                                      y='Valeur fonciere', 
                                      title="Évolution de la Valeur Foncière par Année")

        # Display the plot
        st.plotly_chart(fig_valeur_fonciere, use_container_width=True)

    st.markdown("<div style='font-size: 1.5em;'>En observant deux graphes, nous voyons que la vente est l'une des transactions les plus courantes, suivie des échanges. Dans l'ensemble, plus de 90% des transactions sont des ventes. Toutefois, l'évolution de la valeur foncière annuelle a chuté de 250 000 000 à 100 000 000, mais remonte lentement vers les 150 000 000. Cela renforce l'idée que le marché de l'immobilier dans les Yvelines est fragile, mais qu'il est en train de remonter par rapport à 2018.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)


    grouped_data = df.groupby('Year')['Valeur fonciere'].sum().reset_index()


    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    # Bar Chart pour la moyenne de Valeur foncière par type de voie
    df_valeur_fonciere_moyenne = df_year.groupby('Type de voie')['Valeur fonciere'].mean().reset_index()
    fig_valeur_fonciere_bar = px.bar(df_valeur_fonciere_moyenne.sort_values(by='Valeur fonciere'), 
                                 x='Type de voie', 
                                 y='Valeur fonciere', 
                                 title="Moyenne de la Valeur Foncière par Type de Voie",
                                 category_orders={"Type de voie": df_valeur_fonciere_moyenne.sort_values(by='Valeur fonciere')['Type de voie'].tolist()})

    
    fig_valeur_fonciere_bar.update_layout(
        title={
            'text': "Moyenne de la Valeur Foncière par Type de Voie",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'size': 24  # taille du texte pour le titre
            }
        }
    )

    st.plotly_chart(fig_valeur_fonciere_bar, use_container_width=True)
    
    st.markdown("<div style='font-size: 1.5em;'>Lorsque nous examinons le graphe montrant la moyenne de la valeur foncière par type de voie, nous constatons qu'elle évolue d'année en année. En effet, les chiffres diffèrent pour 2018, 2019, et 2020. Un point d'intérêt ici est la position des 'places'. En 2018, elle était en 9e position, puis a chuté à la 14e en 2019, encore plus bas à la 18e en 2020, est remontée à la 13e en 2021 et est maintenant en 6e position en 2022. Bien que cela n'implique pas nécessairement une augmentation de la valeur de ma maison, il est bénéfique d'être situé dans un type de voie avec l'une des valeurs foncières moyennes les plus élevées.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)


    # Supposons que votre dataframe s'appelle df
    unique_pairs = df_year.drop_duplicates(subset=['longitude', 'latitude'])

    # Cumuler la valeur foncière
    cumulated_value = unique_pairs.groupby('Type de voie')['Valeur fonciere'].sum().reset_index()

    top_5_voie = cumulated_value.nlargest(5, 'Valeur fonciere')

    
    # Barplot pour le top 5
    bar_chart = px.bar(top_5_voie, x='Type de voie', y='Valeur fonciere', title="Top 5 des types de voie par valeur foncière cumulée")

    # Utilisation de st.columns pour afficher les graphiques côte à côte
   

    st.plotly_chart(bar_chart, use_container_width=True)



    
    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################


    # Graphique à barres pour les communes avec le plus de mutations
    df_commune_mutations = df_year['Commune'].value_counts().reset_index()
    df_commune_mutations.columns = ['Commune', 'Nombre de mutations']
    fig_commune_bar = px.bar(df_commune_mutations.nlargest(10, 'Nombre de mutations'), 
                             x='Commune', 
                             y='Nombre de mutations', 
                             title="Top 10 des communes avec le plus de mutations")

    st.plotly_chart(fig_commune_bar, use_container_width=True)

    
    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    
    # Filtrons pour les Ventes
    df_vente = df_year[df_year['Nature mutation'] == 'Vente']
    df_vente_count = df_vente['Commune'].value_counts().reset_index()
    df_vente_count.columns = ['Commune', 'Nombre de Vente']

    # Top 5 communes pour les Ventes
    df_top_vente = df_vente_count.nlargest(5, 'Nombre de Vente')
    fig_top_vente = px.bar(df_top_vente, x='Commune', y='Nombre de Vente', title="Top 5 des communes avec le plus de Vente")

    # Bottom 5 communes pour les Ventes
    df_bottom_vente = df_vente_count.nsmallest(5, 'Nombre de Vente')
    fig_bottom_vente = px.bar(df_bottom_vente, x='Commune', y='Nombre de Vente', title="Top 5 des communes avec le moins de Vente")

    # Créons les colonnes
    col1, col2 = st.columns(2)

    # Affichons les graphiques dans chaque colonne
    with col1:
        st.plotly_chart(fig_top_vente, use_container_width=True)
    with col2:
        st.plotly_chart(fig_bottom_vente, use_container_width=True)


    st.markdown("<div style='font-size: 1.5em;'>Concernant les différents types de voies, il est clair que les rues sont les plus courantes, suivies des avenues, routes, chemins, et allées. L'aspect vraiment intéressant est de déterminer quelles sont les communes avec le plus de mutations, car cela nous donne une idée des marchés immobiliers les plus actifs. Sur ce point, Sartrouville est en première position, suivi de Saint Germain en Laye en deuxième et neuvième position respectivement, et Maisons-Laffitte en onzième position. Ces communes sont proches de chez moi, bien que ma propre commune, Le Mesnil-le-Roi, n'apparaisse pas. Lorsque nous observons les évolutions des dix principales communes avec le plus de mutations, il est apparent que Sartrouville et Saint Germain en Laye sont régulièrement dans le top 10. De même, lors de l'examen des communes avec le plus grand nombre de ventes, nous constatons qu'aucune commune proche de chez moi n'apparaît dans la liste des cinq communes avec le moins de ventes.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)

    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    # Liste des communes d'intérêt
    communes = ['SARTROUVILLE', 'HOUILLES', 'MAISONS-LAFFITTE', 'PECQ (LE)', 'MESNIL-LE-ROI (LE)', 'SAINT-GERMAIN-EN-LAYE']

    # Compter le nombre de ventes par commune pour chaque année
    sales_count = df_vente.groupby(['Year', 'Commune']).size().reset_index(name='number_of_sales')

    # Liste des années présentes dans df_year
    years = sales_count['Year'].unique()

    # Affichage des classements dans des blocs de métriques pour chaque année
    for year in years:
        st.write(f"### Classement des ventes pour l'année {year}")

        # Trier pour obtenir le classement pour cette année
        current_year_data = sales_count[sales_count['Year'] == year].sort_values(by='number_of_sales', ascending=False).reset_index(drop=True)

        # Obtenir le classement des communes d'intérêt
        communes_ranking = current_year_data[current_year_data['Commune'].isin(communes)]

        # Créez toujours un nombre de colonnes égal à la liste des communes d'intérêt
        cols_communes = st.columns(len(communes))
        for col_idx, (i, row) in enumerate(communes_ranking.iterrows()):
            with cols_communes[col_idx]:
                st.metric(label=row['Commune'], value=row['number_of_sales'])
                st.write(f"Classement: {i+1}")

    st.markdown("<div style='font-size: 1.5em;'>En se concentrant spécifiquement sur les communes près de chez moi, comme Sartrouville, Saint Germain en Laye, Maisons-Laffitte, Le Pecq, et ma commune, Le Mesnil-le-Roi, nous observons des tendances sur plusieurs années. Par exemple, Sartrouville occupe souvent la troisième position, tandis que Le Pecq reste autour de la soixantième position. Malheureusement, ma propre commune débute à la 59e position, descend jusqu'à la 85e, remonte à la 79e, et chute à la 82e. Il est évident que bien que certaines communes aient été impactées par la COVID-19, la plupart ont réussi à se rétablir ou à stagner depuis 2019. Cependant, ma commune, Le Mesnil-le-Roi, n'a jamais retrouvé sa position initiale.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)

    
    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    
    communes = ['SARTROUVILLE', 'HOUILLES', 'MAISONS-LAFFITTE', 'PECQ (LE)', 'MESNIL-LE-ROI (LE)', 'SAINT-GERMAIN-EN-LAYE']

    # Compter le nombre de ventes par commune pour chaque année
    sales_count = df.groupby(['Year', 'Commune']).size().reset_index(name='number_of_sales')

    # Trier pour obtenir le classement pour chaque année
    sales_count['Ranking'] = sales_count.groupby('Year')['number_of_sales'].rank(ascending=False, method='min')

    # Filtrer le dataframe pour ne garder que les communes d'intérêt
    filtered_sales_count = sales_count[sales_count['Commune'].isin(communes)]

    # Créer le line plot avec Plotly
    fig = px.line(filtered_sales_count, 
                  x='Year', 
                  y='Ranking', 
                  color='Commune', 
                  title="Classement des communes à travers les années",
                  labels={'Ranking': 'Classement'},
                  line_shape='linear')

    # Inverser l'axe des ordonnées pour que le classement soit affiché correctement (1 en haut)
    fig.update_yaxes(autorange="reversed")

    # Affichez le graphique dans Streamlit
    st.plotly_chart(fig, use_container_width=True)

    


    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    # Lecture de la vidéo dans Streamlit
    video_file = open('race_chart_video_15.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    st.markdown("<div style='font-size: 1.5em;'>De manière plus visuelle, en analysant quelles communes ont réalisé le plus de ventes au fil du temps, il apparaît qu'Houilles commence en première position, mais est rapidement surpassée par Rocancourt. Cependant, Houilles reprend rapidement le dessus, avec Sartrouville qui la double quelques mois plus tard. D'autres communes telles que Saint Germain en Laye et Maisons-Laffitte figurent également sur ce graphe. En fin de compte, Sartrouville est en tête, suivie de Conflans, Houilles, Mantes-la-Jolie, et Saint Germain en Laye.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)


    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    def create_sunburst_chart(df):
        df_count = df.groupby(['Year', 'Type local']).size().reset_index(name='count')

        sunburst_chart = px.sunburst(
            df_count,
            path=['Year', 'Type local'],
            values='count',
            title="Nombre de Type local par année",
            maxdepth=2
        )
        sunburst_chart.update_traces(textinfo='label+percent parent')
        return sunburst_chart
    
    def create_line_plot(df):
        # Création d'un DataFrame pour stocker la proportion de chaque 'Type local' par année
        df_proportion = df.groupby(['Year', 'Type local']).size().unstack().fillna(0)
        df_proportion = df_proportion.div(df_proportion.sum(axis=1), axis=0) * 100  # Conversion en pourcentage     
        line_chart = px.line(
            df_proportion.reset_index().melt(id_vars='Year', value_name='Proportion', var_name='Type local'),
            x='Year',
            y='Proportion',
            color='Type local',
            title="Proportion en pourcentage de Type local par année"
        )
        return line_chart
    
    # Sunburst Chart
    sunburst_chart = create_sunburst_chart(df)
    
    # Line Plot
    line_chart = create_line_plot(df)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(sunburst_chart, use_container_width=True)

    with col2:
        st.plotly_chart(line_chart, use_container_width=True)

    st.markdown("<div style='font-size: 1.5em;'>Maintenant, nous allons nous intéresser aux types de local par année. Ici, on peut voir clairement que le type de local qui domine est la maison, suivi de l'appartement, suivi de la dépendance. Et ensuite des autres. Avec un véritable essor d'ailleurs des dépendances. En 2021 et en 2022, qui reprennent le dessus sur la part de marché des appartements et des différents locaux. Et les différents locaux. En effet, on peut voir que dans les divisions, il y a eu plus de 10000 différentes offres de maison et uniquement 590 pour les locaux différents, 410 pour des dépendances et 263 pour des appartements.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)

    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    # Assumons que votre dataframe a des colonnes 'latitude' et 'longitude' pour représenter ces coordonnées
    unique_coordinates_df = df.drop_duplicates(subset=['latitude', 'longitude'])
    new_df = unique_coordinates_df.copy()
    
    # Supposons que votre dataframe ait une colonne appelée 'type_de_local' pour le type de local.
    # Compter le nombre de chaque type de local et trier par compte
    type_counts = new_df['Type local'].value_counts().reset_index()
    type_counts.columns = ['Type de Local', 'Compte']

    # Création du graphique avec Altair
    chart = alt.Chart(type_counts).mark_bar().encode(
       x=alt.X('Type de Local', sort='-y', axis=alt.Axis(title='Type de Local', labelFontSize=18, titleFontSize=16)),  # tri par compte décroissant et ajustement de la taille de la police
    y=alt.Y('Compte', axis=alt.Axis(title='Nombre', labelFontSize=14, titleFontSize=16)),
        tooltip=['Type de Local', 'Compte']
    ).properties(
        width=600,
        height=700
    )

    # Affichage du graphique dans Streamlit
    st.altair_chart(chart, use_container_width=True)


    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################
    
    
    # Sélectionnez uniquement les colonnes numériques du dataframe
    numeric_cols = new_df.select_dtypes(include=['float64', 'int64'])

    # Obtenez la matrice de corrélation
    corr_matrix = numeric_cols.corr()

    # Créez le heatmap avec Altair
    heatmap = alt.Chart(corr_matrix.reset_index().melt('index')).mark_rect().encode(
        x='index:O',
        y='variable:O',
        color='value:Q',
        tooltip=['index', 'variable', 'value']
    ).properties(
        title="Matrice de corrélation des colonnes numériques",
        width=600,
        height=600
    )

    # Affichez le heatmap dans Streamlit
    st.altair_chart(heatmap, use_container_width=True)

    st.markdown("<div style='font-size: 1.5em;'>Prochain graphe : quand on regarde la matrice de corrélation des colonnes numériques, on peut voir qu'il n'y a aucune corrélation intéressante, sauf entre le nombre de pièces et le code de type local, donc le nombre de pièces par rapport à si c'est une maison ou un appartement, ceci paraît logique puisque. Si nous avons une maison qui est de code type local un, alors il y aura plus de pièces principales que dans un appartement ou que dans une dépendance.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)

    
    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    # Filtrage des éléments de new_df en fonction de la colonne "Valeur fonciere"
    new_df = new_df[new_df['Valeur fonciere'] <= 20000000]



    # Créez le boxplot avec Plotly et ajoutez les points
    fig = px.box(new_df, x='Type local', y='Valeur fonciere', points="all", title="Boxplots pour 'Type local' avec points")

    # Affichez le graphique dans Streamlit
    st.plotly_chart(fig, use_container_width=True)


    st.markdown("<div style='font-size: 1.5em;'>Prochain graphe : Sur le boxplot pour le type de local avec des points, nous pouvons voir ici que. Les maisons coûtent plus cher en moyenne que les dépendances et les appartements, avec beaucoup plus de outliers qui se retrouvent dans la catégorie des maisons que dans les autres qui sont distribuées de manière plus proportionnelle.</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='border-bottom: 2px solid white;margin-bottom: 20px;'></h3>", unsafe_allow_html=True)


    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    
    # Filtrer le dataframe pour la year sélectionnée et pour les maisons
    houses_df = new_df[(new_df['Year'] == selected_year) & (new_df['Type local'] == 'Maison')]

    # Grouper par 'Nombre pieces principales' et calculer la moyenne de "Valeur fonciere"
    avg_values_houses = houses_df.groupby('Nombre pieces principales')['Valeur fonciere'].mean().reset_index()

    # Créer un graphique en barres avec Plotly
    fig_houses = px.bar(avg_values_houses, x='Nombre pieces principales', y='Valeur fonciere', title=f"Prix moyen des Maisons par Nombre de pièces pour l'année {selected_year}")

    # Affichez le graphique dans Streamlit
    st.plotly_chart(fig_houses, use_container_width=True)

    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################


    # Filtrer le dataframe pour la year sélectionnée et pour les maisons
    houses_df = new_df[(new_df['Year'] == selected_year) & (new_df['Type local'] == 'Maison')]

    # Grouper par 'Type de voie' et calculer la moyenne de "Valeur fonciere"
    avg_values_voie = houses_df.groupby('Type de voie')['Valeur fonciere'].mean().reset_index()

    # Trier le dataframe en ordre décroissant de "Valeur fonciere"
    avg_values_voie = avg_values_voie.sort_values(by="Valeur fonciere", ascending=False)

    # Calculer la moyenne générale
    overall_avg = houses_df['Valeur fonciere'].mean()

    # Créer un graphique en barres avec Plotly
    fig_voie = px.bar(avg_values_voie, x='Type de voie', y='Valeur fonciere', title=f"Prix moyen des Maisons par Type de voie pour l'année {selected_year}")

    # Ajouter une ligne horizontale pour la moyenne générale
    fig_voie.add_shape(
        go.layout.Shape(
            type="line",
            x0=avg_values_voie['Type de voie'].iloc[0],  # Début de la ligne
            x1=avg_values_voie['Type de voie'].iloc[-1], # Fin de la ligne
            y0=overall_avg,
            y1=overall_avg,
            line=dict(color="red")
        )
    )

    # Affichez le graphique dans Streamlit
    st.plotly_chart(fig_voie, use_container_width=True)

    st.markdown("<div style='font-size: 1.5em;'>Prochain graphe : quand on regarde le prix moyen des maisons par le type de voix pour les différentes années, on peut voir au final que la place se retrouve en général en dessous des prix moyens de la demande foncière. Donc, au final, ce n'est pas si avantageux que ça de se retrouver sur une place.</div>", unsafe_allow_html=True)

    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    # Grouper par 'Surface terrain' et calculer la moyenne de "Valeur fonciere"
    avg_values_terrain = houses_df.groupby('Surface terrain')['Valeur fonciere'].mean().reset_index()

    # Créer un graphique en barres avec Plotly
    fig_terrain = px.bar(avg_values_terrain, x='Surface terrain', y='Valeur fonciere', title=f"Prix moyen des Maisons par Surface terrain pour l'année {selected_year}")

    # Affichez le graphique dans Streamlit
    st.plotly_chart(fig_terrain, use_container_width=True)


    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################


    # Filtrer le dataframe pour la year sélectionnée et pour les maisons
    houses_df = new_df[(new_df['Year'] == selected_year) & (new_df['Type local'] == 'Maison')]

    # Grouper par 'Commune' et calculer la moyenne de "Valeur fonciere"
    avg_values_commune = houses_df.groupby('Commune')['Valeur fonciere'].mean().reset_index()

    # Trier les résultats par "Valeur fonciere" en ordre décroissant et prendre les 10 premières entrées
    top_10_communes = avg_values_commune.sort_values(by='Valeur fonciere', ascending=False).head(10)

    # Créer un graphique en barres avec Plotly
    fig_communes = px.bar(top_10_communes, x='Commune', y='Valeur fonciere', title=f"Top 10 des Communes par Prix Moyen des Maisons pour l'année {selected_year}")

    # Affichez le graphique dans Streamlit
    st.plotly_chart(fig_communes, use_container_width=True)



    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################


    # Liste des communes d'intérêt
    communes_of_interest = ['HOUILLES', 'SARTROUVILLE', 'SAINT-GERMAIN-EN-LAYE', 'MAISONS-LAFFITTE', 'PECQ (LE)', 'MESNIL-LE-ROI (LE)']

    # Filtrer le dataframe pour la year sélectionnée, pour les maisons, et pour les communes d'intérêt
    filtered_df = new_df[(new_df['Year'] == selected_year) & (new_df['Type local'] == 'Maison') & (new_df['Commune'].isin(communes_of_interest))]

    # Grouper par 'Commune' et calculer la moyenne de "Valeur fonciere"
    avg_values_commune = filtered_df.groupby('Commune')['Valeur fonciere'].mean().reset_index()

    # Créer un graphique en barres avec Plotly
    fig_communes_specific = px.bar(avg_values_commune, x='Commune', y='Valeur fonciere', title=f"Prix Moyen des Maisons pour l'année {selected_year} pour les communes sélectionnées")

    # Affichez le graphique dans Streamlit
    st.plotly_chart(fig_communes_specific, use_container_width=True)


    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    # Grouper par 'Surface reelle bati' et calculer la moyenne de "Valeur fonciere"
    avg_values_bati = houses_df.groupby('Surface reelle bati')['Valeur fonciere'].mean().reset_index()

    # Créer un graphique en barres avec Plotly
    fig_bati = px.bar(avg_values_bati, x='Surface reelle bati', y='Valeur fonciere', title=f"Prix moyen des Maisons par Surface réelle bâtie pour l'année {selected_year}")

    # Affichez le graphique dans Streamlit
    st.plotly_chart(fig_bati, use_container_width=True)

    
    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################


    # Supprimez les lignes avec des valeurs NaN dans les colonnes 'latitude' et 'longitude'
    new_df = new_df.dropna(subset=['latitude', 'longitude'])

    # Créer une carte de base centrée sur un emplacement moyen (vous pouvez le changer si vous le souhaitez)
    mean_lat = new_df['latitude'].mean()
    mean_lon = new_df['longitude'].mean()
    m = folium.Map(location=[mean_lat, mean_lon], zoom_start=10)

    # Ajouter des points à la carte avec FastMarkerCluster
    locations = list(zip(new_df['latitude'], new_df['longitude']))
    popups = [f"Année: {row['Year']} Valeur Foncière: {row['Valeur fonciere']}" for idx, row in new_df.iterrows()]
    m.add_child(FastMarkerCluster(locations, popups=popups))

    # Enregistrez la carte en tant que fichier HTML
    m.save("map.html")

    # Utilisez la fonction st.components.v1.html pour afficher le contenu HTML de la carte
    with open("map.html", "r") as f:
        contents = f.read()
        st.components.v1.html(contents, height=700)



    ############################################
    ############################################

    #                   GRAPH

    ############################################
    ############################################

    st.markdown("<div style='font-size: 1.5em;'>En conclusion, l'immobilier dans les Yvelines est complexe et fluctuant, mais certaines tendances claires apparaissent. Des communes comme Sartrouville et Saint Germain en Laye sont des marchés immobiliers forts, tandis que d'autres, comme ma commune, Le Mesnil-le-Roi, ont du mal à se remettre de la période COVID-19. Cela étant dit, il est important de noter que même si le nombre de mutations a diminué, cela ne signifie pas nécessairement une diminution de la valeur des propriétés. En fait, la valeur foncière moyenne peut augmenter même si le nombre de transactions diminue.</div>", unsafe_allow_html=True)






    




    


    




   


