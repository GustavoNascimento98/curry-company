import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from haversine import haversine


def clean_dataset(df1):
    
    '''
    Essa função tem a responsabilidade de limpar o dataframe:
    
    Input  : dataframe
    Output : dataframe
    
    Tipos de limpeza:
        1. Remove espaços vázios desnecessários ( .strip() )
        2. Remove os registros que possuem dados NaN
        3. Converte algumas colunas do tipo object para int/float
        4. Formatação da coluna de datas
        5. Limpeza da coluna tempo (elimina o texto '(min)')
        6. Limpeza da coluna de condição climática
        7. Cria uma coluna com a distância entre o restaurante e o local de entrega
    '''
    
    # Colunas do dataframe que possuem dados do tipo texto (object)
    object_columns = df1.select_dtypes(include='object').columns

    # Elimina os espaços vazios após o texto nas colunas do tipo 'object'
    df1[object_columns] = df1.select_dtypes(include='object').apply(lambda column: column.str.strip())


    # 1. Elimina os registros que possuem 'Delivery_person_Age' vazio e converte para inteiro
    df1 = df1[df1['Delivery_person_Age'] != 'NaN'].copy()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    # 2. Elimina os registros que possuem 'Delivery_person_Ratings' vazio e converte para float
    df1 = df1[df1['Delivery_person_Ratings'] != 'NaN'].copy()
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    # 3. Converte a coluna 'Order_Date' para tipo data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    # 4. Elimina o texto 'conditions' da coluna 'Weatherconditions'
    df1['Weatherconditions'] = df1['Weatherconditions'].apply(lambda x: x.split(' ')[-1])

    # 5. Elimina os registros que possuem 'Road_traffic_density' vazio
    df1 = df1[df1['Road_traffic_density'] != 'NaN'].copy()

    # 6. Elimina os registros que possuem 'multiple_deliveries' vazio e converte para para int
    df1 = df1[df1['multiple_deliveries'] != 'NaN']
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    # 7. Elimina os registros que possuem 'Festival' vazio
    df1 = df1[df1['Festival'] != 'NaN'].copy()

    # 8. Elimina os registros que possuem 'City' vazio
    df1 = df1[df1['City'] != 'NaN'].copy()

    # 9. Elimina o texto '(min)' da coluna 'Time_taken(min)' e converte para inteiro
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split(' ')[-1]).astype(int)
    
    # 10. Calcula a distância média dos restaurantes e cria a coluna 'Distance'
    geo_columns = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']

    df1['Distance'] = df1[geo_columns].apply(lambda x: haversine(
                                (x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                (x['Delivery_location_latitude'], x['Delivery_location_longitude'])
                            ), axis=1)


    df1 = df1.reset_index(drop=True)
    
    return df1


# ----------------------------------------------------------------------------------------------------------------------


def order_metric(df1):
    df_aux = df1[['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()
    fig = px.bar(df_aux, x='Order_Date', y='ID', labels={'ID': 'Deliveries by Day'})
    
    return fig


def traffic_order_share(df1):
    df_aux = df1[['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    df_aux['Delivery_perc'] = df_aux['ID'] / df_aux['ID'].sum()
    fig = px.pie(df_aux, values='Delivery_perc', names='Road_traffic_density')
    
    return fig


def traffic_order_city(df1):
    df_aux = df1[['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
    
    return fig


def order_by_week(df1):
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df_aux = df1[['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    fig = px.line(df_aux, x='week_of_year', y='ID')
    
    return fig


def order_by_delivery(df1):
    df_aux01 = df1[['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux02 = df1[['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()

    df_aux = pd.merge(df_aux01, df_aux02, how='inner')
    df_aux['Order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    fig = px.line(df_aux, x='week_of_year', y='Order_by_delivery')
    
    return fig


def country_map(df1):
    df_aux = ( df1[['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                    .groupby(['City', 'Road_traffic_density']).median().reset_index() )
    
    map_ = folium.Map()
    
    for index, location_info in df_aux.iterrows():

        folium.Marker([location_info['Delivery_location_latitude'], 
                       location_info['Delivery_location_longitude']],

                       popup=location_info[['City', 'Road_traffic_density']]).add_to(map_)
        
    return map_



def avg_delivery_by_city(df1):
    df_average_by_city = df1[['Time_taken(min)', 'City']].groupby('City').agg({'Time_taken(min)': ['mean', 'std']}).reset_index()
    df_average_by_city.columns = ['City', 'mean_delivery_time', 'std_delivery_time']

    fig = go.Figure()

    fig.add_trace(
        go.Bar( name='Control',
                x=df_average_by_city['City'],
                y=df_average_by_city['mean_delivery_time'],
                error_y=dict( type='data', array=df_average_by_city['std_delivery_time'] )
        )
    )

    fig.update_layout(barmode='group')
    
    return fig




def time_distribution_city(df1):
    avg_distance = df1[['City', 'Distance']].groupby('City').mean().reset_index()

    fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['Distance'], pull=[0.05, 0.1, 0])])
    
    return fig


def sunburn_graph(df1):
    df_aux = ( df1[['Time_taken(min)', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density'])
                                        .agg({'Time_taken(min)': ['mean', 'std']}) )

    df_aux.columns = ['mean_time', 'std_time']

    df_aux = df_aux.reset_index()

    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='mean_time',
                      color='std_time', color_continuous_scale='rdbu',
                      color_continuous_midpoint=np.average(df_aux['std_time']))
    
    return fig