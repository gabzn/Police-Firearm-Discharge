import plotly.express as px
import pandas as pd

df_police = pd.read_csv('../Datasets/police.csv')
df_race = pd.read_csv('../Datasets/race.csv')

df_race_percentage_local = round((df_police['race'].value_counts().sort_values() / 9096) * 100, 2)
df_race_percentage_local = df_race_percentage_local.reset_index()
df_race_percentage_local.rename(columns={'index': 'race', 'race': 'percentage'}, inplace=True)


df_race_percentage_global = {'race': [], 'percentage': []}
for race, num_of_shooting in df_police['race'].value_counts().sort_values().iteritems():
    percentage_global = (num_of_shooting / (df_race.loc[df_race['race'] == race, 'population'].item())) * 100
    df_race_percentage_global['race'].append(race)
    df_race_percentage_global['percentage'].append(percentage_global)
df_race_percentage_global = pd.DataFrame.from_dict(df_race_percentage_global)


race_local_plot = px.pie(data_frame=df_race_percentage_local, names='race', values='percentage', color='race')
race_global_plot = px.pie(data_frame=df_race_percentage_global, names='race', values='percentage', color='race')
