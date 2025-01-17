# Gesamtdokumentation des RPiCar-Projekts

Diese Markdown-Datei dient als ausführliche Erklärung sämtlicher Python-Skripte des Projekts. Sie ist so konzipiert, dass du selbst nach mehreren Monaten noch nachvollziehen kannst, wie alles aufgebaut ist und zusammenarbeitet.

---

## 1. Überblick über alle Dateien

### 1.1 **`basisklasse.py`**
- **Inhalt**: Hier finden sich unveränderte Grundklassen für Sensorik und Antrieb, bereitgestellt von den Projektbetreuern (SunFounder PiCar-S Basisklassen).  
- **Hauptklassen**:
  - `Ultrasonic`: Ansteuerung des Ultraschallsensors (Entfernungsmessung).  
  - `Infrared`: Ansteuerung und Auswertung des IR-Sensor-Arrays (Linienverfolgung).  
  - `FrontWheels`: Ermöglicht die Steuerung (Lenkung) der Vorderräder über einen Servomotor.  
  - `BackWheels`: Ermöglicht das Regeln der beiden DC-Motoren für den Hinterradantrieb.  
- **Zweck**: Diese Klassen brauchst du nicht zu verändern, sie werden **nur** importiert und in den eigenen Modulen genutzt.

---

### 1.2 **`basecar.py`**
- **Zweck**: Stellt die Basisklasse des Fahrzeugs bereit, in der alle grundlegenden Fahrfunktionen wie Vorwärts-/Rückwärtsfahren, Lenken und Stoppen implementiert sind.  
- **Klasse**: `BaseCar`  
  - **Attribute**  
    - `frontwheels`: Instanz von `FrontWheels` (aus `basisklasse.py`).  
    - `backwheels`: Instanz von `BackWheels` (aus `basisklasse.py`).  
    - `_speed`, `_steering_angle`, `_direction`: Interne Variablen für Geschwindigkeit, Lenkwinkel und Fahrtrichtung.  
  - **Properties**  
    - `speed`: Integer von -100 (Rückwärts) bis +100 (Vorwärts), 0 = Stillstand.  
    - `steering_angle`: Integer 45° bis 135°, wobei 90° „geradeaus“ repräsentiert.  
    - `direction`: Read-only (1, 0, -1), hängt vom Vorzeichen von `speed` ab.  
  - **Methoden**  
    - `drive(speed=None, steering_angle=None)`: Ändert (optional) Geschwindigkeit und Lenkwinkel.  
    - `stop()`: Setzt `speed` auf 0 und stoppt das Fahrzeug.  
  - **Verwendung**:  
    - Fahrmodus 1 & 2 (z. B. 3 s vorwärts, 1 s Stopp, 3 s rückwärts; Kreisfahrt mit maximalem Lenkwinkel) basieren auf `BaseCar`.

---

### 1.3 **`soniccar.py`**
- **Zweck**: Erbt von `BaseCar` und erweitert es um Ultraschallsensorik.  
- **Klasse**: `SonicCar`  
  - **Erbt**: Methoden und Properties von `BaseCar`.  
  - **Zusätzlich**:  
    - `ultrasonic` (Objekt von `Ultrasonic`, aus `basisklasse.py`).  
    - `get_distance()`: Liest den aktuellen Messwert des Ultraschallsensors.  
  - **Fahrmodi**  
    - Fahrmodus 3: Vorwärtsfahrt bis Hindernis < `mindist`, dann Stopp.  
    - Fahrmodus 4: Erkundungstour, bei Hindernissen Anpassung der Fahrtrichtung.  
  - **Protokollierung**: Schreibt Daten (u. a. Zeit, Geschwindigkeit, Abstand) in eine interne Liste, sodass sie später für Auswertungen verfügbar sind.

---

### 1.4 **`sensorcar.py`**
- **Zweck**: Erbt von `SonicCar` und integriert zusätzlich die Infrarotsensorik.  
- **Klasse**: `SensorCar`  
  - **Erbt**: Alles von `SonicCar` (somit auch `BaseCar` + Ultraschall).  
  - **Zusätzlich**:  
    - `infrared` (Objekt von `Infrared`).  
    - Linienverfolgung: Fahrmodi 5, 6, 7 (teilweise in Kombination mit Ultraschall).  
  - **Fahrmodi**  
    - Fahrmodus 5: Einfache Linienverfolgung (große Kurven).  
    - Fahrmodus 6: Erweiterte Linienverfolgung (auch enge Kurven).  
    - Fahrmodus 7: Linienverfolgung + Hinderniserkennung (Stoppt bei `distance < mindist`).  
  - **Kalibrierung**: Erlaubt das Einlesen und Setzen von IR-Referenzwerten (z. B. aus `config.json`).

---

