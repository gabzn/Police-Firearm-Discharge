import plotly.express as px
import pandas as pd

df_police = pd.read_csv('../Datasets/police.csv')

# Find the total number of unarmed people and people who carried non-lethal weapon.

weapon_dict = {
    'weapon':['Gun', 'Knife', 'Toy gun', 'Baseball Bat', 'Hammer', 'Ax', 'Crossbow'],
    'count': [4847, 1193, 268, 431, 604, 242, 101]
}

df_weapon = pd.DataFrame.from_dict(weapon_dict)

weapon_plot = px.bar(data_frame=df_weapon, 
                        x='weapon', y='count',
                        labels={'weapon':'Weapons', 'count': 'Total Number of Each Weapon'})