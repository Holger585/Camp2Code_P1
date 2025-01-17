```mermaid
---
config:
  layout: dagre
  theme: forest
  look: handDrawn
---
flowchart TB
    A0(("Start Methode Fahrmodus_5_6_7")) --> C2["Moduswahl 5,6,7"]
    C2 --> C3["Erzeuge ersten Logeintrag Zeit=0"]
    C3 --> C4["Manueller Tastenbruch über Terminal (ESC) initialisieren"]
    C4 --> C5["__Losfahren__ (Geschwindigkeit, Lenkwinkel)"]
    C5 --> C6{"while True"}
    C6 -- Zeitlimit 120s? --> C7["break"]
    C6 -- ESC gedrückt? --> C7
    C6 --> C8["IR lesen & Distanz messen"]
    C10["Anpassung Lenkwinkel und Geschwindigkeit."] -- "Fahrmodus==5 & Linie nicht erkannt" --> C7
    C8 -- "Linie erkannt auf allen IR-LED's" --> C9["Endlinie erkannt."]
    C8 -- "Links/Rechts-Lenken in 8 Stufen" --> C10
    C10 -- "Fahrmodus==7 & Mindesabstand unterschritten" --> C7
    C10 -- "Fahrmodus>=6 & Linie nicht erkannt" --> C11["Einleitung Korrekturfahrt"]
    C10 -- Fahrmodus 5,6,7 & Linie erkannt --> D1
    C11 --> D1["Logeintrag erzeugen"]
    D1 --> C6
    C7 --> E1["finally: Fahrmodus fertig oder Abbruchbedingung erfüllt. Fahrzeug stoppt."]
    C9 --> C7
    E1 --> E2["Logeintrag erzeugen"]
    E2 --> F1["Log in CSV schreiben"]
    F1 --> Z(("Ende Skript"))
