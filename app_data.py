import pandas as pd

# CSV-Datei einlesen
df = pd.read_csv('fahrmodus_log.csv')
df['Geschwindigkeit'] = abs(df['Geschwindigkeit'])
df['Fahrstrecke'] = df['Geschwindigkeit'] * df['Zeit'].diff().fillna(0)

print(f"Fahrzeit : {df['Zeit'].max()} s")
print(f"Geschwindigkeit min.: {df['Geschwindigkeit'].min()} km/h")
print(f"Geschwindigkeit max.: {df['Geschwindigkeit'].max()} km/h")
print(f"Geschwindigkeit mean: {df['Geschwindigkeit'].mean()} km/h")
print(f"Fahrstrecke gesamt: {df['Fahrstrecke'].sum()} km")
print(df)

