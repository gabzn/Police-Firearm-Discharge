from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from age_range import age_plot
from state import state_percentage_plot, state_total_plot
from race_pies import race_local_plot, race_global_plot
from weapon import weapon_plot
from map_plot import scatter_map_ratio_plot, scatter_map_total_plot
from zipcode import state_options, create_map_plot
import numpy as np
import dash_bootstrap_components as dbc

application = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], meta_tags=[{'name': 'viewport',
                   'content': 'width=device-width, initial-scale=1.0'}])
application.title = 'Police Firearm Discharge - Data Visualization'
application.config.suppress_callback_exceptions = True
server = application.server

# Create layouts for graphs
age_plot.update_layout(bargap=0.2, 
                       title={'text': '<b> Age Ranges </b>', 'y': 0.92, 'x': 0.5, 
                              'xanchor': 'center', 'yanchor': 'top'},
                       xaxis={'tickmode':'array', 'tickvals':np.arange(start=0, stop=120, step=5), 
                              'ticktext':np.arange(start=0, stop=100, step=5),
                              'title': 'Age', 'linecolor':'black', 'linewidth':1, 'mirror': True},
                       yaxis={'title': 'Count','linecolor':'black', 'linewidth':1, 'mirror': True},
                       font={'family': 'Arial', 'size': 13})

weapon_plot.update_layout(bargap=0.2, 
                          title={'text': '<b> Most Common Weapons Found </b>', 'y': 0.92, 'x': 0.5, 
                                 'xanchor': 'center', 'yanchor': 'top'},
                          xaxis={'categoryorder':'total descending', 'mirror':True,'linecolor':'black', 'linewidth':1},
                          yaxis={'linecolor':'black', 'linewidth':1, 'mirror': True},
                          font={'family': 'Arial', 'size': 13})
        
race_local_plot.update_layout(title={'text': "<b> Victims' Race Percentages Based on Our Dataset </b>", 
                                     'y': 0.93, 'x': 0.45, 'xanchor': 'center', 'yanchor': 'top'},
                              font={'family': 'Arial', 'size': 13},
                              margin=dict(b=20))

race_global_plot.update_layout(title={'text': "<b> Victims' Race Percentages Based on Population of Each Race </b>", 
                                      'y': 0.93, 'x': 0.45, 'xanchor': 'center', 'yanchor': 'top'},
                               font={'family': 'Arial', 'size': 13},
                               margin=dict(b=20)) 

state_percentage_plot.update_layout(bargap=0.2, title={'text': '<b> Shootings per 10,000 Population in Each State </b>', 
                                                       'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                                    xaxis={'categoryorder':'total descending','visible': True, 'title':''},
                                    font={'family': 'Arial', 'size': 13}, 
                                    margin=dict(b=0))           

state_total_plot.update_layout(bargap=0.2, title={'text': '<b> Total Shootings in Each State </b>', 
                                                  'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                               xaxis={'categoryorder':'total descending','visible': True, 'title':''},
                               font={'family': 'Arial', 'size': 13},
                               margin=dict(b=0))     

scatter_map_ratio_plot.update_layout(margin=dict(b=30, t=10))
scatter_map_total_plot.update_layout(margin=dict(b=30, t=10))

# Layout starts here
application.layout = dbc.Container([
    
    dbc.NavbarSimple(
        children=[dbc.NavItem(dbc.NavLink("Motivation & About", href="/about")),],
        brand="Police Firearm Discharge",
        brand_href="/",
        className='NavBar'
    ),

    dcc.Location(id='url', refresh=False, pathname='/'),
    
    dbc.Container(id='main_container')

], className='container-fliud')

main_page_layout = dbc.Container([
        
    dbc.Row([
        dbc.Col(dcc.Graph(id='age_plot',figure=age_plot),width={'size':'6'}),
        dbc.Col(dcc.Graph(id='weapon_plot', figure=weapon_plot), width={'size':'6'})
    ], className='age_and_weapon_row pb-4'),
  
    dbc.Row([
        dbc.Col(dcc.Graph(figure=race_local_plot), width={'size':'6'}),
        dbc.Col(dcc.Graph(figure=race_global_plot), width={'size':'6'})
    ], className='race_pie_plots_row pb-4'),

    dbc.Row(
        dbc.Col([
            dcc.Tabs(id="state_plots", value='View Percentages in Each State', children=[
                dcc.Tab(label='View Percentages in Each State', value='View Percentages in Each State'),
                dcc.Tab(label='View Total in Each State', value='View Total in Each State')
        ]),

        dcc.Graph(id='state_plot', figure={})]), 
    className='state_tabs_row'),

    dbc.Row(
        dbc.Col(dcc.Graph(id='scatter_map_ratio_plot', figure={}, className='pb-10. mb-20')),
    className='scatter_map_ratio_plot_row pb-4'),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='state_dropdown',options=state_options,placeholder='Select a state...',value='NY'),
            dcc.Graph(id='zipcode_map_plot',figure={})])], 
    class_name='zipcode_map_row pb-4')

], className='main_container')

