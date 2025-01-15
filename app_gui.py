import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json
from dash.dependencies import Output, Input
from app_data import Data
from sensorcar import *
import numpy as np

car = SensorCar()
data = Data()
# print(data.df)
# print(data.result_df)

# Konfigurationslogik
try:
    with open("config.json", "r") as f:
        configdata = json.load(f)
        ip_host = configdata.get("ip_host", "0.0.0.0")  # Fallback zu "0.0.0.0"
except FileNotFoundError:
    print("Fehler: config.json nicht gefunden. Standardwerte werden verwendet.")
    ip_host = "0.0.0.0"

# Dash-App erstellen
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

#Setzt Variable am Anfang auf 1
f_id = 1

output_button_disable = [    
    Output('btFM1', 'disabled', allow_duplicate=True),        
    Output('btFM2', 'disabled', allow_duplicate=True),
    Output('btFM3', 'disabled', allow_duplicate=True),
    Output('btFM4', 'disabled', allow_duplicate=True),
    Output('btFM5', 'disabled', allow_duplicate=True),
    Output('btFM6', 'disabled', allow_duplicate=True),
    Output('btFM7', 'disabled', allow_duplicate=True),
  
    ]

# App-Layout
app.layout = dbc.Container([
    # Titel
    dbc.Row(
        dbc.Col(html.H1("Fahrmodus-Dashboard", className="text-center"), width=12),
        justify="center",  # Zentrieren der Zeile
        align="center",    # Vertikal zentrieren
        className="mb-4"
    ),
    
    # Hauptcard mit ButtonGroup und Buttons
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    children=[
                        dbc.ButtonGroup(
                            [
                                dbc.Button("Fahrmodus 1", id='btFM1'), 
                                dbc.Popover("Vorwärts- und Rückwärtsfahrt", target="btFM1", body=True, trigger="hover", placement="top"),
                                dbc.Button("Fahrmodus 2", id='btFM2'), 
                                dbc.Popover("Kreisfahrt mit max. Lenkwinkel", target="btFM2", body=True, trigger="hover", placement="top"),
                                dbc.Button("Fahrmodus 3", id='btFM3'), 
                                dbc.Popover("Vorwärts fahren bis Hindernis", target="btFM3", body=True, trigger="hover", placement="top"),
                                dbc.Button("Fahrmodus 4", id='btFM4'), 
                                dbc.Popover("Erkundungstour", target="btFM4", body=True, trigger="hover", placement="top"),
                                dbc.Button("Fahrmodus 5", id='btFM5'), 
                                dbc.Popover("Linienverfolgung", target="btFM5", body=True, trigger="hover", placement="top"),
                                dbc.Button("Fahrmodus 6", id='btFM6'), 
                                dbc.Popover("Erweiterte Linienverfolgung", target="btFM6", body=True, trigger="hover", placement="top"),
                                dbc.Button("Fahrmodus 7", id='btFM7'), 
                                dbc.Popover("Erweiterte Linienverfolgung mit Hinderniserkennung", target="btFM7", body=True, trigger="hover", placement="top"),
                            ],
                            size="lg",
                            className="me-1",
                        ),
                        dbc.Button("STOPP", id='btStopp', color='danger', style={'margin':'15px'}, size="lg"),
                        dbc.Popover("Stoppen der aktuellen Fahrt", target="btStopp", body=True, trigger="hover", placement="top"),
                        dbc.Button('Kalibrierung!', id='btCali', n_clicks=0, style={'margin':'15px'}, size="lg"),
                        dbc.Popover("Kalibrierung der IR-Sensoren", target="btCali", body=True, trigger="hover", placement="top"),
                        html.Div(id='cali_value')
                    ]
                ),
                style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
            ),
            width=10,
        ),
        justify="center",  # Zentrieren der Row
        align="center",    # Vertikal zentrieren
        className="mb-4"
    ),
    
    # Dropdown
    dbc.Row(
        dbc.Col([
            html.H4("Fahrtauswahl:"),
            dcc.Dropdown(
                id='fahrt-dropdown',
                options=[{'label': f"Fahrt {fahrt_id}, Fahrmodus: {data.result_df[data.result_df['FahrtID'] == fahrt_id]['Fahrmodus'].iloc[0]}", 'value': fahrt_id} for fahrt_id in data.df['FahrtID'].unique()],
                value=data.df['FahrtID'].unique()[0],  # Standardauswahl
                clearable=False,
                className="mb-2",
            ),
        ], width=10),  # Breite auf 10 gesetzt
        justify="center",  # Horizontale Zentrierung
        align="center",    # Vertikale Zentrierung
        className="mb-3"
    ),
    
    # Geschwindigkeits- und Streckenkarten mit einer Row-Breite von 10
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        children=[html.P("Geschwindigkeit min:"), html.P(f"{data.result_df['Vmin'].iloc[0]:.1f} km/h", id="Vmin")],
                    ),
                    style={ 'margin': '0px'}
                ),
                width=2  # Jede Karte nimmt 2 von 12 Spalten ein
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        children=[html.P("Geschwindigkeit max:"), html.P(f"{data.result_df['Vmax'].iloc[0]:.1f} km/h", id="Vmax")],
                    ),
                    style={'margin': '0px'}
                ),
                width=2
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        children=[html.P("Geschwindigkeit mean:"), html.P(f"{data.result_df['Vmean'].iloc[0]:.1f} km/h", id="Vmean")],
                    ),
                    style={'margin': '0px'}
                ),
                width=2
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        children=[html.P("Fahrstrecke:"), html.P(f"{data.result_df['Fahrstrecke'].iloc[0]:.1f} mm", id="Fahrstrecke")],
                    ),
                    style={'margin': '0px'}
                ),
                width=2
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        children=[html.P("Fahrzeit:"), html.P(f"{data.result_df['Fahrzeit'].iloc[0]:.1f} s", id="Fahrzeit")],
                    ),
                    style={'margin': '0px'}
                ),
                width=2
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        children=[html.P("Fahrmodus:"), html.P(f"{data.result_df['Fahrmodus'].iloc[0]:.1f} s", id="Fahrmodus")],
                    ),
                    style={'margin': '0px'}
                ),
                width=2
            ),
        ],
        justify="center",  # Zentriert die Karten horizontal
        align="center",    # Zentriert die Karten vertikal
        className="mb-4",  # Optional: Abstand nach unten
        style={'width': '84.4%', 'margin-left': 'auto', 'margin-right': 'auto'}  # Setzt die Breite der Row auf 10/12 der Gesamtbreite
    ),


    
    # Graphen
    dbc.Row(
        dbc.Col(dcc.Graph(id='geschwindigkeit-zeit'), width=10),  # Breite auf 10 gesetzt
        justify="center",  # Horizontale Zentrierung
        align="center",    # Vertikale Zentrierung
        className="mb-4"
    ),
    dbc.Row(
        dbc.Col(dcc.Graph(id='fahrstrecke-zeit'), width=10),  # Breite auf 10 gesetzt
        justify="center",  # Horizontale Zentrierung
        align="center",    # Vertikale Zentrierung
        className="mb-4"
    ),
], fluid=True)



