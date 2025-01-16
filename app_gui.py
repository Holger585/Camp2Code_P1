from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json
from dash.dependencies import Output, Input, State
from app_data import Data
from sensorcar import SensorCar
import numpy as np

car = SensorCar()
data = Data()

class SaveConfig():
    def __init__(self):
        self.configdata = []

    def save_config(self, Vmax: int, LWmax: int, DISTmin: int):
        try:
            with open("config.json", "r") as f:
                self.configdata = json.load(f)
            with open("config.json", "w") as f:
                self.configdata["Vmax"] = Vmax
                self.configdata["LWmax"] = LWmax
                self.configdata["DISTmin"] = DISTmin
                json.dump(self.configdata, f, indent=4)

        except FileNotFoundError as e:
            print(f"Fehler: config.json nicht gefunden. Standardwerte werden verwendet. {e}")
            car.vmax_vorgabe = 50
            car.maxwinkel_vorgabe = 30
            car.mindist_vorgabe = 10
        except Exception as e:
            print(e)
            car.vmax_vorgabe = 50
            car.maxwinkel_vorgabe = 30
            car.mindist_vorgabe = 10

saveconfig = SaveConfig()

# Konfigurationslogik
try:
    with open("config.json", "r") as f:
        configdata = json.load(f)
        ip_host = configdata.get("ip_host", "0.0.0.0")  # Fallback zu "0.0.0.0"
        car.vmax_vorgabe = configdata.get("Vmax", 50)  # Fallback zu 50
        car.maxwinkel_vorgabe = configdata.get("LWmax", 45)  # Fallback zu 45
        car.mindist_vorgabe = configdata.get("DISTmin", 10)  # Fallback zu 10
except FileNotFoundError:
    print("Fehler: config.json nicht gefunden. Standardwerte werden verwendet.")
    ip_host = "0.0.0.0"


