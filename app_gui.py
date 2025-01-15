import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json
from dash.dependencies import Output, Input
from app_data import *
from sensorcar import *
import numpy as np

car = SensorCar()

# Konfigurationslogik
try:
    with open("config.json", "r") as f:
        data = json.load(f)
        ip_host = data.get("ip_host", "0.0.0.0")  # Fallback zu "0.0.0.0"
except FileNotFoundError:
    print("Fehler: config.json nicht gefunden. Standardwerte werden verwendet.")
    ip_host = "0.0.0.0"

# Dash-App erstellen
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

#Setzt Variable am Anfang auf 1
f_id = 1
# App-Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Fahrmodus-Dashboard", className="text-center"), width=12)),

    dbc.Row([
        dbc.Col([
            html.H4("Fahrtauswahl:"),
            dcc.Dropdown(
                id='fahrt-dropdown',
                options=[{'label': f'Fahrt {fahrt_id}', 'value': fahrt_id} for fahrt_id in df['FahrtID'].unique()],
                value=df['FahrtID'].unique()[0],  # Standardauswahl
                clearable=False,
                className="mb-4"
            ),
        ], width=12),
    ], className="mb-4"),

        dbc.Row(
            [
            dbc.Card(                
                dbc.CardBody(
                    children=[
                        html.P("Geschwindigkeit min:"),
                        html.P(f"{result_df['Vmin'].iloc[0]:.1f} km/h", id="Vmin"),
                    ]
                ),
                style={'width': '14rem', 'margin': '15px'}
                ),
            dbc.Card(                                
                dbc.CardBody(
                    children=[
                        html.P("Geschwindigkeit max:"),
                        html.P(f"{result_df['Vmax'].iloc[0]:.1f} km/h", id="Vmax"),
                    ]
                ),
                style={'width': '14rem', 'margin': '15px', 'padding' : '0px'}
                ),  
            dbc.Card(                                
                dbc.CardBody(
                    children=[
                        html.P("Geschwindigkeit mean:"),
                        html.P(f"{result_df['Vmean'].iloc[0]:.1f} km/h", id="Vmean"),
                    ]
                ),
                style={'width': '14rem', 'margin': '15px'}
                ),  
            dbc.Card(                                
                dbc.CardBody(
                    children=[
                        html.P("Fahrstrecke:"),
                        html.P(f"{result_df['Fahrstrecke'].iloc[0]:.1f} mm", id="Fahrstrecke"),
                    ]
                ),
                style={'width': '14rem', 'margin': '15px'}
                ),     
            dbc.Card(                                
                dbc.CardBody(
                    children=[
                        html.P("Fahrzeit:"),
                        html.P(f"{result_df['Fahrzeit'].iloc[0]:.1f} s", id="Fahrzeit"),
                    ]
                ),
                style={'width': '14rem', 'margin': '15px'}
                ),     
            dbc.Card(                                
                dbc.CardBody(
                    children=[
                        html.P("Fahrmodus:"),
                        html.P(f"{result_df['Fahrmodus'].iloc[0]:.1f} s", id="Fahrmodus"),
                    ]
                ),
                style={'width': '14rem', 'margin': '15px'}
                ),                   
            dbc.Card(   
                dbc.CardBody(
                    children=[
                        dbc.Button('Kalibrierung!', id='btCali', n_clicks=0),
                        html.Div(id='cali_value')
                    ] 
                ),
                style={'width': '24rem', 'margin': '15px'}                                            
                )                                                                    

            ],                                          
                className="mb-4"       
    ),
        dbc.Row(
            [   
            dbc.Card(   
                dbc.CardBody(
                    dbc.ButtonGroup(
                        [dbc.Button("Fahrmodus 1", id='btFM1'), 
                         dbc.Button("Fahrmodus 2", id='btFM2'), 
                         dbc.Button("Fahrmodus 3", id='btFM3'), 
                         dbc.Button("Fahrmodus 4", id='btFM4'), 
                         dbc.Button("Fahrmodus 5", id='btFM5'), 
                         dbc.Button("Fahrmodus 6", id='btFM6'), 
                         dbc.Button("Fahrmodus 7", id='btFM7'), 
                         dbc.Button("STOPP", id='btStopp')],
                        size="lg",
                        className="me-1",
                    ),
                ),
                style={'width': '90%', 'margin-left': 'auto', 'margin-right': 'auto','margin': '15px'}                                            
                )                                                                    
            ],                                          
                className="mb-4"       
    ),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='geschwindigkeit-zeit'),
        ], width=12),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='fahrstrecke-zeit'),
        ], width=12),
    ]),
], fluid=True)

