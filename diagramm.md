```mermaid
flowchart TB
    A0((Start Skript))

    A0 --> C1["IR-Werte lesen"]
    C1 --> C2["Moduswahl 5,6,7"]
    C2 --> C3["Starte Log"]
    C3 --> C4["Manueller Abbruch (ESC) initialisieren"]
    C4 --> C5["Losfahren (Geschwindigkeit, Lenkwinkel)"]
    C5 --> C6{"while True"}

    %% Schleifenabbruch-Kriterien
    C6 -->|Zeitlimit 120s?| C7["break"]
    C6 -->|ESC gedrückt?| C7["break"]
    C6 -->|ansonsten| C8["IR lesen & Distanz messen"]

    %% IR-Auswertung
    C8 -->|"Linie erkannt auf allen IR-LED's"| C9["Endlinie erkannt. Fahrzeug stoppt."]
    C8 -->|"Links/Rechts-Lenken in 8 Stufen"| C10["Anpassung Lenkwinkel und Geschwindigkeit."]

    %% Sonderfälle in C10
    C10 -->|"Linie nicht erkannt und Fahrmodus >= 6"| C11["Einleitung Korrekturfahrt"]
    C10 -->|"Linie erkannt"| C12["Fortfahren time.sleep(0.05)"]
    C10 -->|"Mindesabstand unterschritten & Fahrmodus == 7"| C13["Fahrzeug stoppt"]

    %% Nach jedem Fahrbefehl wird geloggt
    C11 --> D1["Logeintrag erzeugen"]
    C12 --> D1
    C13 --> D1
    D1 --> C6

    %% finally-Block
    C7 --> E1["finally: Fahrmodus fertig oder Abbruchbedingung erfüllt. Fahrzeug stoppt."]

    %% Logs in CSV
    E1 --> F1["Log in CSV schreiben"]
    F1 --> Z((Ende Skript))
