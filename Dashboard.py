import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash(__name__)

spacex_df =  pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv", 
                            encoding = "ISO-8859-1",
                            )

app.layout = html.Div([
       html.H1('SpaceX Lauch Records Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 24}),
       
     html.Div([               
                    dcc.Dropdown(
                            id='my_dropdown',
                            options=[
                            {'label' : 'ALL sites', 'value' : 'ALL'},
                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                            ],
                            value='ALL',
                            placeholder="Choose a chart",
                            searchable=True
                            ),
     ]),
         html.Div([
             dcc.Graph(id='success-pie-chart')
         ]),
         html.H4("Payload range (kg)"),
         html.Div([             
                dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0', 100: '100'},
                value=[spacex_df["Payload Mass (kg)"].min(), spacex_df["Payload Mass (kg)"].max()])
         ]),	
         html.Div([
             dcc.Graph(id='success-payload-scatter-chart')
         ]),						
     ])

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
               [Input(component_id='my_dropdown', component_property='value')])
def display_pie_chart(my_dropdown):
    if my_dropdown == 'ALL':
        filtered_df = spacex_df
        fig1 = px.pie(filtered_df, values='class', names='Launch Site', title="Success Pie Chart")
        return fig1

    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==my_dropdown].groupby('class', as_index=False).mean()
        fig1 = px.pie(filtered_df, values='Unnamed: 0', names='class', title="Success Pie Chart")
        return fig1
        
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='my_dropdown', component_property='value')])
def display_scatter_plot(my_dropdown):
    if my_dropdown == 'ALL':
        fig2 = px.scatter(spacex_df, x = "Payload Mass (kg)", y = 'class', hover_name="Payload Mass (kg)",
        title="Correlation between Payload and Success for all sites", color="Booster Version")  
        return fig2
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==my_dropdown]
        fig2 = px.scatter(filtered_df, x = "Payload Mass (kg)", y = 'class', hover_name="Payload Mass (kg)",
        title="Correlation between Payload and Success", color="Booster Version")  
        return fig2
    


if __name__ == '__main__':
    app.run_server()