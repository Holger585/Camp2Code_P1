from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from soniccar import SonicCar
import json
from app_data import result_df

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

auto = SonicCar()

x = list(range(30))

df = pd.DataFrame({"x": x, "y": [i**2 for i in x], "z": [i**0.5 for i in x]})

# Konfigurationslogik
try:
    with open("config.json", "r") as f:
        data = json.load(f)
        ip_host = data.get("ip_host", "0.0.0.0")  # Fallback zu "0.0.0.0"
except FileNotFoundError:
    print("Fehler: config.json nicht gefunden. Standardwerte werden verwendet.")
    ip_host = "0.0.0.0"

# App Layout
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("Hallo Dash Welt Projektphase 1", id="my-header"), width={"size": 6, "offset": 3}),
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(html.H2(f"Geschwindigkeit min: {result_df['Vmin'].iloc[0]} km/h", id="Vmin"), width={"size": 6, "offset": 3}),
                dbc.Col(html.H2(f"Geschwindigkeit max: {result_df['Vmax'].iloc[0]} km/h", id="Vmax"), width={"size": 6, "offset": 3}),
                dbc.Col(html.H2(f"Geschwindigkeit mean: {result_df['Vmean'].iloc[0]} km/h", id="Vmean"), width={"size": 6, "offset": 3}),
                dbc.Col(html.H2(f"Fahrstrecke: {result_df['Strecke'].iloc[0]:.1f} mm", id="Fahrstrecke"), width={"size": 6, "offset": 3}),
                dbc.Col(html.H2(f"Fahrzeit: {result_df['Fahrzeit'].iloc[0]} s", id="Fahrzeit"), width={"size": 6, "offset": 3})
            ],                                         
            className="mb-4",
        ),        
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        ["x", "y", "z"],
                        value="x",
                        id="my-dd",
                        className="mb-2",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dcc.Slider(
                        min=1,
                        max=10,
                        step=1,
                        value=5,
                        id="my-slider",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id="my-graph"), width=12),
            className="mb-4",
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Stop", id="stop-button", color="danger", className="btn-lg"),
                width={"size": 2, "offset": 5},
            )
        ),
    ],
    fluid=True,
)

# Verknüpfungen bzw. Funktionen
@app.callback(Output("my-header", "children"), Input("my-dd", "value"), prevent_initial_call=True)
def change_header(selected_value):
    return f"Meine Auswahl war: {selected_value}"

# @app.callback(Output("Vmin", "children"), Input("my-dd", "value"))
# def change_vmin(selected_id):
#     vmin_value = result_df[result_df['ID'] == selected_id]['Vmin'].iloc[0]
#     print(vmin_value)
#     return f"Vmin: {vmin_value}"
    


@app.callback(
    Output("my-header", "children", allow_duplicate=True),
    [Input("my-dd", "value"), Input("my-slider", "value")],
    prevent_initial_call=True,
)
def change_header_2(dd_value, slide_value):
    return f"Der zweite Callback: {dd_value * int(slide_value)}"


@app.callback(Output("my-graph", "figure"), Input("my-dd", "value"))
def upgrade_line_plot(dd_value):
    fig = px.line(df, x="x", y=dd_value)
    return fig


# Callback zum Stoppen des Autos
@app.callback(
    Output("stop-button", "n_clicks"),
    Input("stop-button", "n_clicks"),
    prevent_initial_call=True,
)
def stop_car(n_clicks):
    if n_clicks:
        auto.stop()  # Stopp das Auto
    return n_clicks


if __name__ == "__main__":
    app.run_server(debug=True, host=ip_host, port=8051)
    print(result_df)
