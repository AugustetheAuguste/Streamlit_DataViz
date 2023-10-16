
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
import pydeck as pdk
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

def load_data():
     # Charger les données du subset_78 ici, par exemple depuis un fichier CSV
     return pd.read_json('Datasets\subset_specified_all_years.jsonl', lines = True)
df = load_data()

print(df.columns)

 # Filtrer pour ne garder que les maisons
df_maisons = df[df["Type local"] == "Maison"]

# Regrouper par localisation et année, puis compter le nombre de dépendances
df_grouped = df_maisons.groupby(['No voie', 'Type de voie', 'Code voie', 'Voie', 'Code postal', 'Commune', 'Year']).size().reset_index(name='count')

# Filtrer pour ne garder que les groupes avec plus d'une dépendance
df_duplicates = df_grouped[df_grouped['count'] > 1]

# Afficher le nombre total de cas
total_cases = df_duplicates['count'].sum()
print(f"Le nombre total de cas où des maisons à la même localisation et à la même année ont une dépendance est de : {total_cases}")
