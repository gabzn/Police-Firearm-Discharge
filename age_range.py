import plotly.express as px
import pandas as pd

df_police = pd.read_csv('./Datasets/police.csv')

age_plot = px.histogram(data_frame=df_police, x='age', nbins=40)