# Dash-App erstellen
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Setzt Variable am Anfang auf 1
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
        className="mb-0"
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
                                dbc.Button("M",id="collapse-button", n_clicks=0),
                                dbc.Popover("Manueller Fahrmodus", target="collapse-button", body=True, trigger="hover", placement="top"),
                            ],
                            size="lg",
                            className="me-1",
                        ),
                        dbc.Button("STOPP", id='btStopp', color='danger', style={'margin':'15px'}, size="lg"),
                        dbc.Popover("Stoppen der aktuellen Fahrt", target="btStopp", body=True, trigger="hover", placement="top"),
                        dbc.Button('Kalibrierung!', id='btCali', n_clicks=0, style={'margin':'15px'}, size="lg"),
                        dbc.Popover("Kalibrierung der IR-Sensoren", target="btCali", body=True, trigger="hover", placement="top"),
                        #dbc.Button("M",id="collapse-button", style={'margin':'15px'}, size="lg", n_clicks=0,),                        
                        html.Div(id='cali_value', style={'textAlign':'right'}),
                        # Hier die Dropdowns hinzufügen
                        html.Div(
                            children=[
                                html.Label("Max. Geschwindigkeit", style={'margin-left': '10px'}),  # Label links vom Dropdown
                                dcc.Dropdown(
                                    id='vmax_vorgabe',
                                    options=[
                                        {'label': '15cm/s', 'value': 30},
                                        {'label': '20cm/s', 'value': 40},
                                        {'label': '25cm/s', 'value': 50},
                                        {'label': '30cm/s', 'value': 60},
                                        {'label': '35cm/s', 'value': 70},
                                        {'label': '40cm/s', 'value': 80},
                                        {'label': '45cm/s', 'value': 90},
                                        {'label': '50cm/s', 'value': 100},
                                    ],
                                    value=car.vmax_vorgabe,  # Standardwert
                                    style={'width': '150px'}
                                ),
                                html.Label("Lenkwinkel", style={'margin-left': '10px'}),  # Label links vom Dropdown
                                dcc.Dropdown(
                                    id='maxwinkel_vorgabe',
                                    options=[
                                        {'label': '15°', 'value': 15},
                                        {'label': '30°', 'value': 30},
                                        {'label': '45°', 'value': 45},
                                    ],
                                    value=car.maxwinkel_vorgabe,  # Standardwert
                                    style={'width': '150px'}
                                ),
                                html.Label("Min. Distanz", style={'margin-left': '10px'}),  # Label links vom Dropdown
                                dcc.Dropdown(
                                    id='mindist_vorgabe',
                                    options=[
                                        {'label': 'Aus', 'value': 0},
                                        {'label': '5cm', 'value': 5},
                                        {'label': '10cm', 'value': 10},
                                        {'label': '15cm', 'value': 15},
                                    ],
                                    value=car.mindist_vorgabe,  # Standardwert
                                    style={'width': '150px'}
                                ),
                            ],
                            style={
                                'display': 'flex',  # Flexbox verwenden, um Dropdowns nebeneinander zu setzen
                                'justify-content': 'center',  # Zentrieren
                                'gap': '20px',  # Abstand zwischen den Dropdowns
                                'margin-top': '20px'  # Abstand nach oben
                            }
                        ),
                        dbc.Collapse(
                            dbc.Card(
                                dbc.CardBody(
                                    children=[
                                        dbc.Button("Vor", id='btVor', color='primary', style={'width': '100px', 'margin':'15px'}, size="lg"),
                                        dbc.Popover("Vorwärtsfahren", target="btVor", body=True, trigger="hover", placement="top"),
                                        html.Div(
                                            [
                                                dbc.Button("Links", id='btLinks', color='primary', style={'width': '100px', 'margin':'15px'}, size="lg"),
                                                dbc.Popover("Nach Links lenken", target="btLinks", body=True, trigger="hover", placement="left"),
                                                dbc.Button("Stopp", id='btStop', color='danger', style={'width': '100px', 'margin':'15px'}, size="lg"),                                   
                                                dbc.Button("Rechts", id='btRechts', color='primary', style={'width': '100px', 'margin':'15px'}, size="lg"),
                                                dbc.Popover("Nach Rechts lenken", target="btRechts", body=True, trigger="hover", placement="right"),
                                            ],
                                            style={
                                                'display': 'flex',  # Flexbox verwenden, um Buttons nebeneinander zu setzen
                                                'justify-content': 'center',  # Zentrieren
                                                'gap': '10px'  # Abstand zwischen den Buttons
                                            }
                                        ),
                                        dbc.Button("Zurück", id='btZurueck', color='primary', style={'width': '100px', 'margin':'15px'}, size="lg"),
                                        dbc.Popover("Rückwärtsfahren", target="btZurueck", body=True, trigger="hover", placement="bottom"),                                                                                                            
                                    ],
                                    style={
                                        'display': 'flex',  # Flexbox verwenden, um Buttons nebeneinander zu setzen
                                        'flex-direction': 'column',  # Vertikale Anordnung
                                        'align-items': 'center',  # Zentrieren
                                        'gap': '10px'  # Abstand zwischen den Buttons
                                    }
                                )
                            ),
                            id="collapse",
                            is_open=False,
                        ),                        
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
                        children=[html.P("Geschwindigkeit min:"), html.P(f"{data.result_df['Vmin'].iloc[0]:.1f} cm/s", id="Vmin")],
                    ),
                    style={ 'margin': '0px'}
                ),
                width=2  # Jede Karte nimmt 2 von 12 Spalten ein
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        children=[html.P("Geschwindigkeit max:"), html.P(f"{data.result_df['Vmax'].iloc[0]:.1f} cm/s", id="Vmax")],
                    ),
                    style={'margin': '0px'}
                ),
                width=2
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        children=[html.P("Geschwindigkeit mean:"), html.P(f"{data.result_df['Vmean'].iloc[0]:.1f} cm/s", id="Vmean")],
                    ),
                    style={'margin': '0px'}
                ),
                width=2
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        children=[html.P("Fahrstrecke:"), html.P(f"{data.result_df['Fahrstrecke'].iloc[0]:.1f} m", id="Fahrstrecke")],
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
        dbc.Col(dcc.Graph(id='sonic-zeit'), width=10),  # Breite auf 10 gesetzt
        justify="center",  # Horizontale Zentrierung
        align="center",    # Vertikale Zentrierung
        className="mb-4"
    ),    
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
    dbc.Row(
        dbc.Col(dcc.Graph(id='lenkwinkel-zeit'), width=10),  # Breite auf 10 gesetzt
        justify="center",  # Horizontale Zentrierung
        align="center",    # Vertikale Zentrierung
        className="mb-4"
    ),
    dbc.Row(
        dbc.Col(dcc.Graph(id='ir-status-zeit'), width=10),  # Breite auf 10 gesetzt
        justify="center",  # Horizontale Zentrierung
        align="center",    # Vertikale Zentrierung
        className="mb-4"
    ),
], fluid=True)



