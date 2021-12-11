from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

df_police = pd.read_csv('./Datasets/police.csv')
df_population = pd.read_csv('./Datasets/population.csv')
df_race = pd.read_csv('./Datasets/race.csv')

age_plot = px.histogram(data_frame=df_police, 
                        x='age', 
                        nbins=40)

