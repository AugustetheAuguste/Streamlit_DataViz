# presentation.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def app():
    
    # Grand titre stylisé
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0px; '>Analyse de la Valeur Immobilière 🏡</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style= 'border-bottom: 5px solid white;margin-bottom: 100px; '</h1>", unsafe_allow_html=True)
    # Introduction à gauche et image à droite
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h2 style='font-size: 45px;'>Introduction 📖</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 18px;'>Bienvenue dans l'analyse des valeurs foncières. Dans les Yvelines, près de la ville de Maisons-Laffitte et dans le département Rhône-Alpes, autour de Lyon. Pourquoi s'intéresser aux valeurs immobilières et spécifiquement à ces endroits ? C'est très simple. En effet, je suis lyonnais, né dans le 4e arrondissement de Lyon. J'y ai vécu pendant 9 ans avant de déménager à New York, puis de revenir à Paris. Aujourd'hui, mes parents souhaitent retourner à Lyon et vendre notre maison parisienne. Fort de mes compétences en data science et en data visualisation, j'estime pouvoir les aider à prendre des décisions éclairées afin de vendre notre maison à un prix juste et de mieux comprendre le marché immobilier local. Nous aborderons également l'analyse du marché immobilier à Lyon pour les orienter vers des communes présentant des offres potentiellement intéressantes.</p>", unsafe_allow_html=True)
    with col2:
        st.image("../Images/House.jpg", caption="Légende de l'image si nécessaire", use_column_width=True)

    # Table des matières
    st.markdown("<h2 style='font-size: 45px;'>Table des Matières 📑</h2>", unsafe_allow_html=True)


    # Analyse du DVF dans les Yvelines:
    st.markdown("<h2 style='font-size: 35px;'>1. Analyse du DVF à Yvelines 🌳</h2>", unsafe_allow_html=True)

    # Analyse du DVF à Maisons-Laffite et les alentours
    st.markdown("<h2 style='font-size: 35px;'>2. Analyse du DVF à Maisons-Laffite et les alentours 🏰</h2>", unsafe_allow_html=True)

    # Analyse du DVF à Lyons
    st.markdown("<h2 style='font-size: 35px;'>3. Analyse à Lyons 🌆</h2>", unsafe_allow_html=True)
    
    
    st.markdown("<h1 style= 'border-bottom: 5px solid white;margin-bottom: 100px; '</h1>", unsafe_allow_html=True)
    
    # Ajout d'une ligne blanche avec une marge
    
    # Ajout de votre texte en relativement gros
    st.markdown("<div style='font-size: 1.5em;'>Voici à quoi ressemble notre base de donnée:</div>", unsafe_allow_html=True)
    # Ajout d'une autre ligne blanche avec une marge

    st.markdown("<h3 style= 'margin-bottom: 20px; '</h3>", unsafe_allow_html=True)


    
    @st.cache_data

    def load_data(option):
        if option == 1:
        # Charger les données du subset_78 ici, par exemple depuis un fichier CSV
            return pd.read_json('Datasets\subset_78_all_years.jsonl', lines = True)
        
        if option == 2:
            return pd.read_json('Datasets\subset_specified_all_years.jsonl', lines = True)
        
        if option == 3:
            return pd.read_json('Datasets\\finished_subset_lyon_surrounding_all_years.jsonl', lines = True)
        
    df_78 = load_data(1)
    df_ML = load_data(2)
    df_Lyon = load_data(3)
    # Combine les dataframes

    combined_df = pd.concat([df_78, df_ML, df_Lyon], ignore_index=True)

    # Liste des colonnes à afficher
    columns_to_display = [
        'Nature mutation', 'Valeur fonciere', 'No voie', 'Type de voie','Voie','Code postal', 'Commune', 'Code departement', 
        'No plan', 'Code type local', 'Type local', 'Surface reelle bati', 
        'Nombre pieces principales', 'Year'
    ]

    # Filtrer le dataframe pour n'afficher que les colonnes spécifiques
    filtered_df = combined_df[columns_to_display]

    # Afficher le dataframe filtré dans Streamlit
    st.write(filtered_df)


    # Calculer le nombre d'éléments pour chaque dataframe
    total_elements = len(combined_df)
    elements_df_78 = len(df_78)
    elements_df_ML = len(df_ML)
    elements_df_Lyon = len(df_Lyon)

    def custom_metric(label, value, font_size_h3="2rem", font_size_style = "2rem", emoji=""):
        return f"""
        <div style="text-align: center; margin: 1rem 0;">
            <h3 style="font-size: {font_size_h3}; margin: 0;">{emoji} {label}</h3>
            <span style="font-size: {font_size_style};">{value}</span>
        </div>
        """
    
    
    # Trouver la première et la dernière année
    first_year = combined_df['Year'].min()
    last_year = combined_df['Year'].max()

    # Calculer le nombre total d'années
    number_of_years = last_year - first_year + 1


    # Metrics 3
    cols3 = st.columns(3)
    with cols3[0]:
        st.markdown(custom_metric("Première année", str(first_year),  "2.5rem", "2.5rem", "📅"), unsafe_allow_html=True)
    with cols3[1]:
        st.markdown(custom_metric("➡️", "", "2.5rem", ""), unsafe_allow_html=True)
    with cols3[2]:
        st.markdown(custom_metric("Dernière année", str(last_year), "2.5rem", "2.5rem", "📆"), unsafe_allow_html=True)



    # Metrics 1
    cols1 = st.columns(4)
    with cols1[0]:
        st.markdown(custom_metric("Nombre total d'éléments", total_elements, "1.5rem","2.5rem", "🔢"), unsafe_allow_html=True)
    with cols1[1]:
        st.markdown(custom_metric("Nombre d'éléments dans df_78", elements_df_78, "1.5rem","2.5rem", "📌"), unsafe_allow_html=True)
    with cols1[2]:
        st.markdown(custom_metric("Nombre d'éléments dans df_ML", elements_df_ML, "1.5rem","2.5rem", "📍"), unsafe_allow_html=True)
    with cols1[3]:
        st.markdown(custom_metric("Nombre d'éléments dans df_Lyon", elements_df_Lyon, "1.5rem","2.5rem", "🔍"), unsafe_allow_html=True)

    # Calculer le nombre de valeurs uniques de 'Commune' pour chaque dataframe
    unique_communes_combined = combined_df['Commune'].nunique()
    unique_communes_df_78 = df_78['Commune'].nunique()
    unique_communes_df_ML = df_ML['Commune'].nunique()
    unique_communes_df_Lyon = df_Lyon['Commune'].nunique()

    # Metrics 2
    cols2 = st.columns(4)
    with cols2[0]:
        st.markdown(custom_metric("Valeurs uniques de 'Commune' (Total)", unique_communes_combined, "1.5rem","2.5rem", "🌍"), unsafe_allow_html=True)
    with cols2[1]:
        st.markdown(custom_metric("Valeurs uniques de 'Commune' (df_78)", unique_communes_df_78, "1.5rem","2.5rem", "🌆"), unsafe_allow_html=True)
    with cols2[2]:
        st.markdown(custom_metric("Valeurs uniques de 'Commune' (df_ML)", unique_communes_df_ML, "1.5rem","2.5rem", "🏙️"), unsafe_allow_html=True)
    with cols2[3]:
        st.markdown(custom_metric("Valeurs uniques de 'Commune' (df_Lyon)", unique_communes_df_Lyon, "1.5rem","2.5rem", "🌃"), unsafe_allow_html=True)



    
    # Mappage des emojis pour chaque type de locaux
    emoji_mapping = {
        "Maison": "🏠",
        "Dépendance": "🏡",
        "Appartement": "🏢",
        "Local industriel ou commercial": "🏭"
    }
    
    # Comptes pour chaque type de locaux (fournis)
    type_counts = {
        "Maison": 101824,
        "Dépendance": 18209,
        "Appartement": 17797,
        "Local industriel ou commercial": 13798
    }
    
    # Créer des colonnes pour les métriques
    cols = st.columns(len(type_counts))
    
    for col, (local_type, count) in zip(cols, type_counts.items()):
        with col:
            emoji_for_type = emoji_mapping.get(local_type, "🔲")  # Utilisez "🔲" comme emoji par défaut si le type n'est pas dans le dictionnaire
            st.markdown(custom_metric(local_type, count, "1.5rem","2.5rem", emoji_for_type), unsafe_allow_html=True)
    




    

