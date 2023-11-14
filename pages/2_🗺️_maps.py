import streamlit as st 
import pandas as pd
import geopandas as gpd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import matplotlib.pyplot as plt
import locale
import os
CONDA_PREFIX = r"C:\Users\hcord\anaconda3\envs\geo"
os.environ['GDAL_DATA'] = os.environ['CONDA_PREFIX'] + r'\Library\share\gdal'

locale.setlocale( locale.LC_ALL, 'pt_BR.UTF-8' )

st.set_page_config(layout="wide")

st.session_state['first_display'] = True

# Maps
map_width=800
map_height=400
sp_lat_center = -23.550164466
sp_lon_center = -46.633664132

if "map_districts" not in st.session_state:
    st.session_state['map_districts'] = None
if "map_sp" not in st.session_state:
    st.session_state['map_sp'] = None

@st.cache_data
def load_itbi_map_files():

    temp = pd.read_csv("./data/itbi_files.zip")
    itbi_map_df = temp[['Número do Cadastro','Descrição do uso','CEP']].copy()
    itbi_map_df['CEP'] = itbi_map_df['CEP'].apply(lambda x: '{0:0>8}'.format(x))
    itbi_map_df['Descrição do uso'] = itbi_map_df['Descrição do uso'].map(lambda x: x[0:30])
    
    cep_locations_df = pd.read_csv("./data/cep_ll.csv")
    cep_locations_df['CEP'] = cep_locations_df['CEP'].apply(lambda x: '{0:0>8}'.format(x))

    # Build a LK Table for conversion
    cep_to_bairro = {}
    for _,row in cep_locations_df.iterrows():
        cep_to_bairro[row['CEP']] = row['Bairro'].upper()

    print(cep_to_bairro)
    itbi_map_df['Bairro_New'] = itbi_map_df['CEP'].map(lambda c:cep_to_bairro[c])

    return (itbi_map_df, cep_locations_df)
itbi_map_df, cep_locations_df = load_itbi_map_files()

# Divide a tela do Dashboard em Containers
# Mapas de Localização
con_loc_choro = st.container()
con_loc_clusters = st.container()

def plot_choro_map():
    # Choromap
    # Sao Paulo Geometry
    prov_local = "./data/SIRGAS_SHP_distrito"
    sp_districts = gpd.read_file(prov_local)  # note that I point to the shapefile "directory" containg all the individual files
    sp_districts = sp_districts.to_crs("EPSG:4326")    # I'll explain this later, I'm converting to a different coordinate reference system

    itbi_locs_df = itbi_map_df[['Número do Cadastro','Bairro_New']].copy()
    itbi_locs_df = itbi_locs_df.groupby("Bairro_New").count()
    itbi_locs_df = itbi_locs_df.sort_values("Número do Cadastro",ascending=False).head(50).reset_index()
    itbi_locs_df = itbi_locs_df.rename(columns= {'Bairro_New':'ds_nome','Número do Cadastro':'count'})

    map_districts = folium.Map(location=(sp_lat_center,sp_lon_center), zoom_start=11, tiles="cartodb positron")
    folium.Choropleth(
        geo_data=sp_districts,
        data=itbi_locs_df,
        columns=["ds_nome", "count"],
        key_on="feature.properties.ds_nome",
        fill_color="RdYlGn_r",
        fill_opacity=0.3,
        line_opacity=0.3,
        nan_fill_color="white",
    ).add_to(map_districts)
    st.session_state['map_districts'] = map_districts
    folium_static(st.session_state['map_districts'],width=map_width, height=map_height)

def plot_cluster_map():
    # Clusters Map
    itbi_locations_df = itbi_map_df[['CEP','Descrição do uso']]
    itbi_locations_df = pd.merge(itbi_locations_df, cep_locations_df, how='left', on='CEP')
    
    itbi_locations_df = itbi_locations_df[~itbi_locations_df['lat'].isna()]
    ll_df = itbi_locations_df[["lat","lon"]]

    map_sp = folium.Map(location=[sp_lat_center, sp_lon_center], zoom_start=7, control_scale=True)
    marker_cluster = MarkerCluster().add_to(map_sp)

    for index, row in itbi_locations_df.head(2000).iterrows():
        folium.Marker(
            location=[row['lat'],row['lon']],
            popup=[row['Descrição do uso']],
            icon=folium.Icon(color="green", icon="ok-sign"),
        ).add_to(marker_cluster)
    st.session_state['map_sp'] = map_sp
    folium_static(st.session_state['map_sp'],width=map_width, height=map_height)

with con_loc_choro:
    plot_choro_map()
    
with con_loc_clusters:
    plot_cluster_map()
