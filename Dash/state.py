from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

df_police = pd.read_csv('../Datasets/police.csv')
df_population = pd.read_csv('../Datasets/population.csv')
df_race = pd.read_csv('../Datasets/race.csv')



# Include the total number of population in that state.
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

df_state = df_police['state'].value_counts().reset_index()
df_state.rename(columns={'index': 'state', 'state': 'num_of_shootings'}, inplace=True)



state_percentage_plot = px.bar(data_frame=df_percentage, x='state', y='percentage',
                        labels={'state': 'States', 'percentage':'Number of Shootings per 10,000 Pop'},
                        color_discrete_sequence=px.colors.qualitative.Bold,
                        hover_data=['state_name'])


state_total_plot = px.bar(data_frame=df_state, x='state', y='num_of_shootings',
                          labels={'state': 'States', 'num_of_shootings': 'Number of Shootings'},
                          color_discrete_sequence=px.colors.qualitative.Bold)