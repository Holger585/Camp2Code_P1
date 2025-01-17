```mermaid
flowchart TB
    A0((Start Skript))

    A0 --> C1["IR-Werte lesen:\nir_value = self.get_infrared"]
    C1 --> C2["moduswahl = modus"]
    C2 --> C3["Starte Log:\nself.loggen(...)"]
    C3 --> C4["Terminaleinstellungen\n(tty.setcbreak)"]
    C4 --> C5["drive(speed_value, angle)"]
    C5 --> C6{"while True"}

    %% Schleifenabbruch-Kriterien
    C6 -->|Zeitlimit 120s?| C7["break"]
    C6 -->|ESC gedrückt?| C7["break"]
    C6 -->|ansonsten| C8["IR lesen & Distanz messen"]

    %% IR-Auswertung
    C8 -->|"IR==[1,1,1,1,1]"| C9["stop()\nfrontwheels.turn(90)\nbreak"]
    C8 -->|"Links/Rechts-Stufen"| C10["Anpassung angle/speed\n drive(...)"]

    %% Sonderfälle in C10
    C10 -->|"Linie nicht erkannt\n(modus>=6)\n+counter\nIR==[0,0,0,0,0]"| C11["Wende:\nangle = 180 - angle\nspeed_value = -speed_value"]
    C10 -->|"Linie erkannt"| C12["Fortfahren\ntime.sleep(0.05)"]
    C10 -->|"distance < mindist\n(modus == 7)"| C13["stop()\nbreak"]

    %% Nach jedem Fahrbefehl wird geloggt
    C11 --> D1["self.loggen(...)"]
    C12 --> D1
    C13 --> D1
    D1 --> C6

    %% finally-Block
    C7 --> E1["finally:\nTerminal-Einstellungen\nwiederherstellen\nstop()\n\"Fahrmodus beendet\""]

    %% Logs in CSV
    E1 --> F1["Log in CSV: writerows(...)"]
    F1 --> Z((Ende Skript))
