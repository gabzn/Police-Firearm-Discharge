from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], meta_tags=[{'name': 'viewport',
                                                                           'content': 'width=device-width, initial-scale=1.0'}])

# Read in all the dataframes
df_police = pd.read_csv('../Datasets/police.csv')
df_population = pd.read_csv('../Datasets/population.csv')
df_race = pd.read_csv('../Datasets/race.csv')

population_dict = {}
for city, num in zip(df_population['abbreviation'], df_population['population'] / 10000):
    population_dict[city] = num

percentage_dict = {'state': [], 'percentage': [], 'state_name': []}
for city in population_dict:
    percentage = df_police['state'].value_counts()[city] / population_dict[city] * 100
    percentage = round(percentage)
    percentage_dict['state'].append(city)
    percentage_dict['percentage'].append(percentage)

for state in df_population['state']:
    percentage_dict['state_name'].append(state)

df_percentage = pd.DataFrame.from_dict(percentage_dict)

weapon_dict = {
    'weapon':['gun', 'knife', 'toy gun', 'baseball bat', 'hammer', 'ax', 'crossbow'],
    'count': [4847, 1193, 268, 431, 604, 242, 101]
}
df_weapon = pd.DataFrame.from_dict(weapon_dict)

race_series = round((df_police['race'].value_counts().sort_values() / 9096) * 100, 2)
race_series = race_series.reset_index()
race_series.rename(columns={'index': 'race', 'race': 'percentage'}, inplace=True)

# Create all the graphs 
age_plot = px.histogram(data_frame=df_police, 
                        x='age', 
                        nbins=40, 
                        labels={'age':'Age'})
                        # color_discrete_sequence=px.colors.qualitative.Bold)
age_plot.update_layout(bargap=0.1, 
                       title={'text': 'Age Ranges', 'y': 0.9, 'x': 0.5, 
                              'xanchor': 'center', 'yanchor': 'top'},
                       xaxis={'tickmode':'array', 'tickvals':np.arange(start=0, stop=100, step=5), 'ticktext':np.arange(start=0, stop=100, step=5)})

percentage_plot = px.bar(data_frame=df_percentage, x='state', y='percentage',
                        labels={'state':'States', 'percentage':'Number of Shootings per 10,000'},
                        color_discrete_sequence=px.colors.qualitative.Bold,
                        hover_data=['state_name'])
percentage_plot.update_layout(bargap=0.1, title={'text': 'Shootings per 10,000 Population in Each State', 
                                          'y': 0.9, 'x': 0.5, 
                                          'xanchor': 'center', 
                                          'yanchor': 'top'})                        

race_plot = px.pie(data_frame=race_series, names='race', values='percentage', color='race')
race_plot.update_layout(bargap=0.1, title={'text': 'Race-Shot Percentages Based on 9000 Victims', 
                                          'y': 0.9, 'x': 0.5, 
                                          'xanchor': 'center', 
                                          'yanchor': 'top'}) 

weapon_plot = px.bar(data_frame=df_weapon, 
                        x='weapon', y='count',
                        labels={'weapon':'Weapons', 'count': 'Total Number of Each Weapon'})
                        # color_discrete_sequence=px.colors.qualitative.Bold)
weapon_plot.update_layout(bargap=0.1, title={'text': 'Most Common Weapons Found', 'y': 0.9, 'x': 0.5, 
                                          'xanchor': 'center', 'yanchor': 'top'})

scatter_map_plot = px.scatter_mapbox(df_population, 
                                     lat=df_population['lat'], 
                                     lon=df_population['long'], 
                                     hover_name=df_population['state'],
                                     mapbox_style='carto-positron',
                                     width=1000, height=500,
                                     center={'lat':39.048191, 'lon':-95.677956},
                                     zoom=3)

# Layout starts here
app.layout = dbc.Container(children=[

    dbc.Row(
        dbc.Col(html.H1('Police Firearm Discharge', className='text-center bg-dark text-white'))
    ),

    dbc.Row(children=[
        dbc.Col([
            dcc.Graph(id='age_plot',figure=age_plot), 
        ], width={'size':'6'}),

        dbc.Col([
            dcc.Graph(id='race_plot',figure=race_plot),
        ], width={'size':'6'})
    ], className='age_and_race_row'),
  
    # dbc.Container(children=[
    #     dcc.Graph(
    #         id='race_plot',
    #         figure=race_plot
    #     ),
    # ], className='race_plot_container'),

    dbc.Container(children=[
        dcc.Graph(
            id='percentage_plot',
            figure=percentage_plot
        )
    ], className='percentage_plot_container'),

    dbc.Container(children=[
        dcc.Graph(
            id='weapon_plot',
            figure=weapon_plot
        )
    ], className='weapon_plot_container'),


    dbc.Container(children=[
        dcc.Graph(
            id='scatter_map_plot',
            figure=scatter_map_plot
        )
    ], className='scatter_map_plot_container')

], className='main_container')



if __name__ == '__main__':
    app.run_server(debug=True)