### 1.5 **`app_data.py`**
- **Zweck**: Ermöglicht die Auswertung aller Fahrdaten in einem DataFrame und das Erstellen von Kenngrößen.  
- **Klasse**: `Data`  
  - **Kernmethode**: `read_data()`:  
    - Liest `fahrmodus_log.csv` ein und erzeugt ein pandas-DataFrame `df`.  
    - Berechnet Kennwerte (Fahrzeit, min./max./mean-Geschwindigkeit, Fahrstrecke usw.).  
    - Speichert zusammengefasste Ergebnisse in `result_df`.  
- **Benutzung**:  
  - Wird in der GUI (`app_gui.py`) instanziiert, um Diagramme und KPI-Karten zu füllen.

---

### 1.6 **`app_gui.py`** (aktualisierte Version)

#### 1.6.1 Allgemeines
- **Zweck**: Dash-Applikation, die (1) das Fahrzeug steuert (Buttons, Dropdowns) und (2) die Fahrt- und Sensordaten als Diagramme und Kennzahlen visualisiert.  
- **Beispielstart**: In der Konsole `python3 app_gui.py` → Browser starten → Dashboard verwenden.

#### 1.6.2 Aufbau
1. **Importe**  
   - `dash`, `dbc` (dash_bootstrap_components), `plotly.graph_objects`  
   - `json`, `numpy`  
   - `Data` (aus `app_data.py`), `SensorCar` (aus `sensorcar.py`)  
2. **Objekte**  
   - `car = SensorCar()`: Das Fahrzeugobjekt mit Ultraschall & IR.  
   - `data = Data()`: Dient zur Datenanalyse.  
   - `SaveConfig()`: Kleine Hilfsklasse zum Speichern von Einstellungswerten (`Vmax`, `LWmax`, `DISTmin`) in `config.json`.  
3. **Konfigurationslogik**  
   - Liest `config.json`. Falls vorhanden, werden `ip_host`, `car.vmax_vorgabe`, `car.maxwinkel_vorgabe`, `car.mindist_vorgabe` gesetzt.  
   - Falls `config.json` fehlt, werden Standardwerte genommen.  
4. **Dash-App erstellen**:  
   - `app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])`  
   - In der Layout-Definition werden Buttons, Dropdowns, Diagramme usw. hinzugefügt.  
5. **Layout**  
   - **Buttons**: Fahrmodus 1–7, STOPP, Kalibrierung, sowie ein manueller Modus („M“).  
   - **Dropdowns**: Einstellen von max. Geschwindigkeit (`vmax_vorgabe`), Lenkwinkel (`maxwinkel_vorgabe`) und minimalem Abstand (`mindist_vorgabe`).  
   - **KPIs**: Anzeigen von Geschwindigkeit min/max/mean, Fahrzeit, Fahrstrecke, Fahrmodus.  
   - **Graphen**:  
     - Geschwindigkeit- vs. Zeit  
     - Lenkwinkel- vs. Zeit  
     - Ultraschall- vs. Zeit (wird ein-/ausgeblendet je nach Fahrmodus)  
     - IR-Status- vs. Zeit (wird ein-/ausgeblendet je nach Fahrmodus)  
     - Fahrstrecke- vs. Zeit  
6. **Callbacks**  
   - **Fahrmodus-Buttons (1–7)**  
     - Erster Callback: Setzt Button auf „FMx aktiv…“ (Spinner) und `color='warning'`.  
     - Zweiter Callback: Erkennt „warning“, ruft `car.fahrmodus(...)` auf, aktualisiert das `Data`-Objekt, schaltet Button zurück auf normal.  
   - **STOPP-Button**:  
     - Setzt `car.ismanually_stopped = True`, womit jeder laufende Modus abbricht.  
   - **Kalibrierung** (`btCali`):  
     - In mehreren Schritten (z. B. Klick 1: „Auf Hintergrund stellen“, Klick 2: Messen, Klick 3: Messen der Linie, …).  
     - Schreibt IR-Referenzwerte in `config.json`.  
   - **Manueller Modus** (`collapse-button`):  
     - Zeigt/versteckt den Bereich mit Buttons „Vor“, „Zurück“, „Links“, „Rechts“, „Stopp“.  
     - Jeder Button ruft z. B. `car.drive(...)` auf, um Vorwärts/Rückwärts zu bewegen, oder `car.frontwheels.turn(...)`, um zu lenken.  
   - **Dropdowns**:  
     - Sobald der Benutzer eine Auswahl ändert, wird das in `car.vmax_vorgabe`, `car.maxwinkel_vorgabe`, `car.mindist_vorgabe` übernommen und sofort in `config.json` geschrieben.  
   - **Diagramm-Callback**:  
     - `update_diagrams(selected_fahrt)`: Lädt die Daten für die gewählte `FahrtID`, erstellt Plotly-Figures für Geschwindigkeit, Distanz, Fahrstrecke, Lenkwinkel und IR-Status.  
     - Blendet je nach Fahrmodus z. B. den Ultraschall-Plot aus, wenn es kein relevanter Modus ist.

#### 1.6.3 Start
- **Dateiende**:  
  ```python
  if __name__ == "__main__":
      app.run_server(debug=True, host=ip_host, port=8053)
