import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json
from dash.dependencies import Output, Input
from app_data import *

# Konfigurationslogik
try:
    with open("config.json", "r") as f:
        data = json.load(f)
        ip_host = data.get("ip_host", "0.0.0.0")  # Fallback zu "0.0.0.0"
except FileNotFoundError:
    print("Fehler: config.json nicht gefunden. Standardwerte werden verwendet.")
    ip_host = "0.0.0.0"

# Dash-App erstellen
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
                    dbc.Col(html.H2(f"Geschwindigkeit min: --- km/h", id="Vmin"), width={"size": 6, "offset": 3}),
                    dbc.Col(html.H2(f"Geschwindigkeit max: --- km/h", id="Vmax"), width={"size": 6, "offset": 3}),
                    dbc.Col(html.H2(f"Geschwindigkeit mean: --- km/h", id="Vmean"), width={"size": 6, "offset": 3}),
                    dbc.Col(html.H2(f"Fahrstrecke: --- mm", id="Fahrstrecke"), width={"size": 6, "offset": 3}),
                    dbc.Col(html.H2(f"Fahrzeit: --- s", id="Fahrzeit"), width={"size": 6, "offset": 3})
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
    [
        Output('geschwindigkeit-zeit', 'figure'),
        Output('fahrstrecke-zeit', 'figure'),
        Output('Vmin', 'children'),
        Output('Vmax', 'children'),
        Output('Vmean', 'children'),
        Output('Fahrzeit', 'children'),
        Output('Fahrstrecke', 'children')
    ],
    [
        Input('fahrt-dropdown', 'value')
    ]
)
def update_diagrams(selected_fahrt):
    filtered_df = df[df['FahrtID'] == selected_fahrt]

    vmax_value = f"Geschwindigkeit max: {result_df[result_df['FahrtID'] == selected_fahrt]['Vmax'].iloc[0]} km/h"
    vmin_value = f"Geschwindigkeit min: {result_df[result_df['FahrtID'] == selected_fahrt]['Vmin'].iloc[0]} km/h"
    vmean_value = f"Geschwindigkeit mean: {result_df[result_df['FahrtID'] == selected_fahrt]['Vmean'].iloc[0]} km/h"
    fahrzeit_value = f"Fahrzeit: {result_df[result_df['FahrtID'] == selected_fahrt]['Fahrzeit'].iloc[0]} s"
    fahrstrecke_value = f"Fahrstrecke: {result_df[result_df['FahrtID'] == selected_fahrt]['Fahrstrecke'].iloc[0]} mm"
    
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

    return geschwindigkeit_fig, fahrstrecke_fig, vmin_value, vmax_value, vmean_value, fahrzeit_value, fahrstrecke_value

if __name__ == "__main__":
    app.run_server(debug=True, host=ip_host, port=8053)
    print(df)
