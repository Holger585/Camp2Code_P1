# Detaillierte Gesamtdokumentation des RPiCar-Projekts

Diese Dokumentation ist so konzipiert, dass du selbst nach längerer Zeit (z. B. einem halben Jahr) noch im Detail nachvollziehen kannst, wie alle Programmteile funktionieren und zusammenhängen.  

---

## 1. Projektziel und Struktur

### 1.1 Überblick
- **Projektziel**: Ein autonomes (bzw. teils ferngesteuertes) Modellfahrzeug auf Basis eines Raspberry Pi, das mittels Ultraschallsensor und IR-Sensoren verschiedene Fahrmodi (u. a. Linienverfolgung, Hindernis-Erkennung) unterstützt.  
- **Wesentlicher Aufbau**:
  1. **Basisklassen** (in `basisklasse.py`), unverändert vom Projekt bereitgestellt.  
  2. **Eigene Fahrzeugklassen**:
     - `basecar.py` (Grundfunktionen),  
     - `soniccar.py` (Ultraschall),  
     - `sensorcar.py` (Ultraschall + Infrarot).  
  3. **Datenanalyse** (`app_data.py`) für geloggte Fahrtdaten.  
  4. **Dash-GUI** (`app_gui.py`) zum Steuern und Visualisieren der Fahrten.  

### 1.2 Gesamtablauf (kurz)
1. **User** startet `app_gui.py`  
2. **GUI** (Dash) lädt `car = SensorCar()` und `data = Data()`.  
3. **SensorCar** deckt alle Fahrmodi ab (1–7), kann Hindernisse via Ultraschall erkennen oder Linien mit IR verfolgen.  
4. **app_data.py** analysiert das Fahrprotokoll (`fahrmodus_log.csv`) mit pandas.  
5. **app_gui.py** zeigt Buttons zur Moduswahl, Diagramme für Echtzeit-/Nachtragauswertung.  

---

## 2. Basisklasse (`basisklasse.py`)

Vom Projektteam vorgegeben, **nicht modifiziert**. Enthält:

1. **`Ultrasonic`**  
   - Steuert den Ultraschallsensor (Trigger/Echo).  
   - Methode `distance()` ermittelt Distanz in cm (ggf. Fehlerwerte bei Timeouts).

2. **`Infrared`**  
   - Liest (digital/analog) Infrarotwerte einer 5er-Sensorleiste aus.  
   - Hilfsmethoden zum Kalibrieren (Messung von Hintergrund und Linie).

3. **`FrontWheels`**  
   - Ansteuerung des Servomotors für die Vorderräder.  
   - Beschränkt den Winkel auf maximal ±45° (standardmäßig zwischen 45° und 135°).

4. **`BackWheels`**  
   - Verwaltet die beiden DC-Motoren für den Hinterradantrieb.  
   - Setzt Geschwindigkeit (0–100) und Fahrtrichtung (Vorwärts/ Rückwärts).

5. **Hilfsklassen** (`Servo`, `Motor`, `PWM` etc.)  
   - Detaillieren die Grundlagen für PWM-Signale, Motorsteuerung und I2C-Kommunikation.  

**Du arbeitest lediglich mit deren Schnittstellen**, z. B. `FrontWheels().turn(...)`, `BackWheels().speed = 50`, `Ultrasonic().distance()` und `Infrared().read_digital()`.

---

## 3. `basecar.py` – Die Grundfahrzeug-Klasse

### 3.1 Klasse `BaseCar`
- **Zweck**: Basisklasse, um das Fahrzeug in einfachster Form zu steuern (Lenken, Fahren, Stoppen).  
- **Konstruktor**:
  - Erstellt Objekte: `self.frontwheels = FrontWheels()`, `self.backwheels = BackWheels()`  
  - Initialisiert interne Variablen `_speed`, `_steering_angle`, `_direction` (z. B. 0 = kein Fahren, 90° = geradeaus).  
  - Kann Konfigurationen (z. B. offset für Lenkung, forward_A/B) aus `config.json` laden.

