import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import folium
# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})
year = list(map(str, range(2005, 2023)))

def compute_data_choice_1(df):
    # Cancellation Category Count
    bar_data = df.groupby(['Month','CancellationCode'])['Flights'].sum().reset_index()
    # Average flight time by reporting airline
    line_data = df.groupby(['Month','Reporting_Airline'])['AirTime'].mean().reset_index()
    # Diverted Airport Landings
    div_data = df[df['DivAirportLandings'] != 0.0]
    # Source state count
    map_data = df.groupby(['OriginState'])['Flights'].sum().reset_index()
    # Destination state count
    tree_data = df.groupby(['DestState', 'Reporting_Airline'])['Flights'].sum().reset_index()
    return [bar_data, line_data, div_data, map_data, tree_data]

def compute_info(df):
    # Select data
    # Compute delay averages
    avg_car = df.groupby(['Month','Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month','Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month','Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month','Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month','Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late

app = dash.Dash(__name__)
app.layout = html.Div(children=[ html.H1('US Domestic Airline Flights Performance', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 24}),
                                
                                
                                
                                
                                html.Div([
                                    
                                    html.Div([
                                         
                                        html.Div(
                                            [
                                            html.H2('Report Type:', style={'margin-right': '2em'})
                                            ]
                                        ),
                                       
                                        dcc.Dropdown(id='input-type',
                                                     options=[
                                                              {'label': 'Yearly Airline Performance Report', 'value': 'Yearly Airline Performance Report'},
                                                              {'label': 'Yearly Airline Delay Report', 'value': 'OPT2'}
                                                             ],
                                                     placeholder='Select a report type',
                                                     style={'width':'80%', 'padding':'3px', 'font-size':'20px', 'text-align-last':'center'}
                                                    )
                                    # Place them next to each other using the division style
                                            ], style={'display':'flex'})]),
                                
                                
                                
                                
                                
                                html.Div([
                                    
                                    html.Div([
                                         
                                        html.Div(
                                            [
                                            html.H2('Choose Year:', style={'margin-right': '2em'})
                                            ]
                                        ),
                                       
                                        dcc.Dropdown(id='input_year',
                                                     options=[
                                                              {'label': j, 'value': j } for i,j in enumerate(year)
                                                             ],
                                                     placeholder='Select a year',
                                                     style={'width':'80%', 'padding':'3px', 'font-size':'20px', 'text-align-last':'center'}
                                                    )
                                    # Place them next to each other using the division style
                                            ], style={'display':'flex'})]),
                                 html.Div(dcc.Graph(id='plot0'), style={'width':'64%'}),
                                
                                
                                
                                
                                
                                
                                html.Div([

                        html.Div(dcc.Graph(id='plot1')),
                        html.Div(dcc.Graph(id='plot2'))


                    ], style={'display': 'flex'}),
                    html.Div([

                        html.Div(dcc.Graph(id='plot3')),
                        html.Div(dcc.Graph(id='plot4'))


                    ], style={'display': 'flex'})
                                


    ])
                                
                                
                                
@app.callback([Output(component_id='plot0', component_property='figure'),
               Output(component_id='plot1', component_property='figure'),
               Output(component_id='plot2', component_property='figure'),
               Output(component_id='plot3', component_property='figure'),
               Output(component_id='plot4', component_property='figure')
               ],
               [
                Input(component_id='input_year', component_property='value'),
                Input(component_id='input-type', component_property='value'),
               ])








def get_dash(value,value1):
    df =  airline_data[airline_data['Year']==int(value)]
    print(value, value1)
    if value1 == 'Yearly Airline Performance Report':
        avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(df)
        carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline', title='Average carrrier delay time (minutes) by airline')
    # Line plot for weather delay
        weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline', title='Average weather delay time (minutes) by airline')
        # Line plot for nas delay
        nas_fig = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline', title='Average NAS delay time (minutes) by airline')
        # Line plot for security delay
        sec_fig = px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline', title='Average security delay time (minutes) by airline')
        # Line plot for late aircraft delay
        late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline', title='Average late aircraft delay time (minutes) by airline')

        return[carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]
    else:
        bar_data, line_data, div_data, map_data, tree_data = compute_data_choice_1(df)
            
            # Number of flights under different cancellation categories
        bar_fig = px.bar(bar_data, x='Month', y='Flights', color='CancellationCode', title='Monthly Flight Cancellation')
            
            # TODO5: Average flight time by reporting airline
        line_fig = px.line(line_data, x='Month', y='AirTime', color='Reporting_Airline', title='Average monthly flight time (minutes) by airline')
            
            # Percentage of diverted airport landings per reporting airline
        pie_fig = px.pie(div_data, values='Flights', names='Reporting_Airline', title='% of flights by reporting airline')
        
        tree_fig = px.treemap(tree_data, path=['DestState', 'Reporting_Airline'], 
                      values='Flights',
                      color='Flights',
                      color_continuous_scale='RdBu',
                      title='Flight count by airline to destination state'
                )
        map_fig = px.choropleth(map_data,  # Input data
                    locations='OriginState', 
                    color='Flights',  
                    hover_data=['OriginState', 'Flights'], 
                    locationmode = 'USA-states', # Set to plot as USA States
                    color_continuous_scale='GnBu',
                    range_color=[0, map_data['Flights'].max()]) 
        map_fig.update_layout(
                    title_text = 'Number of flights from origin state', 
                    geo_scope='usa') # Plot only the USA instead of globe 
        
        return [tree_fig, pie_fig, map_fig, bar_fig, line_fig]
        
        
        
        
    
    






    
if __name__ == '__main__':
    app.run_server()

                           
                 
                                
                                
                                
                                
                                


