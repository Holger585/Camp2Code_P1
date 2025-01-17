```mermaid
---
config:
  layout: dagre
---
flowchart TB
    A0(("Start Skript")) --> C2["Moduswahl 5,6,7"]
    C2 --> C3["Erzeuge ersten Logeintrag Zeit=0"]
    C3 --> C4["Manueller Tastenbruch über Terminal (ESC) initialisieren"]
    C4 --> C5["__Losfahren__ (Geschwindigkeit, Lenkwinkel)"]
    C5 --> C6{"while True"}
    C6 -- Zeitlimit 120s? --> C7["break"]
    C6 -- ESC gedrückt? --> C7
    C6 --> C8["IR lesen & Distanz messen"]
    C10["Anpassung Lenkwinkel und Geschwindigkeit."] -- "Mindesabstand unterschritten & Fahrmodus == 7" --> C7
    C8 -- "Linie erkannt auf allen IR-LED's" --> C9["Endlinie erkannt."]
    C8 -- "Links/Rechts-Lenken in 8 Stufen" --> C10
    C10 -- "Linie nicht erkannt und Fahrmodus >= 6" --> C11["Einleitung Korrekturfahrt"]
    C10 -- Linie erkannt --> C12["Fortfahren time.sleep(0.05)"]
    C11 --> D1["Logeintrag erzeugen"]
    C12 --> D1
    D1 --> C6
    C7 --> E1["finally: Fahrmodus fertig oder Abbruchbedingung erfüllt. Fahrzeug stoppt."]
    C9 --> C7
    E1 --> E2["Logeintrag erzeugen"]
    E2 --> F1["Log in CSV schreiben"]
    F1 --> Z(("Ende Skript"))
