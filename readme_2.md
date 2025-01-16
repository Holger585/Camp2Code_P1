# Projektdokumentation für das autonome RPiCar mit Sensorik und Dash-GUI

Dieses Dokument ist das Ergebnis der zwewöchigen Projektphase „Camp2Code“, in der ein Modellfahrzeug auf Basis eines Raspberry Pi entwickelt wurde. Ziel war es, verschiedene Fahrmodi (Vor-/Rückwärtsfahrt, Hinderniserkennung, Linienverfolgung) zu realisieren und die anfallenden Daten in einer Dash-App zu visualisieren. Die folgenden Kapitel orientieren sich an den im Projekt zur Verfügung gestellten **Anforderungen** und beschreiben den Projektablauf, die Softwarestruktur und die Umsetzung einschließlich einer Beispiel-Präsentationsstruktur.

---

## 1. Überblick Projektziel

Zentrales Ziel war die Implementierung einer Software, die ein Modellauto selbstständig und manuell steuern kann. Dafür:

- **Modellauto**: Chassis mit Vorderradlenkung (Servo) und Hinterradantrieb (DC-Motoren).  
- **Sensorik**:  
  - *Ultraschallsensor* (Hinderniserkennung)  
  - *Infrarotsensorleiste* (Linienverfolgung)  
- **Zentrale Steuereinheit**: Raspberry Pi (Raspberry-Pi-OS), Programmiersprache Python.  
- **Bereitgestellte Basisklassen**:  
  - `BackWheels`, `FrontWheels`, `Ultrasonic`, `Infrared` (in `basisklassen.py`)  
- **Verwendete Prinzipien**:  
  - Objektorientierte Programmierung (OOP)  
  - Agile Arbeitsweise in einem 2-Wochen-Sprint (Planung, Teilaufgaben, tägliche Abstimmung)  
  - Versionierung via Git  

Zwei Hauptziele wurden dabei unterschieden:

1. **Woche 1**: Ansteuerung und Auslesen der Komponenten, einfache Fahrmodi (Vorwärts, Rückwärts, Kurvenfahrt).  
2. **Woche 2**: Linienverfolgung, Aufzeichnung und Visualisierung von Fahrdaten.

---

## 2. Projektorganisation

### 2.1 Arbeitsweise

Unser Team (fünf Personen) hat an der Software in einem **agilen Ansatz** gearbeitet. Wir haben:

- **Daily Scrums** (kurzer täglicher Austausch) durchgeführt.  
- **User Stories** bzw. Teilaufgaben definiert (z. B. „Fahrmodus 3 umsetzen“, „IR-Kalibrierung implementieren“).  
- **Rollenverteilung** (Product Owner, Scrum Master) nur rudimentär betrieben; alle blieben im Entwicklerteam aktiv.  

### 2.2 Technische Voraussetzungen und Materialien

- Raspberry Pi (OS installiert, GPIO-I2C konfiguriert)  
- Basisklassen-Datei `basisklassen.py` (enthält: `BackWheels`, `FrontWheels`, `Ultrasonic`, `Infrared` usw.)  
- Chassis inkl. Motoren, Motorentreiber, PCA9685, TB6612  
- **Wichtige Schritte**:
  1. Raspberry Pi einrichten (Betriebssystem, Konfiguration)  
  2. Download der Basisklassen und ersten Funktionstest  
  3. Einrichtung einer Entwicklungsumgebung (IDE, Remoteverbindung, etc.)  
  4. Test, ob das Modellauto grundsätzlich funktionsfähig ist (GPIO, I2C)  

### 2.3 Projektplanung

- **Zeitplan**:  
  - Woche 1: Basisklassen prüfen und kleine Fahrmodi programmieren (Fahrmodus 1 & 2).  
  - Woche 2: Linienverfolgung (Fahrmodus 5–7), Datenaufzeichnung, Dash-GUI.  
- **Aufgabenverteilung**:  
  - Entwickler*innen für Ultraschall, IR, Python-Klassen.  
  - GUI-Entwicklung in Dash.  
  - Dokumentation (Readme, Code-Doku, Präsentation).  