### 3.2 Properties
1. **`speed`** (int)  
   - Bereich: -100 bis +100  
   - **Setter** begrenzt Werte (clamping).  
   - +Wert = Vorwärts, 0 = Stopp, -Wert = Rückwärts.  
   - Passt `self._direction` an (1, 0, -1).
2. **`steering_angle`** (int)  
   - Bereich: 45° bis 135°  
   - 90° = Geradeaus  
   - **Setter** begrenzt automatisch, wenn man z. B. 10 oder 200 setzt, wird auf 45 bzw. 135 korrigiert.
3. **`direction`** (Read-only)  
   - Gibt 1 (Vorwärts), 0 (Stillstand), -1 (Rückwärts) zurück.

### 3.3 Methoden
- **`drive(speed=None, steering_angle=None)`**  
  - Falls `speed` angegeben, wird `self.speed` gesetzt.  
  - Falls `steering_angle` angegeben, wird `self.steering_angle` gesetzt.  
  - Wenn das Fahrzeug vorwärtsfahren soll, ruft `self.backwheels.forward()` auf. Bei negativen Werten `self.backwheels.backward()`.  
  - `self.backwheels.speed = abs(self.speed)`.
- **`stop()`**  
  - Setzt `speed` = 0 und ruft `self.backwheels.stop()` auf.  
  - `direction` wird dadurch zu 0.

### 3.4 Beispiel-Fahrmodi  
- **Fahrmodus 1** (in `basecar.py` oder darüber hinaus umgesetzt): 3 s vorwärts, 1 s Stop, 3 s rückwärts.  
- **Fahrmodus 2**: Kreisfahrt mit maximalem Lenkanschlag (z. B. 8 s), dann Rückwärts.  

---

## 4. `soniccar.py` – Ultraschallerweiterung

### 4.1 Klasse `SonicCar`
- **Erbt**: `BaseCar`  
- **Ergänzt**: `ultrasonic = Ultrasonic()` aus `basisklasse.py`  
- **Methode**:
  - `get_distance()`: Liest per `ultrasonic.distance()` den aktuellen cm-Wert. Ggf. -1, -2, -3 bei Fehlern.  

### 4.2 Fahrmodi
- **Fahrmodus 3**: „Vorwärts bis Hindernis“  
  - Startet Vorwärtsfahrt (z. B. `speed=50`), Schleife prüft via `get_distance()`, ob Wert < `mindist`.  
  - Bei Unterschreitung → `stop()`.  
- **Fahrmodus 4**: „Erkundungstour“  
  - Zufällige oder flexible Richtungswechsel bei Hindernis.  
  - Kann z. B. `car.drive(...)` anweisen, bei `distance < mindist` → Rückwärts + Lenkung, danach wieder Vorwärts.

### 4.3 Datenlogging
- In der Implementierung (z. B. `fahrmodus_3()`) wird üblicherweise `self.loggen(...)` aufgerufen, um Fahrzustände (Zeit, Speed, Distance) in einer CSV-Datei oder internen Liste zu speichern.

---

## 5. `sensorcar.py` – IR- und Ultraschall vereint

### 5.1 Klasse `SensorCar`
- **Erbt**: `SonicCar` → Hat also alle Methoden von `BaseCar` + Ultraschall.  
- **Neu**: `self.infrared = Infrared()`.  
- **Kalibrierung**: Setzt IR-Referenzwerte (Hintergrund, Linie) in der Instanz oder `config.json`.

### 5.2 Fahrmodi
1. **Fahrmodus 5**: Einfaches Folgen einer Linie (gerade, weite Kurven).  
2. **Fahrmodus 6**: Erweiterte Linienverfolgung (enges Kurvenfahren, ggf. Rundkurs).  
3. **Fahrmodus 7**: Linienverfolgung + Abstandsprüfung (Ultraschall). Wenn `distance < mindist`, Stop.  

