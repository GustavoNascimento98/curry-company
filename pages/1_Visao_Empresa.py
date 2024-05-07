# Libraries
import pandas as pd
import streamlit as st
from PIL import Image

from datetime import datetime
from streamlit_folium import folium_static

import pages.modulos.utils as utils

st.set_page_config(page_title='Visão Empresa', page_icon='📊', layout='wide')


# Importa o dataset
df = pd.read_csv('dataset/food-delivery-dataset.csv')

# Limpeza dos dados
df1 = df.copy()

df1 = utils.clean_dataset(df1)

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

# Header
st.header('Marketplace - Visão Cliente')

st.dataframe(df1.head())


# st.header(data_slider)


tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])


with tab1:
    
    with st.container():
        st.markdown('# Orders by Day')

        fig = utils.order_metric(df1)

        st.plotly_chart(fig, use_container_width=True)



    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('## Traffic Order Share')
            
            fig = utils.traffic_order_share(df1)
            
            st.plotly_chart(fig, use_container_width=True)

            
        with col2:
            st.markdown('## Traffic Order City')
            
            fig = utils.traffic_order_city(df1)
            
            st.plotly_chart(fig, use_container_width=True)

    
    
with tab2:
    
    with st.container():
        st.markdown('# Orders by Week')

        fig = utils.order_by_week(df1)

        st.plotly_chart(fig, use_container_width=True)

        
    with st.container():
        st.markdown('# Orders per Deliveryman by Week')

        fig = utils.order_by_delivery(df1)

        st.plotly_chart(fig, use_container_width=True)

    
    
with tab3:
    st.markdown('# Country Maps')
    
    map_ = utils.country_map(df1)
    
    folium_static(map_, width=900, height=500)