- **Quellcodeverwaltung**:  
  - Git-Repository (lokal und remote).  
  - Branch-Strategie: `main` + Featurebranches.  
- **Dokumentation**:  
  - Laufende Erstellung von Docstrings für alle Klassen und Methoden.  
  - Ergebnisdokumentation in Markdown (README) und kurze Anwenderdoku.  
  - Finalpräsentation mit PowerPoint.

---

## 3. Anforderungsbeschreibung

Der Anforderungskatalog benennt folgende **Kernklassen** und **Ziele**:

### 3.1 Klassen

1. **Verwendung der Basisklassen**  
   - `BackWheels`, `FrontWheels`, `Ultrasonic`, `Infrared` werden aus `basisklassen.py` übernommen.  
   - *Wichtig*: Konstruktor-Argumente und vorhandene Methoden verstehen und für unser Projekt anpassen.  

2. **Modularisierung**  
   - Die Software wurde so strukturiert, dass Kernfunktionen in eigenen Modulen abgelegt sind (`basecar.py`, `soniccar.py`, `sensorcar.py`) und eine zentrale GUI-Anwendung (`app_gui.py`) darauf zugreift.

3. **Klasse `BaseCar`**  
   - **Properties**:  
     - `steering_angle`: Regelt den Lenkwinkel (45–135°, 90° = geradeaus). Werte außerhalb dieses Bereichs werden „geclamped“.  
     - `speed`: Integer von -100 bis 100.  
       - Negative Werte = Rückwärtsfahrt  
       - 0 = Stillstand  
       - Positive Werte = Vorwärtsfahrt  
     - `direction`: read-only Property, gibt 1 (vorwärts), -1 (rückwärts) oder 0 (still) zurück.  
   - **Methoden**:  
     - `drive(speed=None, steering_angle=None)`: Setzt neue Geschwindigkeit und/oder Lenkwinkel. Bleibt unverändert, wenn ein Parameter `None` ist.  
     - `stop()`: Geschwindigkeit = 0 (Stillstand).  
   - **Fahrmodi** (Tests der Klasse `BaseCar`):  
     - *Fahrmodus 1*: 3 Sekunden vorwärts, 1 Sekunde Stop, 3 Sekunden rückwärts.  
     - *Fahrmodus 2*: Kreisfahrt mit maximalem Lenkwinkel (z. B. 8 Sekunden linksherum) und Rückkehr an den Start. Anschließend dasselbe in die andere Richtung.

4. **Klasse `SonicCar`**  
   - Erbt von `BaseCar` und bietet zusätzlich:  
     - `get_distance()`: Liest den Ultraschallwert.  
     - Fahrmodus 3: Vorwärtsfahrt bis Hindernis (`distance < mindist`), dann Stopp.  
     - Fahrmodus 4: Erkundungstour mit zufälligen oder frei definierten Lenkbewegungen; Hindernisse lösen eine Richtungsänderung aus.  
   - **Aufzeichnung von Fahrdaten** (Geschwindigkeit, Lenkwinkel, Ultraschallabstand etc.). Diese Daten werden später z. B. in `.csv` geschrieben oder direkt an die Dash-App übergeben.

5. **Dash-Visualisierung**  
   - „**Stufe 1**“: Anzeige von Key Performance Indicators (KPIs) wie min./max./durchschnittliche Geschwindigkeit, Gesamtfahrzeit, Gesamtstrecke.  
   - „**Stufe 2**“: Grafische Darstellung über die Zeit (z. B. Linien-Plot für Geschwindigkeit vs. Zeit, Abstand vs. Zeit).  
   - „**Stufe 3**“: Interaktives Dropdown-Menü (z. B. Auswahl verschiedener Fahrten oder Fahrdaten).  

6. **Klasse `SensorCar`**  
   - Erbt ebenfalls von `BaseCar`, kombiniert Ultraschallsensor und Infrarotsensor.  
   - **Linienverfolgung**:  
     - *Fahrmodus 5*: Folgen einer (breiteren) Linie mit großen Kurvenradien. Stop bei Linienende.  
     - *Fahrmodus 6*: Engere Kurven bis hin zu geschlossenen Rundkursen, wiederholte Runden.  
     - *Fahrmodus 7*: Linienverfolgung mit zusätzlicher Ultraschall-Hindernisserkennung; Fahrzeug stoppt, sobald Hindernis im Weg.  
   - Auch IR-Werte werden geloggt.

