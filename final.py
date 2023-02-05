import pandas as pd
import plotly.graph_objects as go
import dash
from dash import *
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import folium

spacex_df = pd.read_csv('./spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)
app.layout = html.Div(children=[ html.H1('SpaceX Launch Records Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 40}),
                                html.Div([dcc.Dropdown(id='site-dropdown',
                                                       options=[ {'label': 'All Sites', 'value': 'ALL'},
                                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                                ],
                                                       value='ALL',
                                                       placeholder='Select a Launch Site here',
                                                       searchable=True,
                                                       style={'width':'80%', 'padding':'3px', 'font-size':'20px', 'text-align-last':'center'}
                                                       
                                                       )]),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart'), style={'width':'100%'}),
                                html.Br(),
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=1000000,
                                                step=1000,
                                                value=[min_payload, max_payload]
                                                ),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                
                                
                                ])


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(value1):
    filtered_df = spacex_df
    if value1 == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title=f"Total Success Launches for site {value1}")
        return fig
    else:
        filtered_df=spacex_df[spacex_df['Launch Site']== value1]
        filtered_df=filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig=px.pie(filtered_df,values='class count',names='class',title=f"Total Success Launches for site {value1}")
        return fig
        
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])

def get_pie_chart(value, value1):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(value1[0],value1[1])]
    if value=='ALL':
        fig=px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Success count on Payload mass for all sites')
        return fig
    else:
        fig=px.scatter(filtered_df[filtered_df['Launch Site']==value],x='Payload Mass (kg)',y='class',color='Booster Version Category',title=f"Success count on Payload mass for site ")
        return fig


if __name__ == '__main__':
    app.run_server()
