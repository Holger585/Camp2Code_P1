import pandas as pd

# CSV-Datei einlesen
df = pd.read_csv('fahrmodus_log.csv')
#df['Geschwindigkeit'] = abs(df['Geschwindigkeit'])
df['Diff_Zeit'] = df['Zeit'].diff().shift(-1).fillna(0)


# Hier werden die verschiedenen Fahrten der log.csv Datei erkannt. 
# Erkennung der Fahrten basierend auf der Spalte Zeit: Von 0 bis 0 = 1 Fahrt.
# Schreibt die Fahrten als ID in eine neue Spalte des df
fahrt_ids = []
current_fahrt_id = 0
for i in range(len(df)):
    if df['Zeit'].iloc[i] == 0:
        # Erhöht die fart_id um 1, wenn eine neue 0 bei Zeit gefunden wird.
        current_fahrt_id += 1
    fahrt_ids.append(current_fahrt_id)

df['FahrtID'] = fahrt_ids


# Berechnung der Fahrstrecke mit stetigem Anstieg
fahrstrecke = []
current_distance = 0
for i in range(len(df)):
    if i > 0 and df['FahrtID'].iloc[i] == df['FahrtID'].iloc[i-1]:
        if df['Geschwindigkeit'].iloc[i-1] == 0:  # Reset wenn vorherige Geschwindigkeit 0 war
            current_distance = 0
        else:
            time_diff = df['Zeit'].iloc[i] - df['Zeit'].iloc[i-1]
            current_distance += df['Geschwindigkeit'].iloc[i-1] * time_diff
    else:
        current_distance = 0
    fahrstrecke.append(current_distance)

df['Fahrstrecke'] = fahrstrecke

# Ermittlung der KPI für die Kopfzeile in eigenem df
fahrt_id_result = 0
result_df= pd.DataFrame()
for i in range(len(df)):
    if df['FahrtID'].iloc[i] != fahrt_id_result:
        fahrt_id_result = df['FahrtID'].iloc[i]
        result_df= pd.concat([result_df,pd.DataFrame({
            'FahrtID': fahrt_id_result,
            'Fahrzeit': [df[df['FahrtID'] == fahrt_id_result]['Zeit'].sum()],
            'Vmin': [df[df['FahrtID'] == fahrt_id_result]['Geschwindigkeit'].min()],
            'Vmax': [df[df['FahrtID'] == fahrt_id_result]['Geschwindigkeit'].max()],
            'Vmean': [df[df['FahrtID'] == fahrt_id_result]['Geschwindigkeit'].abs().mean()],
            'Fahrstrecke': [df[df['FahrtID'] == fahrt_id_result]['Fahrstrecke'].abs().sum()]
        })])

if __name__ == "__main__":
    print(result_df)
    print(df)

# print(f"Fahrzeit1 : {result_df['Fahrzeit']}")
# print(f"Geschwindigkeit min.: {df['Geschwindigkeit'].min()} km/h")
# print(f"Geschwindigkeit max.: {df['Geschwindigkeit'].max()} km/h")
# print(f"Geschwindigkeit mean: {df['Geschwindigkeit'].mean()} km/h")
# print(f"Fahrstrecke gesamt: {df['Fahrstrecke'].sum():.1f} mm")
# print(df)
