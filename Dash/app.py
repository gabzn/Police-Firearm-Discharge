from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from age_range import age_plot
from percentage import percentage_plot
from race_pies import race_local_plot, race_global_plot
from weapon import weapon_plot
from map_plot import scatter_map_plot
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], meta_tags=[{'name': 'viewport',
                                                                           'content': 'width=device-width, initial-scale=1.0'}])
app.title = 'Police Firearm Discharge - Data Visualization'

# Read in all the dataframes
df_police = pd.read_csv('../Datasets/police.csv')
df_population = pd.read_csv('../Datasets/population.csv')
df_race = pd.read_csv('../Datasets/race.csv')

# Create layouts for graphs
age_plot.update_layout(bargap=0.2, 
                       title={'text': 'Age Ranges', 'y': 0.9, 'x': 0.5, 
                              'xanchor': 'center', 'yanchor': 'top'},
                       xaxis={'tickmode':'array', 'tickvals':np.arange(start=0, stop=120, step=5), 'ticktext':np.arange(start=0, stop=100, step=5)})

percentage_plot.update_layout(bargap=0.1, title={'text': 'Shootings per 10,000 Population in Each State', 
                                          'y': 0.9, 'x': 0.5, 
                                          'xanchor': 'center', 
                                          'yanchor': 'top'})                        

race_local_plot.update_layout(bargap=0.1, title={'text': 'Race Percentages Based on 9000+ Victims', 
                                          'y': 0.9, 'x': 0.5, 
                                          'xanchor': 'center', 
                                          'yanchor': 'top'})

race_global_plot.update_layout(bargap=0.1, title={'text': 'Race Percentages Based on Population of Each Race', 
                                          'y': 0.9, 'x': 0.5, 
                                          'xanchor': 'center', 
                                          'yanchor': 'top'}) 

weapon_plot.update_layout(bargap=0.1, title={'text': 'Most Common Weapons Found', 'y': 0.9, 'x': 0.5, 
                                          'xanchor': 'center', 'yanchor': 'top'})


# Layout starts here
app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(html.H1('Police Firearm Discharge', className='text-center text-white'))
    ),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='age_plot',figure=age_plot), 
        ], width={'size':'6'}),

        dbc.Col([
            dcc.Graph(id='race_local_plot',figure=race_local_plot),
        ], width={'size':'6'})
    ], className='age_and_race_row pb-3'),
  
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='percentage_plot', figure=percentage_plot)
        ])
    ], className='percentage_plot_row pb-3'),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='weapon_plot', figure=weapon_plot)
        ])
    ], className='weapon_plot_row pb-3'),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='scatter_map_plot', figure=scatter_map_plot)
        ])
    ], className='scatter_map_plot_row pb-3'),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='race_global_plot', figure=race_global_plot)
        ])
    ], className='race_global_plot_row pb-3'),

], className='container-fliud')


if __name__ == '__main__':
    app.run_server(debug=True)