### 3.2 Nutzerinterface

- **Menüführung (Terminal)** oder *Erweiterung der Dash-App* ermöglicht die Auswahl jedes Fahrmodus.  
- Der Anwender kann z. B. im Terminal oder in der Browser-GUI anklicken, ob Fahrmodus 1, 2, 3 usw. gestartet werden soll.  
- Eine **kurze Anwendungsdokumentation** beschreibt die Bedienung (s. Kapitel 9 „Kurze Anwenderdoku“).

### 3.3 Dokumentation

- Mindestanforderung: Docstrings für Klassen und Methoden, damit Implementierung, Schnittstellen und Nutzung deutlich sind.  
- Zusätzlich: README-Dokumentation (diese Datei), Abschlussshow (PowerPoint).

### 3.4 Präsentation der Software

- Das fertige Produkt (Modellauto + Software) wird abschließend vorgeführt.  
- **Zwei Teile** in der Präsentation:  
  1. Demonstration für Anwender (Wie startet man Fahrmodi? Wie sieht die Dash-GUI aus?)  
  2. Technische Erklärung (Aufbau der Klassen, Module, Code-Struktur).

---

## 4. Struktur und Ablauf im Projekt

1. **Anforderungsanalyse**: Lesen der Vorgaben und Bestimmung, wie wir IR/Ultraschall ansteuern.  
2. **Konzept**: Aufteilung in `basecar.py` (Grundfunktionen), `soniccar.py` (Ultraschallintegration), `sensorcar.py` (IR + Ultraschall).  
3. **Implementierung**:  
   - Code in kleinen Einheiten (User Stories)  
   - Frequentes Testing (z. B. Lenkung, Sensorwerte im Terminal prüfen)  
   - Fahrmodi programmieren und verknüpfen  
4. **Test**:  
   - Einzelsensor (Ultraschall, IR)  
   - Vollständige Fahrmodi  
   - Datenerfassung in `fahrmodus_log.csv`  
   - Dash-Visualisierung  
5. **Abschluss**:  
   - Dokumentation (Readme, Codekommentare)  
   - Präsentation (PowerPoint-Folien, Live-Demo)

---

## 5. Implementierte Fahrmodi

Gemäß den Anforderungen existieren folgende Fahrmodi (klassifiziert nach *BaseCar*, *SonicCar*, *SensorCar*):

1. **Fahrmodus 1**  
   - Vorwärts (3 s), Stopp (1 s), Rückwärts (3 s).  
2. **Fahrmodus 2**  
   - Kreisfahrt mit maximalem Lenkwinkel (bspw. 8 s) → Stop → Rückwärtsfahrt.  
3. **Fahrmodus 3** (*SonicCar*)  
   - Vorwärts bis ein Hindernis < `mindist` erkannt wird → Stopp.  
4. **Fahrmodus 4** (*SonicCar*)  
   - „Erkundungstour“: Zufällige/variierende Fahrtrichtung, Hindernisse lösen Umkehrmanöver aus.  
5. **Fahrmodus 5** (*SensorCar*)  
   - Linienverfolgung (große Kurven, einfacher Parcours).  
6. **Fahrmodus 6** (*SensorCar*)  
   - Komplexere oder engere Linienverfolgung, ggf. geschlossene Rundkurse.  
7. **Fahrmodus 7** (*SensorCar*)  
   - Linienverfolgung + Hinderniserkennung (Ultraschall) → Stopp bei Hindernis.

Während der Fahrten wird protokolliert (z. B. Zeit, Speed, Steering, Abstand, IR-Status, Fahrmodus), um die Ergebnisse auszuwerten.

---

## 6. Test und Validierung

