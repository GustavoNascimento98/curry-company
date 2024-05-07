# Libraries
from datetime import datetime

import pandas as pd
import streamlit as st
from PIL import Image

import pages.modulos.utils as utils


# Importa o dataset
df = pd.read_csv('dataset/food-delivery-dataset.csv')


# Limpeza dos dados
df1 = df.copy()

df1 = utils.clean_dataset(df1)


st.set_page_config(page_title='Visão Restaurantes', page_icon='🍛', layout='wide')


# =====================================================================================
# Sidebar (Barra Lateral)
# =====================================================================================
image_path = 'img/logo.png'
image = Image.open(image_path)
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('### Fastest Delivery in Town')
st.sidebar.markdown('''---''')

st.sidebar.markdown('## Selecione uma data limite')

data_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 6, 4),
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

st.header('Marketplace - Visão Restaurantes')


tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])


with tab1:
    
    with st.container():
        st.title('Overall Metrics')
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            delivery_unique = df1['Delivery_person_ID'].nunique()
            col1.metric('Entregadores', delivery_unique)
            
        with col2:
            avg_distance = round(df1['Distance'].mean(), 2)
            col2.metric('Distância média (km)', avg_distance)
            
        with col3:
            df_aux = ( df1[['Festival', 'Time_taken(min)']]
                      .groupby('Festival')
                      .agg({'Time_taken(min)': ['mean', 'std']})
                )
            df_aux.columns = ['mean_time', 'std_time']
            
            avg_time_festival = round(df_aux.loc['Yes', 'mean_time'], 2)
            std_time_festival = round(df_aux.loc['Yes', 'std_time'], 2)
            
            avg_time_NO_festival = round(df_aux.loc['No', 'mean_time'], 2)
            std_time_NO_festival = round(df_aux.loc['No', 'std_time'], 2)
            
            col3.metric('Tempo médio c/ festival', avg_time_festival)
            
            
        with col4:
            col4.metric('Desvio padrão c/ festival', std_time_festival)
            
        with col5:
            col5.metric('Tempo médio s/ festival', avg_time_NO_festival)
            
        with col6:
            col6.metric('Desvio padrão c/ festival', std_time_NO_festival)
            
            
        
    with st.container():
        st.markdown('''---''')
        
        col1, col2 = st.columns(2, gap='large')
    
        with col1:
            st.title('Tempo médio de entrega por cidade')
            
            fig = utils.avg_delivery_by_city(df1)

            st.plotly_chart(fig, use_container_width=True)
            
            
        with col2:
            st.title('Distribuição da distância')
            
            df_aux = ( df1[['Time_taken(min)', 'City', 'Type_of_order']]
                      .groupby(['City', 'Type_of_order'])
                      .agg({'Time_taken(min)': ['mean', 'std']})
                      .reset_index()
                )

            df_aux.columns = ['City', 'Type', 'mean_time', 'std_time']

            st.dataframe(df_aux, use_container_width=True)


        
        
        
    with st.container():
        st.markdown('---')
        st.title('Distribuição do tempo')
        
        col1, col2 = st.columns(2)
        
        with col1:

            fig = utils.time_distribution_city(df1)

            st.plotly_chart(fig, use_container_width=True)
            
            
            
        with col2:
            
            fig = utils.sunburn_graph(df1)

            st.plotly_chart(fig, use_container_width=True)
            
        
        
    