from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from age_range import age_plot
from state import state_percentage_plot, state_total_plot
from race_pies import race_local_plot, race_global_plot
from weapon import weapon_plot
from map_plot import scatter_map_ratio_plot, scatter_map_total_plot
import numpy as np
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], meta_tags=[{'name': 'viewport',
                                                                           'content': 'width=device-width, initial-scale=1.0'}])
app.title = 'Police Firearm Discharge - Data Visualization'

# Create layouts for graphs
age_plot.update_layout(bargap=0.2, 
                       title={'text': '<b> Age Ranges </b>', 'y': 0.92, 'x': 0.5, 
                              'xanchor': 'center', 'yanchor': 'top'},
                       xaxis={'tickmode':'array', 'tickvals':np.arange(start=0, stop=120, step=5), 
                              'ticktext':np.arange(start=0, stop=100, step=5),
                              'title': 'Age', 'linecolor':'black', 'linewidth':1, 'mirror': True},
                       yaxis={'title': 'Count','linecolor':'black', 'linewidth':1, 'mirror': True},
                       font={'family': 'Arial', 'size': 13},
                       )

weapon_plot.update_layout(bargap=0.2, title={'text': '<b> Most Common Weapons Found </b>', 'y': 0.92, 'x': 0.5, 
                                          'xanchor': 'center', 'yanchor': 'top'},
                                          xaxis={'categoryorder':'total descending', 'mirror':True,
                                                 'linecolor':'black', 'linewidth':1},
                                          yaxis={'linecolor':'black', 'linewidth':1, 'mirror': True},
                                          font={'family': 'Arial', 'size': 13})
        
race_local_plot.update_layout(title={'text': '<b> Race Percentages Based on Our Dataset </b>', 
                                          'y': 0.93, 'x': 0.45, 
                                          'xanchor': 'center', 
                                          'yanchor': 'top'},
                             font={'family': 'Arial', 'size': 13})

race_global_plot.update_layout(title={'text': '<b> Race Percentages Based on Population of Each Race </b>', 
                                          'y': 0.93, 'x': 0.45, 
                                          'xanchor': 'center', 
                                          'yanchor': 'top'},
                                          font={'family': 'Arial', 'size': 13}) 

state_percentage_plot.update_layout(bargap=0.2, title={'text': '<b> Shootings per 10,000 Population in Each State </b>', 
                                          'y': 0.95, 'x': 0.5, 
                                          'xanchor': 'center', 
                                          'yanchor': 'top'},
                                          xaxis={'categoryorder':'total descending','visible': False},
                                          font={'family': 'Arial', 'size': 13}, 
                                          margin=dict(b=0))           

state_total_plot.update_layout(bargap=0.2, title={'text': '<b> Total Shootings in Each State </b>', 
                                          'y': 0.95, 'x': 0.5, 
                                          'xanchor': 'center', 
                                          'yanchor': 'top'},
                                          xaxis={'categoryorder':'total descending','visible': False},
                                          font={'family': 'Arial', 'size': 13},
                                          margin=dict(b=0))     

scatter_map_ratio_plot.update_layout(margin=dict(b=50))
scatter_map_total_plot.update_layout(margin=dict(b=50))

# Layout starts here
app.layout = dbc.Container([

    dbc.Row(dbc.Col(html.H1('Police Firearm Discharge', className='text-center text-white')), class_name='pb-2'),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='age_plot',figure=age_plot), 
        ], width={'size':'6'}),

        dbc.Col([
            dcc.Graph(id='weapon_plot', figure=weapon_plot)
        ], width={'size':'6'})
    ], className='age_and_weapon_row pb-4'),
  
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=race_local_plot), 
        ], width={'size':'6'}),

        dbc.Col([
            dcc.Graph(figure=race_global_plot)
        ], width={'size':'6'})
    ], className='race_pie_plots_row pb-4'),

    dbc.Row([
        dbc.Col([
            dcc.Tabs(id="state_plots", value='View Percentages in Each State', children=[
                dcc.Tab(label='View Percentages in Each State', value='View Percentages in Each State'),
                dcc.Tab(label='View Total in Each State', value='View Total in Each State'),
            ]),

            dcc.Graph(id='state_plot', figure={})
        ]),
    ], className='state_tabs_row'),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='scatter_map_ratio_plot', figure={}, className='pb-10. mb-20')
        ])
    ], className='scatter_map_ratio_plot_row pb-4'),

], className='container-fliud')

@app.callback([Output('state_plot', 'figure'),
               Output('scatter_map_ratio_plot', 'figure')],
               Input('state_plots', 'value'))
def render_state_plot(tab):
    if tab == 'View Percentages in Each State':
        return state_percentage_plot, scatter_map_ratio_plot
    elif tab == 'View Total in Each State':
        return state_total_plot, scatter_map_total_plot

if __name__ == '__main__':
    app.run_server(debug=True)