# Callback zur Aktualisierung der Diagramme basierend auf der Fahrtauswahl

# Button Fahrmodus 1
@app.callback(
    output_button_disable,
    Output('btFM1', 'children', allow_duplicate=True),
    Output('btFM1', 'color', allow_duplicate=True),
    Input('btFM1', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    return True, True, True, True, True, True, True, [dbc.Spinner(size="sm"), " FM1 aktiv..."], 'warning'

# Button Fahrmodus 1 Farbänderung
@app.callback(
    output_button_disable,        
    Output('btFM1', 'children', allow_duplicate=True),    
    Output('fahrt-dropdown', 'options', allow_duplicate=True), 
    Output('fahrt-dropdown', 'value', allow_duplicate=True),     
    Output('btFM1', 'color', allow_duplicate=True),
    Input('btFM1', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'warning':
        car.fahrmodus(fmodus=1, speed=car.vmax_vorgabe, mindist=car.mindist_vorgabe)
        data.read_data()  
    return False, False, False, False, False, False, False, 'Fahrmodus 1', [{'label': f"Fahrt {fahrt_id}, Fahrmodus: {data.result_df[data.result_df['FahrtID'] == fahrt_id]['Fahrmodus'].iloc[0]}", 'value': fahrt_id} for fahrt_id in data.df['FahrtID'].unique()], data.df['FahrtID'].unique()[-1], 'primary'

# Button Fahrmodus 2
@app.callback(
    output_button_disable, 
    Output('btFM2', 'children', allow_duplicate=True),    
    Output('btFM2', 'color'),
    Input('btFM2', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    return True, True, True, True, True, True, True, [dbc.Spinner(size="sm"), " FM2 aktiv..."],'warning'

# Button Fahrmodus 2 Farbänderung
@app.callback(
    output_button_disable, 
    Output('btFM2', 'children', allow_duplicate=True),    
    Output('fahrt-dropdown', 'options', allow_duplicate=True), 
    Output('fahrt-dropdown', 'value', allow_duplicate=True),            
    Output('btFM2', 'color', allow_duplicate=True),
    Input('btFM2', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'warning':
        car.fahrmodus(fmodus=2, speed=car.vmax_vorgabe, mindist=car.mindist_vorgabe)
        data.read_data()  
    return False, False, False, False, False, False, False, 'Fahrmodus 2', [{'label': f"Fahrt {fahrt_id}, Fahrmodus: {data.result_df[data.result_df['FahrtID'] == fahrt_id]['Fahrmodus'].iloc[0]}", 'value': fahrt_id} for fahrt_id in data.df['FahrtID'].unique()], data.df['FahrtID'].unique()[-1], 'primary'

# Button Fahrmodus 3
@app.callback(
    output_button_disable,
    Output('btFM3', 'children', allow_duplicate=True),      
    Output('btFM3', 'color'),
    Input('btFM3', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    return True, True, True, True, True, True, True, [dbc.Spinner(size="sm"), " FM3 aktiv..."], 'warning'

# Button Fahrmodus 3 Farbänderung
@app.callback(
    output_button_disable, 
    Output('btFM3', 'children', allow_duplicate=True),            
    Output('fahrt-dropdown', 'options', allow_duplicate=True), 
    Output('fahrt-dropdown', 'value', allow_duplicate=True),     
    Output('btFM3', 'color', allow_duplicate=True),
    Input('btFM3', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'warning':
        car.fahrmodus(fmodus=3, speed=car.vmax_vorgabe,  mindist=car.mindist_vorgabe)
        data.read_data()  
    return False, False, False, False, False, False, False, 'Fahrmodus 3', [{'label': f"Fahrt {fahrt_id}, Fahrmodus: {data.result_df[data.result_df['FahrtID'] == fahrt_id]['Fahrmodus'].iloc[0]}", 'value': fahrt_id} for fahrt_id in data.df['FahrtID'].unique()], data.df['FahrtID'].unique()[-1], 'primary'

# Button Fahrmodus 4
@app.callback(
    output_button_disable, 
    Output('btFM4', 'children', allow_duplicate=True),     
    Output('btFM4', 'color'),
    Input('btFM4', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    return True, True, True, True, True, True, True, [dbc.Spinner(size="sm"), " FM4 aktiv..."],'warning'

# Button Fahrmodus 4 Farbänderung
@app.callback(
    output_button_disable, 
    Output('btFM4', 'children', allow_duplicate=True),     
    Output('fahrt-dropdown', 'options', allow_duplicate=True), 
    Output('fahrt-dropdown', 'value', allow_duplicate=True),            
    Output('btFM4', 'color', allow_duplicate=True),
    Input('btFM4', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'warning':
        car.fahrmodus(fmodus=4, speed=car.vmax_vorgabe, mindist=car.mindist_vorgabe)
        data.read_data()  
    return False, False, False, False, False, False, False, 'Fahrmodus 4', [{'label': f"Fahrt {fahrt_id}, Fahrmodus: {data.result_df[data.result_df['FahrtID'] == fahrt_id]['Fahrmodus'].iloc[0]}", 'value': fahrt_id} for fahrt_id in data.df['FahrtID'].unique()], data.df['FahrtID'].unique()[-1], 'primary'


# Button Fahrmodus 5
@app.callback(
    output_button_disable, 
    Output('btFM5', 'children', allow_duplicate=True),      
    Output('btFM5', 'color'),
    Input('btFM5', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    return True, True, True, True, True, True, True, [dbc.Spinner(size="sm"), " FM5 aktiv..."], 'warning'

# Button Fahrmodus 5 Farbänderung
@app.callback(
    output_button_disable,  
    Output('btFM5', 'children', allow_duplicate=True),      
    Output('fahrt-dropdown', 'options', allow_duplicate=True), 
    Output('fahrt-dropdown', 'value', allow_duplicate=True),           
    Output('btFM5', 'color', allow_duplicate=True),
    Input('btFM5', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'warning':
        car.fahrmodus(fmodus=5, speed=car.vmax_vorgabe, mindist=car.mindist_vorgabe)
        data.read_data()  
    return False, False, False, False, False, False, False, 'Fahrmodus 5', [{'label': f"Fahrt {fahrt_id}, Fahrmodus: {data.result_df[data.result_df['FahrtID'] == fahrt_id]['Fahrmodus'].iloc[0]}", 'value': fahrt_id} for fahrt_id in data.df['FahrtID'].unique()], data.df['FahrtID'].unique()[-1], 'primary'

# Button Fahrmodus 6
@app.callback(
    output_button_disable, 
    Output('btFM6', 'children', allow_duplicate=True),     
    Output('btFM6', 'color'),
    Input('btFM6', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    return True, True, True, True, True, True, True, [dbc.Spinner(size="sm"), " FM6 aktiv..."], 'warning'

# Button Fahrmodus 6 Farbänderung
@app.callback(
    output_button_disable, 
    Output('btFM6', 'children', allow_duplicate=True),       
    Output('fahrt-dropdown', 'options', allow_duplicate=True), 
    Output('fahrt-dropdown', 'value', allow_duplicate=True),          
    Output('btFM6', 'color', allow_duplicate=True),
    Input('btFM6', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'warning':
        car.fahrmodus(fmodus=6, speed=car.vmax_vorgabe, mindist=car.mindist_vorgabe)
        data.read_data()  
    return False, False, False, False, False, False, False, 'Fahrmodus 6', [{'label': f"Fahrt {fahrt_id}, Fahrmodus: {data.result_df[data.result_df['FahrtID'] == fahrt_id]['Fahrmodus'].iloc[0]}", 'value': fahrt_id} for fahrt_id in data.df['FahrtID'].unique()], data.df['FahrtID'].unique()[-1], 'primary'

# Button Fahrmodus 7
@app.callback(
    output_button_disable, 
    Output('btFM7', 'children', allow_duplicate=True),     
    Output('btFM7', 'color'),
    Input('btFM7', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    return True, True, True, True, True, True, True, [dbc.Spinner(size="sm"), " FM7 aktiv..."], 'warning'

# Button Fahrmodus 7 Farbänderung
@app.callback(
    output_button_disable,  
    Output('btFM7', 'children', allow_duplicate=True),      
    Output('fahrt-dropdown', 'options', allow_duplicate=True), 
    Output('fahrt-dropdown', 'value', allow_duplicate=True),          
    Output('btFM7', 'color', allow_duplicate=True),
    Input('btFM7', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'warning':
        car.fahrmodus(fmodus=7, speed=car.vmax_vorgabe, mindist=car.mindist_vorgabe)
        data.read_data()  
    return False, False, False, False, False, False, False, 'Fahrmodus 7', [{'label': f"Fahrt {fahrt_id}, Fahrmodus: {data.result_df[data.result_df['FahrtID'] == fahrt_id]['Fahrmodus'].iloc[0]}", 'value': fahrt_id} for fahrt_id in data.df['FahrtID'].unique()], data.df['FahrtID'].unique()[-1], 'primary'

# Stopp-Button
@app.callback(
    Output('btFM1', 'children', allow_duplicate=True),
    Output('btFM1', 'disabled', allow_duplicate=True),
    Output('btFM1', 'color', allow_duplicate=True),  
    Output('btFM2', 'children', allow_duplicate=True),       
    Output('btFM2', 'disabled', allow_duplicate=True),
    Output('btFM2', 'color', allow_duplicate=True),
    Output('btFM3', 'children', allow_duplicate=True),
    Output('btFM3', 'disabled', allow_duplicate=True),
    Output('btFM3', 'color', allow_duplicate=True),
    Output('btFM4', 'children', allow_duplicate=True),
    Output('btFM4', 'disabled', allow_duplicate=True),
    Output('btFM4', 'color', allow_duplicate=True),
    Output('btFM5', 'children', allow_duplicate=True),
    Output('btFM5', 'disabled', allow_duplicate=True),
    Output('btFM5', 'color', allow_duplicate=True),
    Output('btFM6', 'children', allow_duplicate=True),
    Output('btFM6', 'disabled', allow_duplicate=True),
    Output('btFM6', 'color', allow_duplicate=True),
    Output('btFM7', 'children', allow_duplicate=True),
    Output('btFM7', 'disabled', allow_duplicate=True),
    Output('btFM7', 'color', allow_duplicate=True),
    Input('btStopp', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    car.ismanually_stopped = True
    return 'Fahrmodus 1', False, 'primary', 'Fahrmodus 2', False, 'primary', 'Fahrmodus 3', False, 'primary', 'Fahrmodus 4', False, 'primary', 'Fahrmodus 5', False, 'primary', 'Fahrmodus 6', False, 'primary', 'Fahrmodus 7', False, 'primary'

@app.callback(
    Output('btCali', 'children'),
    Output('btCali', 'color'),
    Output('cali_value', 'children'),
    Output('vmax_vorgabe', 'value'),
    Output('maxwinkel_vorgabe', 'value'),
    Output('mindist_vorgabe', 'value'),
    [Input('btCali', 'n_clicks')]
)
def update_output(n_clicks):
    if n_clicks >= 1:
        if n_clicks % 3 == 1:
            car.frontwheels.turn(90)
            return f'Fzg. auf Hintergrd. stellen', 'warning' , '', car.vmax_vorgabe, car.maxwinkel_vorgabe, car.mindist_vorgabe
        elif n_clicks % 3 == 2:
            car.background = car.infrared.get_average(100)
            print('measured background:', car.background)
            return f'Fzg. auf Linie stellen', 'warning' , f'Hintergrund: {car.background}', car.vmax_vorgabe, car.maxwinkel_vorgabe, car.mindist_vorgabe
        elif n_clicks % 3 == 0:
            line = car.infrared.get_average(100)
            print('measured line:', line)
            car.infrared._references = (np.array(line) + np.array(car.background)) / 2
            print('Reference:', car.infrared._references)
            car.save_reference(car.infrared._references)
            return f'Neukalibrierung starten', 'primary' , f'Hintergrund: {car.background} Vordergrund: {line} Schwellwert: {car.infrared._references}', car.vmax_vorgabe, car.maxwinkel_vorgabe, car.mindist_vorgabe
    return f'Kalibrierung starten', 'primary' , '', car.vmax_vorgabe, car.maxwinkel_vorgabe, car.mindist_vorgabe

# Button zum Ausklappen des manuellen Fahrmodus
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Dropdown Max Geschwindigkeit
@app.callback(
    Output('btCali', 'disabled', allow_duplicate=True),
    Input('vmax_vorgabe', 'value'),
    prevent_initial_call=True
)
def update_output(value):
    car.vmax_vorgabe = value
    saveconfig.save_config(car.vmax_vorgabe, car.maxwinkel_vorgabe, car.mindist_vorgabe)
    return False

# Dropdown Max Lenkwinkel
@app.callback(
    Output('btCali', 'disabled', allow_duplicate=True),
    Input('maxwinkel_vorgabe', 'value'),
   prevent_initial_call=True
)
def update_output(value):
    car.maxwinkel_vorgabe = value
    saveconfig.save_config(car.vmax_vorgabe, car.maxwinkel_vorgabe, car.mindist_vorgabe)
    return False

# Dropdown Min Abstand
@app.callback(
    Output('btCali', 'disabled', allow_duplicate=True),
    Input('mindist_vorgabe', 'value'),
    prevent_initial_call=True
)
def update_output(value):
    car.mindist_vorgabe = value
    saveconfig.save_config(car.vmax_vorgabe, car.maxwinkel_vorgabe, car.mindist_vorgabe)
    return False

# Button Vorwärts
@app.callback(
    Output('btVor', 'color', allow_duplicate=True),
    Output('btZurueck', 'disabled', allow_duplicate=True),  
    Output('btRechts', 'color', allow_duplicate=True),
    Output('btLinks', 'color', allow_duplicate=True),       
    Input('btVor', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks): 
    car.frontwheels.turn(90)
    return 'success', True, 'primary', 'primary'

# Button Vorwärts Farbänderung
@app.callback( 
    Output('btCali', 'disabled', allow_duplicate=True),    
    Input('btVor', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'success':
        car.drive(car.vmax_vorgabe)
    return False

# Button Rückwärts
@app.callback(
    Output('btZurueck', 'color', allow_duplicate=True),
    Output('btVor', 'disabled', allow_duplicate=True), 
    Output('btRechts', 'color', allow_duplicate=True),
    Output('btLinks', 'color', allow_duplicate=True),        
    Input('btZurueck', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    car.frontwheels.turn(90)
    return 'success', True, 'primary', 'primary'

# Button Rückwärts Farbänderung
@app.callback( 
    Output('btCali', 'disabled', allow_duplicate=True),
    Input('btZurueck', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'success':
        car.drive(-car.vmax_vorgabe)
    return False  

# Button Links lenken
@app.callback(
    Output('btLinks', 'color', allow_duplicate=True),    
    Output('btRechts', 'color', allow_duplicate=True),
    Input('btLinks', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    car.frontwheels.turn(90-car.maxwinkel_vorgabe)
    return 'success', 'primary'

# Button Links lenken Farbänderung
@app.callback( 
    Output('btCali', 'disabled', allow_duplicate=True),
    Input('btLinks', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'success':
        car.frontwheels.turn(90-car.maxwinkel_vorgabe)
    return False  

# Button Rechts lenken
@app.callback(
    Output('btRechts', 'color', allow_duplicate=True),
    Output('btLinks', 'color', allow_duplicate=True), 
    Input('btRechts', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    car.frontwheels.turn(90+car.maxwinkel_vorgabe)
    return 'success', 'primary'

# Button Rechts lenken Farbänderung
@app.callback( 
    Output('btCali', 'disabled', allow_duplicate=True),
    Input('btRechts', 'color'), 
    prevent_initial_call=True
)
def update_output(color):
    if color == 'success':
        car.frontwheels.turn(90+car.maxwinkel_vorgabe)
    return False     

# Button Stopp
@app.callback(
    Output('btVor', 'color', allow_duplicate=True),
    Output('btLinks', 'color', allow_duplicate=True),
    Output('btRechts', 'color', allow_duplicate=True),
    Output('btZurueck', 'color', allow_duplicate=True),
    Output('btVor', 'disabled', allow_duplicate=True),
    Output('btLinks', 'disabled', allow_duplicate=True),
    Output('btRechts', 'disabled', allow_duplicate=True),
    Output('btZurueck', 'disabled', allow_duplicate=True),
    Input('btStop', 'n_clicks'), 
    prevent_initial_call=True
)
def update_output(n_clicks):
    car.stop()
    car.frontwheels.turn(90)
    return 'primary', 'primary', 'primary', 'primary', False, False, False, False

@app.callback(
    [
        Output('geschwindigkeit-zeit', 'figure'),
        Output('fahrstrecke-zeit', 'figure'),
        Output('sonic-zeit', 'figure'),
        Output('sonic-zeit', 'style'),
        Output('lenkwinkel-zeit', 'figure'),
        Output('ir-status-zeit', 'figure'),
        Output('ir-status-zeit', 'style'),
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
    filtered_df['Abstand2'] = filtered_df['Abstand'].apply(lambda x: 500 if x == -2 else (x if x >= 0 else None))

    vmax_value = f"{data.result_df[data.result_df['FahrtID'] == selected_fahrt]['Vmax'].iloc[0]:.1f} cm/s"
    vmin_value = f"{data.result_df[data.result_df['FahrtID'] == selected_fahrt]['Vmin'].iloc[0]:.1f} cm/s"
    vmean_value = f"{data.result_df[data.result_df['FahrtID'] == selected_fahrt]['Vmean'].iloc[0]:.1f} cm/s"
    fahrzeit_value = f"{data.result_df[data.result_df['FahrtID'] == selected_fahrt]['Fahrzeit'].iloc[0]:.1f} s"
    fahrstrecke_value = f"{data.result_df[data.result_df['FahrtID'] == selected_fahrt]['Fahrstrecke'].iloc[0]:.1f} m"
    fahrmodus_value = f"{data.result_df[data.result_df['FahrtID'] == selected_fahrt]['Fahrmodus'].iloc[0]}"

    sonic_fig = go.Figure(
        data=[
            go.Scatter(
                x=filtered_df['Zeit'],
                y=filtered_df['Abstand2'],
                mode='lines',
                name="Abstand"
            )
        ],
        layout=go.Layout(
            title={"text": f"Abstand über Zeit (Fahrt {selected_fahrt})","font": {"color": "white"}},
            xaxis={"title": {"text": "Zeit (s)","font": {"color": "white"}}, "tickfont": {"color": "white"}, "gridcolor": "grey", "linecolor": "grey"},
            yaxis={"title": {"text": "Abstand (cm)","font": {"color": "white"}}, "tickfont": {"color": "white"}, "gridcolor": "grey", "linecolor": "grey"},            
            height=400,
            paper_bgcolor="rgba(40,40,40,1)",
            plot_bgcolor="rgba(40,40,40,1)",
            shapes=[  # Hinzufügen der roten Linie
                dict(
                    type="line",
                    x0=filtered_df['Zeit'].min(),
                    x1=filtered_df['Zeit'].max(),
                    y0=car.mindist_vorgabe,
                    y1=car.mindist_vorgabe,
                    line=dict(color="red", width=1),
                )
            ]
        )
    )

    geschwindigkeit_fig = go.Figure(
        data=[
            go.Scatter(
                x=filtered_df['Zeit'],
                y=filtered_df['Geschwindigkeit']/1.85,
                mode='lines',
                line_shape='hv',  # Horizontale Stufenanzeige
                name="Geschwindigkeit"
            )
        ],
        layout=go.Layout(
            title={"text": f"Fahrstrecke über Zeit (Fahrt {selected_fahrt})","font": {"color": "white"}},
            xaxis={"title": {"text": "Zeit (s)","font": {"color": "white"}}, "tickfont": {"color": "white"}, "gridcolor": "grey", "linecolor": "grey"},
            yaxis={"title": {"text": "Geschwindigkeit (cm/s)","font": {"color": "white"}}, "tickfont": {"color": "white"}, "gridcolor": "grey", "linecolor": "grey"},
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
            yaxis={"title": {"text": "Fahrstrecke (m)","font": {"color": "white"}}, "tickfont": {"color": "white"}, "gridcolor": "grey", "linecolor": "grey"},            
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

    lenkwinkel_fig = go.Figure(
        data=[
            go.Scatter(
                x=filtered_df['Zeit'],
                y=filtered_df['Lenkwinkel'] - 90,  # Adjusting the Lenkwinkel values
                mode='lines',
                name="Lenkwinkel"
            )
        ],
        layout=go.Layout(
            title={"text": f"Lenkwinkel über Zeit (Fahrt {selected_fahrt})","font": {"color": "white"}},
            xaxis={"title": {"text": "Zeit (s)","font": {"color": "white"}}, "tickfont": {"color": "white"}, "gridcolor": "grey", "linecolor": "grey"},
            yaxis={
                "title": {"text": "Lenkwinkel (°)","font": {"color": "white"}},
                "tickfont": {"color": "white"},
                "gridcolor": "grey",
                "linecolor": "grey",
                "dtick": 10  # Setting the tick step to 10 degrees
            },
            height=400,
            paper_bgcolor="rgba(40,40,40,1)",
            plot_bgcolor="rgba(40,40,40,1)"
        )
    )

    ir_status_fig = go.Figure(
        data=[
            go.Scatter(
                x=filtered_df['Zeit'],
                y=filtered_df['IR_Status2'],
                mode='lines',
                name="IR-Status"
            )
        ],
        layout=go.Layout(
            title={"text": f"IR-Status über Zeit (Fahrt {selected_fahrt})","font": {"color": "white"}},
            xaxis={"title": {"text": "Zeit (s)","font": {"color": "white"}}, "tickfont": {"color": "white"}, "gridcolor": "grey", "linecolor": "grey"},
            yaxis={"title": {"text": "IR-Status","font": {"color": "white"}}, "tickfont": {"color": "white"}, "gridcolor": "grey", "linecolor": "grey"},
            height=400,
            paper_bgcolor="rgba(40,40,40,1)",
            plot_bgcolor="rgba(40,40,40,1)"
        )
    )

    # Show or hide the sonic_fig based on Fahrmodus
    sonic_fig_style = {'display': 'block'} if fahrmodus_value in ['3','4', '7'] else {'display': 'none'}
    ir_status_fig_style = {'display': 'block'} if fahrmodus_value in ['5', '6', '7'] else {'display': 'none'}

    return geschwindigkeit_fig, fahrstrecke_fig, sonic_fig, sonic_fig_style, lenkwinkel_fig, ir_status_fig, ir_status_fig_style, vmin_value, vmax_value, vmean_value, fahrzeit_value, fahrstrecke_value, fahrmodus_value

if __name__ == "__main__":
    app.run_server(debug=True, host=ip_host, port=8053)
    
    # print(df)