### 5.3 Datenlogging
- Liest IR-Sensorwerte (z. B. digital `[0,1,1,0,1]`) und speichert sie zusammen mit Fahrtzuständen in `fahrmodus_log.csv`.

---

## 6. `app_data.py` – Datenanalyseschicht

### 6.1 Klasse `Data`
- **Kernaufgabe**: CSV-Logs (typisch `fahrmodus_log.csv`) laden und in einem `pandas.DataFrame` bereitstellen.  
- **`read_data()`**:
  - Liest CSV. Spaltet Einträge in Zeit, Speed, Lenkwinkel, Abstände, IR-Status usw.  
  - Erzeugt **`df`**: Komplette Zeilen (Messung pro Zeitabschnitt).  
  - Erzeugt **`result_df`**: Kennwerte je Fahrt (Fahrt-ID), z. B. Vmin, Vmax, Vmean, Fahrzeit, Fahrmodus.  
- **Verwendung in `app_gui.py`**:  
  - Wir greifen auf `data.df` zu, um Diagramme zu erstellen, und auf `data.result_df` für KPIs (z. B. max. Geschwindigkeit).

---

## 7. `app_gui.py` – Zentrale Dash-GUI (Neueste Version)

Im Folgenden die ausführlichste Beschreibung, da dies das Kern-UI-Element ist.

