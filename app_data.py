import pandas as pd

class Data():
    """
    Klasse zum Verarbeiten und Analysieren von Fahrtdaten aus einer CSV-Datei.
    """

    def __init__(self):
        """
        Initialisiert die Data-Klasse und liest die Daten aus der CSV-Datei ein.
        """
        self.read_data()     

    def read_data(self):
        """
        Liest die Fahrtdaten aus der CSV-Datei ein, berechnet zusätzliche Spalten und erstellt eine Zusammenfassung.
        """
        # CSV-Datei einlesen
        df = pd.read_csv('fahrmodus_log.csv')
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
                time_diff = df['Zeit'].iloc[i] - df['Zeit'].iloc[i-1]
                current_distance += ((abs(df['Geschwindigkeit'].iloc[i-1])/2) * time_diff)/100
            else:
                current_distance = 0
            fahrstrecke.append(current_distance)

        df['Fahrstrecke'] = fahrstrecke

        # Ermittlung der KPI für die Kopfzeile in eigenem df
        fahrt_id_result = 0
        result_df = pd.DataFrame()
        for i in range(len(df)):
            if df['FahrtID'].iloc[i] != fahrt_id_result:
                fahrt_id_result = df['FahrtID'].iloc[i]
                result_df = pd.concat([result_df, pd.DataFrame({
                    'FahrtID': fahrt_id_result,
                    'Fahrzeit': [df[df['FahrtID'] == fahrt_id_result]['Zeit'].max()],
                    'Vmin': [(df[df['FahrtID'] == fahrt_id_result]['Geschwindigkeit'].min()/2)],
                    'Vmax': [(df[df['FahrtID'] == fahrt_id_result]['Geschwindigkeit'].max()/2)],
                    'Vmean': [(df[df['FahrtID'] == fahrt_id_result]['Geschwindigkeit'].abs().mean()/2)],
                    'Fahrstrecke': [df[df['FahrtID'] == fahrt_id_result]['Fahrstrecke'].max()],
                    'Fahrmodus': [df[df['FahrtID'] == fahrt_id_result]['Fahrmodus'].max()]
                })])
        self.result_df = result_df
        self.df = df

if __name__ == "__main__":
    data = Data()
    print(data.result_df)
    print(data.df)
