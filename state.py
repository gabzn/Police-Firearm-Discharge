import plotly.express as px
import pandas as pd

df_police = pd.read_csv('./Datasets/police.csv')
df_population = pd.read_csv('./Datasets/population.csv')

df_state = df_police['state'].value_counts().reset_index()
df_state.rename(columns={'index': 'state', 'state': 'num_of_shootings'}, inplace=True)

state_shootings_percentage_dict = {'state': [], 'state_name': [], 'percentage': []}
for state in df_population['abbreviation']:
    state_name = df_population.loc[df_population['abbreviation'] == state, 'state'].item()
    state_shootings_percentage_dict['state_name'].append(state_name)
    state_shootings_percentage_dict['state'].append(state)
    
    total_shootings_in_state = df_police['state'].value_counts()[state]
    population_per_10000_in_state = df_population.loc[df_population['abbreviation'] == state, 'population'].item() / 10000
    
    percentage_per_10000_in_state = (total_shootings_in_state / population_per_10000_in_state) * 100
    percentage_per_10000_in_state = round(percentage_per_10000_in_state)
    state_shootings_percentage_dict['percentage'].append(percentage_per_10000_in_state)
df_state_shooting_percentages = pd.DataFrame.from_dict(state_shootings_percentage_dict)

state_total_plot = px.bar(data_frame=df_state, x='state', y='num_of_shootings',
                          labels={'state': 'State', 'num_of_shootings': 'Number of Shootings'},
                          hover_name='state')

state_percentage_plot = px.bar(data_frame=df_state_shooting_percentages, x='state', y='percentage',
                               labels={'state': 'State', 'percentage':'Number of Shootings per 10,000 Pop'},
                               hover_name='state_name')