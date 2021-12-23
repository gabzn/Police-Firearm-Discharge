import plotly.express as px
import pandas as pd
from state import df_state, df_state_shooting_percentages

df_population = pd.read_csv('./Datasets/population.csv')

df_shootings = df_population.copy()
df_shootings['total_shootings'] = 0
df_shootings['percentage'] = 0

for state in df_state['state']:
    total_shootings = df_state.loc[df_state['state'] == state, 'num_of_shootings'].item()
    percentage = df_state_shooting_percentages.loc[df_state_shooting_percentages['state'] == state, 'percentage'].item()
    df_shootings.loc[df_shootings['abbreviation'] == state, 'total_shootings'] = total_shootings
    df_shootings.loc[df_shootings['abbreviation'] == state, 'percentage'] = percentage
 
scatter_map_ratio_plot = px.scatter_mapbox(df_shootings, 
                                     lat='lat', 
                                     lon='long', 
                                     hover_name='state',
                                     hover_data={'lat': False, 'long': False, 'population': True},
                                     labels={'percentage': 'Shootings per 10000','population': 'Population'},
                                     mapbox_style='open-street-map',
                                     center={'lat':39.048191, 'lon':-95.677956},
                                     zoom=3,
                                     size='percentage',
                                     color='percentage',
                                     color_continuous_scale='portland',
                                     opacity=0.8,
                                     height=500)

scatter_map_total_plot = px.scatter_mapbox(df_shootings, 
                                     lat='lat', 
                                     lon='long', 
                                     hover_name='state',
                                     hover_data={'lat': False, 'long': False, 'population': True},
                                     labels={'total_shootings': 'Total Shootings','population': 'Population'},
                                     mapbox_style='open-street-map',
                                     center={'lat':39.048191, 'lon':-95.677956},
                                     zoom=3,
                                     size='total_shootings',
                                     color='total_shootings',
                                     color_continuous_scale='portland',
                                     opacity=0.8,
                                     height=500)        