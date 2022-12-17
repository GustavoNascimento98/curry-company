import streamlit as st
from PIL import Image



import sys
module_path = r'C:\Users\estud\Desktop\ComunidadeDS\FTC\6_visualizacao_interativa\pages\modulos'
sys.path.append(module_path)



st.set_page_config(
    page_title='Home',
    page_icon='📊',
    layout='wide'

)


image_path = 'logo.png'
image = Image.open(image_path)

st.sidebar.image(image, width=120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('### Fastest Delivery in Town')
st.sidebar.markdown('''---''')


st.write('# Curry Company Growth Dashboard')

st.markdown(
    '''
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos entregadores e restaurantes.
    
    ### Como utilizar esse dashboard?
    
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
        
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
        
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes.
        
    ### Ask for Help
    - Time de Data Science no Discord
    '''
)