import plotly.express as px
import pandas as pd
import numpy as np
from state import df_percentage

df_s = pd.read_csv('./Datasets/police.csv')
df_zipcode = pd.read_csv('./Datasets/zip_lat_long.csv')

def format_zipcode(df):
    def append_and_format(num):
        num = str(num)
        while len(num) != 5:
            num = '0'+num
        return num
    
    df['new_zipcode'] = df['zipcode'].apply(append_and_format)
    df.drop(labels='zipcode', axis=1, inplace=True)
    df.rename(columns={'new_zipcode':'zipcode'}, inplace=True)




def create_map_plot(state):
    df_lats_longs = {'lats': [], 'longs': [], 'count': [], 'zipcode': [], 'city': []}
    holders = {}

    for zipcode in df_s[df_s['state'] == state]['zipcode']:
        try:
            lat = df_zipcode.loc[df_zipcode['zipcode'] == zipcode, 'lat'].item()
            long = df_zipcode.loc[df_zipcode['zipcode'] == zipcode, 'long'].item()
            k = str(lat) + ',' + str(long)
            if k in holders:
                holders[k] += 1
            else:
                holders[k] = 1
                df_lats_longs['zipcode'].append(zipcode)
                df_lats_longs['city'].append(df_s.loc[df_s['zipcode'] == zipcode, 'city'].tolist()[0])
        except:
            pass
        

    for k, value in holders.items():
        k = k.split(',')
        lat = float(k[0])
        long = float(k[1])
        df_lats_longs['lats'].append(lat)
        df_lats_longs['longs'].append(long)
        df_lats_longs['count'].append(value)
    
    
    df_lats_longs = pd.DataFrame.from_dict(df_lats_longs)
    
    zipcode_map_plot = px.scatter_mapbox(df_lats_longs, 
                                      lat='lats',
                                      lon='longs',
                                      mapbox_style='open-street-map',
                                      hover_name=[state for x in range(len(df_lats_longs))],
                                      hover_data={'lats': False, 'longs':False, 'count': True, 'zipcode':True, 'city':True},
                                      labels={'count': 'Count', 'zipcode': 'Zipcode', 'city': 'City'},
                                      zoom=6,
                                      opacity=0.7,
                                      size='count',
                                      color='count',
                                      color_continuous_scale='portland')
    return zipcode_map_plot



format_zipcode(df_s)
format_zipcode(df_zipcode)
state_options = [{'label': df_percentage.loc[df_percentage['state'] == x, 'state_name'].item(), 'value': x} for x in np.sort(df_s['state'].unique())]