# Callback zur Aktualisierung der Diagramme basierend auf der Fahrtauswahl
# Button Fahrmodus 1
@app.callback(
    output_button_disable,
    Output('btFM1', 'color', allow_duplicate=True),
    Input('btFM1', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    return True, True, True, True, True, True, True, 'warning'

# Button Fahrmodus 1 Farbänderung
@app.callback(
    output_button_disable,        
    Output('fahrt-dropdown', 'options', allow_duplicate=True), 
    Output('fahrt-dropdown', 'value', allow_duplicate=True),     
    Output('btFM1', 'color', allow_duplicate=True),
    Input('btFM1', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'warning':
        car.fahrmodus(1)
        data.read_data()  
    return False, False, False, False, False, False, False, [{'label': f"Fahrt {fahrt_id}, Fahrmodus: {data.result_df[data.result_df['FahrtID'] == fahrt_id]['Fahrmodus'].iloc[0]}", 'value': fahrt_id} for fahrt_id in data.df['FahrtID'].unique()], data.df['FahrtID'].unique()[-1], 'primary'

# Button Fahrmodus 2
@app.callback(
    output_button_disable, 
    Output('btFM2', 'color'),
    Input('btFM2', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    return True, True, True, True, True, True, True, 'warning'

# Button Fahrmodus 2 Farbänderung
@app.callback(
    output_button_disable, 
    Output('fahrt-dropdown', 'options', allow_duplicate=True), 
    Output('fahrt-dropdown', 'value', allow_duplicate=True),            
    Output('btFM2', 'color', allow_duplicate=True),
    Input('btFM2', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'warning':
        car.fahrmodus(2)
        data.read_data()  
    return False, False, False, False, False, False, False, [{'label': f"Fahrt {fahrt_id}, Fahrmodus: {data.result_df[data.result_df['FahrtID'] == fahrt_id]['Fahrmodus'].iloc[0]}", 'value': fahrt_id} for fahrt_id in data.df['FahrtID'].unique()], data.df['FahrtID'].unique()[-1], 'primary'

# Button Fahrmodus 3
@app.callback(
    output_button_disable, 
    Output('btFM3', 'color'),
    Input('btFM3', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    return True, True, True, True, True, True, True, 'warning'

# Button Fahrmodus 3 Farbänderung
@app.callback(
    output_button_disable,        
    Output('fahrt-dropdown', 'options', allow_duplicate=True), 
    Output('fahrt-dropdown', 'value', allow_duplicate=True),     
    Output('btFM3', 'color', allow_duplicate=True),
    Input('btFM3', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'warning':
        car.fahrmodus(3)
        data.read_data()  
    return False, False, False, False, False, False, False, [{'label': f"Fahrt {fahrt_id}, Fahrmodus: {data.result_df[data.result_df['FahrtID'] == fahrt_id]['Fahrmodus'].iloc[0]}", 'value': fahrt_id} for fahrt_id in data.df['FahrtID'].unique()], data.df['FahrtID'].unique()[-1], 'primary'

# Button Fahrmodus 4
@app.callback(
    output_button_disable, 
    Output('btFM4', 'color'),
    Input('btFM4', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    return True, True, True, True, True, True, True, 'warning'

# Button Fahrmodus 4 Farbänderung
@app.callback(
    output_button_disable, 
    Output('fahrt-dropdown', 'options', allow_duplicate=True), 
    Output('fahrt-dropdown', 'value', allow_duplicate=True),            
    Output('btFM4', 'color', allow_duplicate=True),
    Input('btFM4', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'warning':
        car.fahrmodus(4)
        data.read_data()  
    return False, False, False, False, False, False, False, [{'label': f"Fahrt {fahrt_id}, Fahrmodus: {data.result_df[data.result_df['FahrtID'] == fahrt_id]['Fahrmodus'].iloc[0]}", 'value': fahrt_id} for fahrt_id in data.df['FahrtID'].unique()], data.df['FahrtID'].unique()[-1], 'primary'


# Button Fahrmodus 5
@app.callback(
    output_button_disable, 
    Output('btFM5', 'color'),
    Input('btFM5', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    return True, True, True, True, True, True, True, 'warning'

# Button Fahrmodus 5 Farbänderung
@app.callback(
    output_button_disable,  
    Output('fahrt-dropdown', 'options', allow_duplicate=True), 
    Output('fahrt-dropdown', 'value', allow_duplicate=True),           
    Output('btFM5', 'color', allow_duplicate=True),
    Input('btFM5', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'warning':
        car.fahrmodus(5)
        data.read_data()  
    return False, False, False, False, False, False, False, [{'label': f"Fahrt {fahrt_id}, Fahrmodus: {data.result_df[data.result_df['FahrtID'] == fahrt_id]['Fahrmodus'].iloc[0]}", 'value': fahrt_id} for fahrt_id in data.df['FahrtID'].unique()], data.df['FahrtID'].unique()[-1], 'primary'

# Button Fahrmodus 6
@app.callback(
    output_button_disable, 
    Output('btFM6', 'color'),
    Input('btFM6', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    return True, True, True, True, True, True, True, 'warning'

# Button Fahrmodus 6 Farbänderung
@app.callback(
    output_button_disable,   
    Output('fahrt-dropdown', 'options', allow_duplicate=True), 
    Output('fahrt-dropdown', 'value', allow_duplicate=True),          
    Output('btFM6', 'color', allow_duplicate=True),
    Input('btFM6', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'warning':
        car.fahrmodus(6)
        data.read_data()  
    return False, False, False, False, False, False, False, [{'label': f"Fahrt {fahrt_id}, Fahrmodus: {data.result_df[data.result_df['FahrtID'] == fahrt_id]['Fahrmodus'].iloc[0]}", 'value': fahrt_id} for fahrt_id in data.df['FahrtID'].unique()], data.df['FahrtID'].unique()[-1], 'primary'

# Button Fahrmodus 7
@app.callback(
    output_button_disable, 
    Output('btFM7', 'color'),
    Input('btFM7', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    return True, True, True, True, True, True, True, 'warning'

# Button Fahrmodus 7 Farbänderung
@app.callback(
    output_button_disable,   
    Output('fahrt-dropdown', 'options', allow_duplicate=True), 
    Output('fahrt-dropdown', 'value', allow_duplicate=True),          
    Output('btFM7', 'color', allow_duplicate=True),
    Input('btFM7', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'warning':
        car.fahrmodus(7)
        data.read_data()  
    return False, False, False, False, False, False, False, [{'label': f"Fahrt {fahrt_id}, Fahrmodus: {data.result_df[data.result_df['FahrtID'] == fahrt_id]['Fahrmodus'].iloc[0]}", 'value': fahrt_id} for fahrt_id in data.df['FahrtID'].unique()], data.df['FahrtID'].unique()[-1], 'primary'

# Stopp-Button
@app.callback(
    Output('btFM1', 'disabled', allow_duplicate=True),
    Output('btFM1', 'color', allow_duplicate=True),         
    Output('btFM2', 'disabled', allow_duplicate=True),
    Output('btFM2', 'color', allow_duplicate=True),
    Output('btFM3', 'disabled', allow_duplicate=True),
    Output('btFM3', 'color', allow_duplicate=True),
    Output('btFM4', 'disabled', allow_duplicate=True),
    Output('btFM4', 'color', allow_duplicate=True),
    Output('btFM5', 'disabled', allow_duplicate=True),
    Output('btFM5', 'color', allow_duplicate=True),
    Output('btFM6', 'disabled', allow_duplicate=True),
    Output('btFM6', 'color', allow_duplicate=True),
    Output('btFM7', 'disabled', allow_duplicate=True),
    Output('btFM7', 'color', allow_duplicate=True),
    Input('btStopp', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    car.ismanually_stopped = True
    return False, 'primary', False, 'primary',False, 'primary',False, 'primary',False, 'primary',False, 'primary', False, 'primary'

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
    filtered_df = data.df[data.df['FahrtID'] == selected_fahrt]

    vmax_value = f"{data.result_df[data.result_df['FahrtID'] == selected_fahrt]['Vmax'].iloc[0]:.1f} km/h"
    vmin_value = f"{data.result_df[data.result_df['FahrtID'] == selected_fahrt]['Vmin'].iloc[0]:.1f} km/h"
    vmean_value = f"{data.result_df[data.result_df['FahrtID'] == selected_fahrt]['Vmean'].iloc[0]:.1f} km/h"
    fahrzeit_value = f"{data.result_df[data.result_df['FahrtID'] == selected_fahrt]['Fahrzeit'].iloc[0]:.1f} s"
    fahrstrecke_value = f"{data.result_df[data.result_df['FahrtID'] == selected_fahrt]['Fahrstrecke'].iloc[0]:.1f} mm"
    fahrmodus_value = f"{data.result_df[data.result_df['FahrtID'] == selected_fahrt]['Fahrmodus'].iloc[0]}"
    
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
            title={"text": f"Fahrstrecke über Zeit (Fahrt {selected_fahrt})","font": {"color": "white"}},
            xaxis={"title": {"text": "Zeit (s)","font": {"color": "white"}}, "tickfont": {"color": "white"}, "gridcolor": "grey", "linecolor": "grey"},
            yaxis={"title": {"text": "Geschwindigkeit (km/h)","font": {"color": "white"}}, "tickfont": {"color": "white"}, "gridcolor": "grey", "linecolor": "grey"},
            height=400,
            paper_bgcolor="rgba(40,40,40,1)",
            plot_bgcolor="rgba(40,40,40,1)",            
            shapes=[  # Hinzufügen der roten Linie
                dict(
                    type="line",
                    x0=filtered_df['Zeit'].min(),
                    x1=filtered_df['Zeit'].max(),
                    y0=0,
                    y1=0,
                    line=dict(color="red", width=2),
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
            title={"text": f"Fahrstrecke über Zeit (Fahrt {selected_fahrt})","font": {"color": "white"}},
            xaxis={"title": {"text": "Zeit (s)","font": {"color": "white"}}, "tickfont": {"color": "white"}, "gridcolor": "grey", "linecolor": "grey"},
            yaxis={"title": {"text": "Fahrstrecke (km)","font": {"color": "white"}}, "tickfont": {"color": "white"}, "gridcolor": "grey", "linecolor": "grey"},            
            height=400,
            paper_bgcolor="rgba(40,40,40,1)",
            plot_bgcolor="rgba(40,40,40,1)",
            # shapes=[  # Hinzufügen der roten Linie
            #     dict(
            #         type="line",
            #         x0=filtered_df['Zeit'].min(),
            #         x1=filtered_df['Zeit'].max(),
            #         y0=0,
            #         y1=0,
            #         line=dict(color="red", width=2),
            #     )
            # ]
        )
    )

    return geschwindigkeit_fig, fahrstrecke_fig, vmin_value, vmax_value, vmean_value, fahrzeit_value, fahrstrecke_value, fahrmodus_value

if __name__ == "__main__":
    app.run_server(debug=True, host=ip_host, port=8053)
    
    # print(df)