### 7.1 Allgemeines
- **GUI**: Basiert auf [Dash](https://dash.plotly.com/) + `dash_bootstrap_components`.  
- **Start**: `python3 app_gui.py`  
- **Browser**: Standardmäßig IP `0.0.0.0` und Port `8053` (konfigurierbar via `config.json`).  
- **Funktionen**:  
  1. Anzeige und Update von Fahrdaten (Diagramme, Kennzahlen).  
  2. Start von Fahrmodi 1–7 per Buttonklick.  
  3. Stop-Funktion, Kalibrierung, manueller Modus (Vor/Zurück/Links/Rechts).

### 7.2 Hauptbestandteile
1. **Importe**  
   - `dash`, `html`, `dcc`, `dbc` (Bootstrap), `plotly.graph_objects`.  
   - Eigene Module: `Data` (app_data.py), `SensorCar` (sensorcar.py).  
   - `SaveConfig`: Kleine Hilfsklasse zum Schreiben von `config.json`.  

2. **Konfiguration**  
   - Zu Beginn werden `config.json` eingelesen → `ip_host`, `car.vmax_vorgabe`, `car.maxwinkel_vorgabe`, `car.mindist_vorgabe`.  
   - Objekt `car = SensorCar()` wird erstellt.  
   - Objekt `data = Data()` lädt bereits vorhandene Fahrdaten, um Diagramme initial zu füllen.

3. **Layout-Aufbau**  
   - **Titelzeile**: „Fahrmodus-Dashboard“.  
   - **Buttons**:  
     - `btFM1` bis `btFM7` (Fahrmodus 1–7).  
     - `btStopp` (Stoppen einer Fahrt).  
     - `btCali` (Kalibrierung IR-Sensor).  
     - `collapse-button` (öffnet manuellen Modus).  
   - **Manueller Fahrmodus**: Buttons „Vor“, „Zurück“, „Links“, „Rechts“, „Stop“ innerhalb einer ausklappbaren Card.  
   - **Dropdowns**:  
     - `vmax_vorgabe` (max. Geschwindigkeit)  
     - `maxwinkel_vorgabe` (Lenkwinkel ±15/30/45°)  
     - `mindist_vorgabe` (Minimalabstand 0, 5, 10, 15 cm)  
   - **Fahrt-Auswahl**: `fahrt-dropdown` (ermöglicht Auswahl einer vorherigen Fahrt).  
   - **KPIs**: min. Speed, max. Speed, mean Speed, Fahrzeit, Fahrstrecke, Fahrmodus (als Karten).  
   - **Diagramme** (in Rows):  
     1. `geschwindigkeit-zeit` (Geschwindigkeit vs. Zeit)  
     2. `lenkwinkel-zeit` (Lenkwinkel vs. Zeit)  
     3. `sonic-zeit` (Ultraschall vs. Zeit, ausblendbar)  
     4. `ir-status-zeit` (IR-Sensorstatus vs. Zeit, ausblendbar)  
     5. `fahrstrecke-zeit` (Entwicklung der gefahrenen Strecke)  

### 7.3 Callbacks (wichtigste Teile)
- **Fahrmodus-Buttons**  
  - Beispiel: `btFM1`  
    1. Erstes Callback: Setzt Buttons disabled, zeigt `[dbc.Spinner(size="sm"), " FM1 aktiv..."]`, `color='warning'`.  
    2. Zweites Callback: Bemerkt den `warning`-Zustand → ruft `car.fahrmodus(1, speed=..., mindist=...)` auf, anschließend `data.read_data()` (lädt neue Log-Einträge). Schaltet Buttons wieder frei.  
- **Stop-Button**  
  - Setzt `car.ismanually_stopped = True`. Jeder Fahrmodus bricht ab. Button-Labels werden auf Normalzustand gesetzt.  
- **Kalibrierung** (`btCali`)  
  - Reagiert auf `n_clicks % 4`:
    - 1. Klick: „Fzg. auf Hintergrund stellen“ → fixiert Lenkwinkel auf 90.  
    - 2. Klick: Liest Hintergrundwerte: `car.background = car.infrared.get_average(100)`.  
    - 3. Klick: Liest Linienwerte: IR-Referenz = (Linie + Hintergrund)/2, speichert in `config.json`.  
    - 4. Klick: Setzt Button-Text auf „Neukalibrierung starten“ und resettet die Anzeige.  
- **Manueller Modus** (Aus- und Einklappen)  
  - `collapse-button`: toggelt `is_open` in einer `dbc.Collapse`. Enthält Buttons:
    - `btVor`, `btZurueck`: Setzt `car.drive(...)` vorwärts bzw. rückwärts.  
    - `btLinks`, `btRechts`: Justiert nur den Lenkwinkel, z. B. `90 - maxwinkel_vorgabe` oder `90 + maxwinkel_vorgabe`.  
    - `btStop`: Ruft `car.stop()` auf.  
- **Dropdowns** für Konfiguration  
  - Jede Änderung speichert den Wert in `car.vmax_vorgabe`, `car.maxwinkel_vorgabe`, `car.mindist_vorgabe`. `save_config.save_config(...)` schreibt es in `config.json`.  
- **Diagramm-Callback** (`update_diagrams`)  
  1. `selected_fahrt` = gewählte Fahrt-ID aus `fahrt-dropdown`.  
  2. `filtered_df = data.df[data.df['FahrtID'] == selected_fahrt]` filtert Fahrten.  
  3. Berechnet Kennzahlen wie `vmax_value`, `vmin_value` usw. aus `data.result_df`.  
  4. Generiert Plotly-Figures:
     - Geschwindigkeit vs. Zeit (mit 0-Linie)  
     - Fahrstrecke vs. Zeit  
     - Ultraschall (Abstand) vs. Zeit, ggf. roter Strich bei `car.mindist_vorgabe`.  
     - Lenkwinkel vs. Zeit (Umrechnung: angezeigter Wert - 90).  
     - IR-Status vs. Zeit.  
  5. Entscheidet mittels `fahrmodus_value`, ob Sonic-Plot und IR-Plot ein- oder ausgeblendet werden.  

### 7.4 Start (Main)
```python
if __name__ == "__main__":
    app.run_server(debug=True, host=ip_host, port=8053)
