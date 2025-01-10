import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json

# CSV-Datei einlesen
df = pd.read_csv('fahrmodus_log.csv')
#df['Geschwindigkeit'] = abs(df['Geschwindigkeit'])

# Konfigurationslogik
try:
    with open("config.json", "r") as f:
        data = json.load(f)
        ip_host = data.get("ip_host", "0.0.0.0")  # Fallback zu "0.0.0.0"
except FileNotFoundError:
    print("Fehler: config.json nicht gefunden. Standardwerte werden verwendet.")
    ip_host = "0.0.0.0"

# Berechnung der Fahrstrecke mit stetigem Anstieg
fahrstrecke = []
current_distance = 0
for i in range(len(df)):
    if i > 0:
        if df['Geschwindigkeit'].iloc[i-1] == 0 and df['Geschwindigkeit'].iloc[i] == 0:  # Bleibt bei 0
            current_distance = 0
        elif df['Geschwindigkeit'].iloc[i-1] == 0:  # Reset wenn vorherige Geschwindigkeit 0 war
            current_distance = 0
        else:
            time_diff = df['Zeit'].iloc[i] - df['Zeit'].iloc[i-1]
            current_distance += df['Geschwindigkeit'].iloc[i-1] * time_diff
    fahrstrecke.append(current_distance)

df['Fahrstrecke'] = fahrstrecke

# Duplikate entfernen
df = df.drop_duplicates(subset=['Zeit', 'Geschwindigkeit']).sort_values('Zeit').reset_index(drop=True)

# Statistiken berechnen
fahrzeit = df['Zeit'].max()
geschwindigkeit_min = df['Geschwindigkeit'].min()
geschwindigkeit_max = df['Geschwindigkeit'].max()
geschwindigkeit_mean = df['Geschwindigkeit'].mean()
fahrstrecke_gesamt = df['Fahrstrecke'].max()

# Dash-App erstellen
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App-Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Fahrmodus-Dashboard", className="text-center"), width=12)),

    dbc.Row([
        dbc.Col([
            html.H4("Statistiken:"),
            html.Ul([
                html.Li(f"Fahrzeit: {fahrzeit:.2f} s"),
                html.Li(f"Geschwindigkeit (min): {geschwindigkeit_min:.2f} km/h"),
                html.Li(f"Geschwindigkeit (max): {geschwindigkeit_max:.2f} km/h"),
                html.Li(f"Geschwindigkeit (mean): {geschwindigkeit_mean:.2f} km/h"),
                html.Li(f"Fahrstrecke gesamt: {fahrstrecke_gesamt:.2f} km"),
            ]),
        ], width=12),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='geschwindigkeit-zeit',
                figure=go.Figure(
                    data=[
                        go.Scatter(
                            x=df['Zeit'],
                            y=df['Geschwindigkeit'],
                            mode='lines',
                            line_shape='hv',  # Horizontale Stufenanzeige
                            name="Geschwindigkeit"
                        )
                    ],
                    layout=go.Layout(
                        title="Geschwindigkeit über Zeit (Stufenanzeige)",
                        xaxis_title="Zeit (s)",
                        yaxis_title="Geschwindigkeit (km/h)",
                        height=400
                    )
                )
            ),
        ], width=12),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='fahrstrecke-zeit',
                figure=go.Figure(
                    data=[
                        go.Scatter(
                            x=df['Zeit'],
                            y=abs(df['Fahrstrecke']),
                            mode='lines',
                            name="Fahrstrecke"
                        )
                    ],
                    layout=go.Layout(
                        title="Fahrstrecke über Zeit",
                        xaxis_title="Zeit (s)",
                        yaxis_title="Fahrstrecke (km)",
                        height=400
                    )
                )
            ),
        ], width=12),
    ]),
], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True, host=ip_host, port=8052)
