# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

import folium
from streamlit_folium import folium_static

import pages.modulos.utils as utils


# Importa o dataset
df = pd.read_csv('dataset/train.csv')

# Limpeza dos dados
df1 = df.copy()

df1 = utils.clean_dataset(df1)



st.set_page_config(page_title='Visão Entregadores', page_icon='🛵', layout='wide')


# =====================================================================================
# Sidebar (Barra Lateral)
# =====================================================================================
image_path = 'logo.png'
image = Image.open(image_path)
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('### Fastest Delivery in Town')
st.sidebar.markdown('''---''')

st.sidebar.markdown('## Selecione uma data limite')

data_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.datetime(2022, 4, 13),
    min_value=pd.datetime(2022, 2, 11),
    max_value=pd.datetime(2022, 6, 4),
    format='DD-MM-YYYY'
)



st.sidebar.markdown('''---''')


traffic_list = list(df1['Road_traffic_density'].unique())

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito?',
    traffic_list,
    default=traffic_list

)

st.sidebar.markdown('''---''')
st.sidebar.markdown('### Powered by Comunidade DS')


# Filtro de Data
df1 = df1.loc[df1['Order_Date'] < data_slider, :]

# Filtro de Trânsito
df1 = df1.loc[df1['Road_traffic_density'].isin(traffic_options), :]




# =====================================================================================
# Layout streamlit
# =====================================================================================

# Header
st.header('Marketplace - Visão Entregadores')

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])


with tab1:
    
    with st.container():
        
        st.title('Overall Metrics')
        col1, col2, col3, col4 = st.columns(4, gap='large')
        
        with col1:
            
            maior_idade = df1['Delivery_person_Age'].max()
            col1.metric('Maior idade', maior_idade)
            
            
        with col2:
            
            menor_idade = df1['Delivery_person_Age'].min()
            col2.metric('Menor idade', menor_idade)
            
            
        with col3:
            
            melhor_condicao = df1['Vehicle_condition'].max()
            col3.metric('Melhor condição', melhor_condicao)
            
        with col4:
            
            pior_condicao = df1['Vehicle_condition'].min()
            col4.metric('Pior condição', pior_condicao)
            
            
            
    with st.container():
        
        st.markdown('''---''')
        st.title('Avaliações')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('##### Avaliações média por entregador')
            
            df_ratings = df1[['Delivery_person_Ratings', 'Delivery_person_ID']].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(df_ratings)
            
            
        with col2:
            
            st.markdown('##### Avaliação média por trânsito')
            
            df_traffic_stats = ( df1[['Delivery_person_Ratings', 'Road_traffic_density']].groupby('Road_traffic_density')
                                                .agg([np.mean, np.std]).reset_index() )
            
            df_traffic_stats.columns = ['Road_traffic_density', 'Ratings_mean', 'Ratings_std']
            st.dataframe(df_traffic_stats)

            
            
            st.markdown('##### Avaliação média por clima')
            
            df_weather_stats = ( df1[['Delivery_person_Ratings', 'Weatherconditions']].groupby('Weatherconditions')
                                                .agg({'Delivery_person_Ratings': ['mean', 'std']}).reset_index() )

            df_weather_stats.columns = ['Weatherconditions', 'Ratings_mean', 'Ratings_std']
            st.dataframe(df_weather_stats)
            
            
            
    with st.container():
        
        st.markdown('''---''')
        st.title('Velocidade de entrega (média)')
        
        city = st.selectbox(
            'Qual cidade você quer filtrar?',
            df1['City'].unique()
        )
        
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('##### Top entregadores mais rápidos')
            
            df_fast_delivery = ( df1[['Time_taken(min)', 'Delivery_person_ID', 'City']].groupby(['City', 'Delivery_person_ID'])
                                        .mean().sort_values(['City', 'Time_taken(min)']) )
            
            st.dataframe(df_fast_delivery.loc[city].reset_index().head(10))

            
        with col2:
            st.markdown('##### Top entregadores mais lentos')
            
            df_slow_delivery = ( df1[[ 'Time_taken(min)', 'Delivery_person_ID', 'City']].groupby(['City', 'Delivery_person_ID'])
                                        .mean().sort_values(['City', 'Time_taken(min)'], ascending=False) )
            
            st.dataframe(df_slow_delivery.loc[city].reset_index().head(10))
            
            
            
        
        
        