about_page_layout = dbc.Container([
    
    dbc.Container(
        dbc.Row(
            dbc.Col([
                html.H3(html.U('Motivation Behind This Project'), className='text-center pt-3 pb-2'),
                html.H4("Police Shootings have been a very controversial topic in recent years. Every now and then we are witnessing police shootings across the United States, especially for the last few years. We have lost thousands of people’s lives in police altercation, and some victims were shot or killed with no valid reasons."),
                html.H4("We decided to name our project Police Firearm Discharge, and the project is inspired by the police altercations that happened with George Floyd back in 2020. Our goal and motivation behind this project is to raise awareness of police abuse of power.", 
                        className='mb-3 '),
            ], width={'size': '12'}),
        ),
    className='motivation_container'),

    dbc.Container(
        dbc.Row(
            dbc.Col([
                html.H3(html.U("Some Questions We'd Like to Answer in This Project"), className='text-center pt-3 pb-2'),
                html.Ol([
                    html.Li('What age range gets shot the most?'),
                    html.Li('What are some lethal weapons that police found?'),
                    html.Li('What are the percentages of each race getting shot?'),
                    html.Li('Which state has the highest level of police shootings per 10,000 population?')
                ], className='questions_list')
            ], width={'size': '12'})
        ),
    className='questions_container'),

    dbc.Container(
        dbc.Row([
            dbc.Col(
                html.H3(html.U("Datasets Used in This Project"), className='text-center pt-3 pb-2'),
            width={'size': '12'}),

            dbc.Col([
                html.H4('U.S Police Shootings 2013 - 2020'),
                html.H5(html.A('Source Can Be Found Here', href='https://www.kaggle.com/jamesvandenberg/us-police-shootings-20132020')),
                html.H5("Features include: victim's age, gender, race, state, city, alleged weapon and criminal charges.")
            ], width={'size': '4'}, className='police_dataset'),
            
            dbc.Col([
                html.H4('Census US Population by State'),
                html.H5(html.A('Source Can Be Found Here', href='https://www.kaggle.com/peretzcohen/2019-census-us-population-data-by-state')),
                html.H5("Features include: population in each state, states' latitude and longtitude.")
            ], width={'size': '4'}, className='population_dataset'),
            
            dbc.Col([
                html.H4('U.S. Census Bureau Race Origin 2020'),
                html.H5(html.A('Source Can Be Found Here', href='https://www.census.gov/quickfacts/fact/table/US/POP010220')),
                html.H5("Features include: percentage of each race in the US.")
            ], width={'size': '4'}, className='race_dataset')
        ]),
    className='datasets_container'),

    dbc.Container(
        dbc.Row([
            html.H3(html.U('Where to Find Me'), className='text-center pt-3 pb-2'),    
            
            dbc.Col(
                html.H4(html.A('GitHub', href='https://github.com/gabzn'), className='text-center')
            , width={'size': '6'}),

            dbc.Col(
                html.H4(html.A('LinkedIn', href='http://www.linkedin.com/in/gabrielzhen'), className='text-center')
            , width={'size': '6'})
        ]),
    className='dev_container'),

], className='about_container')

@application.callback([Output('state_plot', 'figure'),
               Output('scatter_map_ratio_plot', 'figure')],
               Input('state_plots', 'value'))
def render_state_plot(tab):
    if tab == 'View Percentages in Each State':
        return state_percentage_plot, scatter_map_ratio_plot
    elif tab == 'View Total in Each State':
        return state_total_plot, scatter_map_total_plot


@application.callback(Output('zipcode_map_plot', 'figure'),
                      Input('state_dropdown', 'value'),)
def render_zipcode_map(state):
    return create_map_plot(state)


@application.callback(Output('main_container', 'children'),
                      Input('url', 'pathname'))
def render_path(pathname):
    if pathname == '/':
        return main_page_layout
    elif pathname == '/about':
        return about_page_layout
    else:
        return main_page_layout
    
if __name__ == '__main__':
    # application.run_server(debug=True)
    application.run_server()