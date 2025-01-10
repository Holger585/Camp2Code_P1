import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import json
from app_data import result_df

#Konfiguration einlesen
try:
    with open("config.json", "r") as f:
        data = json.load(f)
        ip_host = data.get("ip_host", "0.0.0.0")  # Fallback zu "0.0.0.0"
except FileNotFoundError:
    print("Fehler: config.json nicht gefunden. Standardwerte werden verwendet.")
    ip_host = "0.0.0.0"

# Erstelle eine Dash-App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Definiere das Layout der App
app.layout = html.Div(
    [
        # Überschrift
        html.H1("Hübsches, responsives Dashboard", style={"textAlign": "center", "marginBottom": "30px"}),

        # 3 Slider - Responsiv über dbc.Row und dbc.Col
        dbc.Row(
            [
                dbc.Col(
                    dcc.Slider(
                        id="slider-1",
                        min=0,
                        max=100,
                        step=1,
                        value=50,
                        marks={i: str(i) for i in range(0, 101, 10)},
                    ),
                    width=12,  # Vollbreite für kleinere Bildschirme
                    lg=4,      # 4 von 12 Spalten für größere Bildschirme
                ),
                dbc.Col(
                    dcc.Slider(
                        id="slider-2",
                        min=0,
                        max=100,
                        step=1,
                        value=50,
                        marks={i: str(i) for i in range(0, 101, 10)},
                    ),
                    width=12,
                    lg=4,
                ),
                dbc.Col(
                    dcc.Slider(
                        id="slider-3",
                        min=0,
                        max=100,
                        step=1,
                        value=50,
                        marks={i: str(i) for i in range(0, 101, 10)},
                    ),
                    width=12,
                    lg=4,
                ),
            ],
            style={"marginBottom": "30px"},
        ),

        # 4 Buttons - responsiv und in einer Reihe
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Button 1", color="primary", className="mb-3"),
                    width=6,  # 6 von 12 Spalten für mittlere Bildschirme
                    sm=6,     # 6 von 12 Spalten für kleine Bildschirme
                    md=3,     # 3 von 12 Spalten für mittlere Bildschirme
                ),
                dbc.Col(
                    dbc.Button("Button 2", color="secondary", className="mb-3"),
                    width=6,
                    sm=6,
                    md=3,
                ),
                dbc.Col(
                    dbc.Button("Button 3", color="success", className="mb-3"),
                    width=6,
                    sm=6,
                    md=3,
                ),
                dbc.Col(
                    dbc.Button("Button 4", color="danger", className="mb-3"),
                    width=6,
                    sm=6,
                    md=3,
                ),
            ],
            style={"marginBottom": "30px"},
        ),
    ],
    style={"padding": "30px"},
)

# Starte die App
if __name__ == "__main__":
    app.run_server(debug=True, host=ip_host, port=8051)
