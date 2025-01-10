import pandas as pd

# CSV-Datei einlesen
df = pd.read_csv('fahrmodus_log.csv')
df['Fahrstrecke'] = df['Geschwindigkeit'] * 10
print(f"Fahrzeit : {df['Zeit'].max()} s")
print(f"Geschwindigkeit min.: {df['Geschwindigkeit'].min()} km/h")
print(f"Geschwindigkeit max.: {df['Geschwindigkeit'].max()} km/h")
print(f"Geschwindigkeit mean: {df['Geschwindigkeit'].mean()} km/h")
print(df)