# Callback zur Aktualisierung der Diagramme basierend auf der Fahrtauswahl
@app.callback(
    Output('btCali', 'children'),
    Output('btCali', 'color'),
    Output('cali_value', 'children'),
    [Input('btCali', 'n_clicks')]
)
def update_output(n_clicks):
    if n_clicks >= 1:
        if n_clicks % 3 == 1:
            car.frontwheels.turn(90)
            return f'Fahrzeug auf Hintergrund stellen.', 'warning' , ''
        elif n_clicks % 3 == 2:
            car.background = car.infrared.get_average(100)
            print('measured background:', car.background)
            return f'Fahrzeug auf Linie stellen.', 'warning' , f'Hintergrund: {car.background}'
        elif n_clicks % 3 == 0:
            line = car.infrared.get_average(100)
            print('measured line:', line)
            car.infrared._references = (np.array(line) + np.array(car.background)) / 2
            print('Reference:', car.infrared._references)
            car.save_reference(car.infrared._references)
            return f'Neukalibrierung starten', 'primary' , f'Hintergrund: {car.background} Vordergrund: {line} Schwellwert: {car.infrared._references}'
    return f'Kalibrierung starten', 'primary' , ''

@app.callback(
    [
        Output('geschwindigkeit-zeit', 'figure'),
        Output('fahrstrecke-zeit', 'figure'),
        Output('Vmin', 'children'),
        Output('Vmax', 'children'),
        Output('Vmean', 'children'),
        Output('Fahrzeit', 'children'),
        Output('Fahrstrecke', 'children'),
        Output('Fahrmodus', 'children')
    ],
    [
        Input('fahrt-dropdown', 'value')
    ]
)
def update_diagrams(selected_fahrt):
    filtered_df = df[df['FahrtID'] == selected_fahrt]

    vmax_value = f"{result_df[result_df['FahrtID'] == selected_fahrt]['Vmax'].iloc[0]:.1f} km/h"
    vmin_value = f"{result_df[result_df['FahrtID'] == selected_fahrt]['Vmin'].iloc[0]:.1f} km/h"
    vmean_value = f"{result_df[result_df['FahrtID'] == selected_fahrt]['Vmean'].iloc[0]:.1f} km/h"
    fahrzeit_value = f"{result_df[result_df['FahrtID'] == selected_fahrt]['Fahrzeit'].iloc[0]:.1f} s"
    fahrstrecke_value = f"{result_df[result_df['FahrtID'] == selected_fahrt]['Fahrstrecke'].iloc[0]:.1f} mm"
    fahrmodus_value = f"{result_df[result_df['Fahrmodus'] == selected_fahrt]['Fahrmodus'].iloc[0]}"
    
    geschwindigkeit_fig = go.Figure(
        data=[
            go.Scatter(
                x=filtered_df['Zeit'],
                y=filtered_df['Geschwindigkeit'],
                mode='lines',
                line_shape='hv',  # Horizontale Stufenanzeige
                name="Geschwindigkeit"
            )
        ],
        layout=go.Layout(
            title=f"Geschwindigkeit über Zeit (Fahrt {selected_fahrt})",
            xaxis_title="Zeit (s)",
            yaxis_title="Geschwindigkeit (km/h)",
            height=400,
            shapes=[  # Hinzufügen der roten Linie
                dict(
                    type="line",
                    x0=filtered_df['Zeit'].min(),
                    x1=filtered_df['Zeit'].max(),
                    y0=0,
                    y1=0,
                    line=dict(color="black", width=2),
                )
            ]
        )
    )

    fahrstrecke_fig = go.Figure(
        data=[
            go.Scatter(
                x=filtered_df['Zeit'],
                y=filtered_df['Fahrstrecke'],
                mode='lines',
                name="Fahrstrecke"
            )
        ],
        layout=go.Layout(
            title=f"Fahrstrecke über Zeit (Fahrt {selected_fahrt})",
            xaxis_title="Zeit (s)",
            yaxis_title="Fahrstrecke (km)",
            height=400,
            shapes=[  # Hinzufügen der roten Linie
                dict(
                    type="line",
                    x0=filtered_df['Zeit'].min(),
                    x1=filtered_df['Zeit'].max(),
                    y0=0,
                    y1=0,
                    line=dict(color="black", width=2),
                )
            ]
        )
    )

    return geschwindigkeit_fig, fahrstrecke_fig, vmin_value, vmax_value, vmean_value, fahrzeit_value, fahrstrecke_value, fahrmodus_value

if __name__ == "__main__":
    app.run_server(debug=True, host=ip_host, port=8053)
    
    # print(df)
