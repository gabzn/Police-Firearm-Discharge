from dash import Dash, dcc, html
from dash.dependencies import Input, Output
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


df_race_percentage_local = round((df_police['race'].value_counts().sort_values() / 9096) * 100, 2)
df_race_percentage_local = df_race_percentage_local.reset_index()
df_race_percentage_local.rename(columns={'index': 'race', 'race': 'percentage'}, inplace=True)


df_race_percentage_global = {'race': [], 'percentage': []}
for race, num_of_shooting in df_police['race'].value_counts().sort_values().iteritems():
    percentage_global = (num_of_shooting / (df_race.loc[df_race['race'] == race, 'population'].item())) * 100
    df_race_percentage_global['race'].append(race)
    df_race_percentage_global['percentage'].append(percentage_global)
df_race_percentage_global = pd.DataFrame.from_dict(df_race_percentage_global)


# Create all the graphs 
age_plot = px.histogram(data_frame=df_police, 
                        x='age', 
                        nbins=40, 
                        labels={'age':'Age'})
                        # color_discrete_sequence=px.colors.qualitative.Bold)
age_plot.update_layout(bargap=0.2, 
                       title={'text': 'Age Ranges', 'y': 0.9, 'x': 0.5, 
                              'xanchor': 'center', 'yanchor': 'top'},
                       xaxis={'tickmode':'array', 'tickvals':np.arange(start=0, stop=120, step=5), 'ticktext':np.arange(start=0, stop=100, step=5)})

percentage_plot = px.bar(data_frame=df_percentage, x='state', y='percentage',
                        labels={'state':'States', 'percentage':'Number of Shootings per 10,000'},
                        color_discrete_sequence=px.colors.qualitative.Bold,
                        hover_data=['state_name'])
percentage_plot.update_layout(bargap=0.1, title={'text': 'Shootings per 10,000 Population in Each State', 
                                          'y': 0.9, 'x': 0.5, 
                                          'xanchor': 'center', 
                                          'yanchor': 'top'})                        

race_local_plot = px.pie(data_frame=df_race_percentage_local, names='race', values='percentage', color='race')
race_local_plot.update_layout(bargap=0.1, title={'text': 'Race Percentages Based on 9000+ Victims', 
                                          'y': 0.9, 'x': 0.5, 
                                          'xanchor': 'center', 
                                          'yanchor': 'top'})

race_global_plot = px.pie(data_frame=df_race_percentage_global, names='race', values='percentage', color='race')
race_global_plot.update_layout(bargap=0.1, title={'text': 'Race Percentages Based on Population of Each Race', 
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
                                     lat='lat', 
                                     lon='long', 
                                     hover_name='state',
                                     mapbox_style='carto-positron',
                                    #  width=1000, height=500,
                                     center={'lat':39.048191, 'lon':-95.677956},
                                     zoom=3)

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


    # dbc.Row([
    #     dbc.Col([
    #         dcc.Tabs(id="race_pie_plots", value='View Race Percentages in Our Dataset', children=[
    #             dcc.Tab(label='View Race Percentages in Our Dataset', value='View Race Percentages in Our Dataset'),
    #             dcc.Tab(label='View Race Percentages in The Total Population', value='View Race Percentages in The Total Population'),
    #         ]),

    #         dcc.Graph(id='race_pie_plot', figure={})
    #     ]),
    # ], className='race_tabs_row pb-3'),

    # @app.callback(Output('race_pie_plot', 'figure'),
#               Input('race_pie_plots', 'value'))
# def render_state_plot(tab):
#     if tab == 'View Race Percentages in Our Dataset':
#         return race_local_plot
#     elif tab == 'View Race Percentages in The Total Population':
#         return race_global_plot