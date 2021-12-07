from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

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
age_plot.update_layout(bargap=0.1, title={'text': 'Age Ranges', 'y': 0.9, 'x': 0.5, 
                                          'xanchor': 'center', 'yanchor': 'top'})

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
                                          'y': 1, 'x': 0.5, 
                                          'xanchor': 'center', 
                                          'yanchor': 'top'}) 

weapon_plot = px.bar(data_frame=df_weapon, 
                        x='weapon', y='count',
                        labels={'weapon':'Weapons', 'count': 'Total Number of Each Weapon'})
                        # color_discrete_sequence=px.colors.qualitative.Bold)
weapon_plot.update_layout(bargap=0.1, title={'text': 'Most Common Weapons Found', 'y': 0.9, 'x': 0.5, 
                                          'xanchor': 'center', 'yanchor': 'top'})


# Layout starts here
app.layout = html.Div(children=[

    dbc.Row(
        dbc.Col(html.H1('Police Firearm Discharge', className='text-center'))
    ),

    html.Div(children=[
        dcc.Graph(
            id='age_plot',
            figure=age_plot
        ),
    ], className='age_plot_container'),
  
    html.Div(children=[
        dcc.Graph(
            id='race_plot',
            figure=race_plot
        ),
    ], className='race_plot_container'),

    html.Div(children=[
        dcc.Graph(
            id='percentage_plot',
            figure=percentage_plot
        )
    ], className='percentage_plot_container'),

    html.Div(children=[
        dcc.Graph(
            id='weapon_plot',
            figure=weapon_plot
        )
    ], className='weapon_plot_container')

], className='main_container')



if __name__ == '__main__':
    app.run_server(debug=True)