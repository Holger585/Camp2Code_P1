import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json
from dash.dependencies import Output, Input

# CSV-Datei einlesen
df = pd.read_csv('fahrmodus_log.csv')

# Konfigurationslogik
try:
    with open("config.json", "r") as f:
        data = json.load(f)
        ip_host = data.get("ip_host", "0.0.0.0")  # Fallback zu "0.0.0.0"
except FileNotFoundError:
    print("Fehler: config.json nicht gefunden. Standardwerte werden verwendet.")
    ip_host = "0.0.0.0"

# Erkennung der Fahrten basierend auf Zeit = 0
fahrt_ids = []
current_fahrt_id = 1
for i in range(len(df)):
    if df['Zeit'].iloc[i] == 0:
        current_fahrt_id += 1
    fahrt_ids.append(current_fahrt_id)

df['FahrtID'] = fahrt_ids

# Berechnung der Fahrstrecke mit stetigem Anstieg
fahrstrecke = []
current_distance = 0
for i in range(len(df)):
    if i > 0 and df['FahrtID'].iloc[i] == df['FahrtID'].iloc[i-1]:
        if df['Geschwindigkeit'].iloc[i-1] == 0 and df['Geschwindigkeit'].iloc[i] == 0:  # Bleibt bei 0
            current_distance = 0
        elif df['Geschwindigkeit'].iloc[i-1] == 0:  # Reset wenn vorherige Geschwindigkeit 0 war
            current_distance = 0
        else:
            time_diff = df['Zeit'].iloc[i] - df['Zeit'].iloc[i-1]
            current_distance += df['Geschwindigkeit'].iloc[i-1] * time_diff
    else:
        current_distance = 0
    fahrstrecke.append(abs(current_distance))

df['Fahrstrecke'] = fahrstrecke

# Duplikate entfernen
df = df.drop_duplicates(subset=['Zeit', 'Geschwindigkeit', 'FahrtID']).sort_values(['FahrtID', 'Zeit']).reset_index(drop=True)

# Dash-App erstellen
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
    [
        Output('geschwindigkeit-zeit', 'figure'),
        Output('fahrstrecke-zeit', 'figure')
    ],
    [
        Input('fahrt-dropdown', 'value')
    ]
)
def update_diagrams(selected_fahrt):
    filtered_df = df[df['FahrtID'] == selected_fahrt]

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
            height=400
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
            height=400
        )
    )

    return geschwindigkeit_fig, fahrstrecke_fig

if __name__ == "__main__":
    app.run_server(debug=True, host=ip_host, port=8053)
