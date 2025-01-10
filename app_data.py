import pandas as pd

# CSV-Datei einlesen
df = pd.read_csv('fahrmodus_log.csv')
df['Geschwindigkeit'] = abs(df['Geschwindigkeit'])
df['Diff_Zeit'] = df['Zeit'].diff().shift(-1).fillna(0)
df['Fahrstrecke'] = df['Geschwindigkeit'] * df['Diff_Zeit']

fahrzeit = df['Zeit'].max()
result_df = pd.DataFrame({
    'Fahrzeit': [df['Zeit'].max()],
    'Vmin': [df['Geschwindigkeit'].min()],
    'Vmax': [df['Geschwindigkeit'].max()],
    'Vmean': [df['Geschwindigkeit'].mean()],
    'Strecke': [df['Fahrstrecke'].sum()]
    })

# result_df = pd.DataFrame({
#     'Fahrzeit': [fahrzeit],

    # })

print(result_df)

# print(f"Fahrzeit1 : {result_df['Fahrzeit']}")
# print(f"Geschwindigkeit min.: {df['Geschwindigkeit'].min()} km/h")
# print(f"Geschwindigkeit max.: {df['Geschwindigkeit'].max()} km/h")
# print(f"Geschwindigkeit mean: {df['Geschwindigkeit'].mean()} km/h")
# print(f"Fahrstrecke gesamt: {df['Fahrstrecke'].sum():.1f} mm")
# print(df)