- **Sensortests**: Manuelle Messwert-Abfragen über Konsolenausgaben.  
- **Basisklassen-Test**: Durch Aufrufe von `FrontWheels()`, `BackWheels()`, `Ultrasonic()`, `Infrared()`.  
- **Fahrmodi-Test**:  
  1. Fahrmodus 1 & 2 auf freier Bahn.  
  2. Fahrmodus 3 & 4 (Hindernisse aufstellen).  
  3. Fahrmodus 5–7 (Linienbahnen aus Klebeband oder Papier drucken und auslegen).  
- **Aufzeichnung**: `fahrmodus_log.csv` sammelt Daten für die GUI.  
- **GUI-Test**: Dash-App auf Port 805x starten und Diagramme prüfen (Geschwindigkeit, Distanz, Fahrstrecke).

---

## 7. GUI und Datenauswertung (Dash)

In `app_gui.py` wird eine Dash-App verwendet, um die gesammelten Daten anzuzeigen und Fahrmodi zu starten:

1. **KPIs**:  
   - max. Geschwindigkeit, min. Geschwindigkeit, Durchschnittswerte  
   - Fahrzeit, gefahrene Strecke  
2. **Graphen** (Plotly):  
   - Geschwindigkeit vs. Zeit, Abstand vs. Zeit  
   - Dropdown zur Auswahl der Fahrt-ID oder zum Filtern von Fahrdaten  
3. **Zusätzliche Buttons**:  
   - Start Fahrmodus 1–7, Stopp, Kalibrierung IR-Sensor etc.

---

## 8. Fazit und Ausblick

- **Fazit**:  
  - Die grundlegenden Anforderungen (Vor-/Rückwärtsfahrt, Hinderniserkennung, Linienverfolgung) sind erfüllt.  
  - Die Software ist modular und dokumentiert; mit `SensorCar` können alle Sensorfunktionen genutzt werden.  
  - Eine Dash-App zeigt die Daten in Echtzeit oder nach Abschluss an.  

- **Erweiterungen**:  
  - **Kamerasensorik** (OpenCV) zur fortgeschrittenen Objekterkennung  
  - **Industrielle Anforderungen** wie flexible Wegplanung  
  - **Weitere Fahrmodi** (z. B. Ausweichmanöver, Slalom)  

---

## 9. Kurze Anwenderdokumentation

1. **Hardware anschließen**  
   - Raspberry Pi mit allen Sensoren/Motoren gemäß Schaltplan verbinden.  
   - `config.json` anpassen (Lenkungs-Offsets, IR-Referenzwerte etc.).  

2. **Software starten**  
   - In der Konsole: `python3 app_gui.py` (bzw. `python3 sensorcar.py`)  
   - Browser öffnen (IP/Port wie in `config.json` angegeben, z. B. `http://0.0.0.0:8050`).  

3. **Fahrmodus auswählen**  
   - Im Terminal oder in der Dash-GUI: z. B. `Fahrmodus 5` für einfache Linienverfolgung.  
   - Mit ESC (im Terminal) oder „STOPP“-Button (in der GUI) kann jederzeit abgebrochen werden.  

4. **Kalibrierung IR-Sensor**  
   - Fahrzeug erst auf Hintergrund stellen → Klick „Kalibrierung“ → dann auf Linie stellen → „Kalibrierung“  
   - Neue Referenzwerte werden gespeichert und genutzt.  

5. **Datenanzeige**  
   - In der GUI: Diagramme für Geschwindigkeit und Distanz, plus Kennwerte (v. a. min./max./mean Speed, Fahrzeit, Strecke).  
   - Im CSV-Log: Zeitstempel, Fahrmodus, Sensorwerte.

---


## 10. Code und Dokumentation

- **Code**:  
  - `basisklassen.py` (vorgegeben)  
  - `basecar.py`, `soniccar.py`, `sensorcar.py` (Erweiterungen gemäß Anforderung)  
  - `app_data.py` (Datenanalyse und KPI-Berechnung)  
  - `app_gui.py` (Dash-Applikation)  
- **Dokumentation**:  
  - Docstrings in den Klassen und Methoden, README in Markdown (dieses Dokument).  
  - Präsentationsfolien als PowerPoint-Datei zur Demo.

---

**Vielen Dank für das Interesse an unserem Projekt**  
Bei weiteren Fragen oder Feedback steht unser Team gerne zur Verfügung.
