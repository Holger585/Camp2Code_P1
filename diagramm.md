flowchart TB
    A0((Start Skript)) --> A1[/__main__:/ <br/> car = SensorCar() <br/> car.frontwheels.turn(90) <br/> car.fahrmodus(7)/]

    %% Fahrmodus() dispatch
    A1 --> B1{fahrmodus(fmodus=7)?}
    B1 -->|fmodus==7| C0[fahrmodus_5_6_7(speed, angle, modus, mindist)]

    %% fahrmodus_5_6_7
    C0 --> C1[IR-Werte lesen: <br/> ir_value = self.get_infrared]
    C1 --> C2[moduswahl = modus]
    C2 --> C3[Starte Log: <br/> self.loggen(...)]
    C3 --> C4[Terminaleinstellungen (tty.setcbreak)]
    C4 --> C5[drive(speed_value, angle)]
    C5 --> C6{Schleife while True}

    %% Schleife
    C6 -->|Zeitlimit 120s?| C7[Abbruch (break)]
    C6 -->|ESC gedrückt?| C7[Abbruch (break)]
    C6 -->|Sonst| C8[IR lesen & Distanz messen]

    C8 -->|IR=[1,1,1,1,1]| C9[stop(), turn(90), break]
    C8 -->|Links/Rechts-Stufen| C10[Anpassung von angle und speed_value <br/> drive(...)]

    C10 -->|Linie nicht erkannt & modus>=6 <br/> +counter check| C11[Wende: angle=180-angle, <br/> speed_value=-speed_value]
    C10 -->|Linie erkannt| C12[Fortfahren <br/> time.sleep(0.05)]
    C10 -->|distance < mindist & modus==7| C13[stop(), break]

    %% Logging in Schleife
    C11 --> D1[selbst.loggen(...)]
    C12 --> D1
    C13 --> D1

    D1 --> C6

    %% Schleifenende
    C7 --> E1[finally-Block: <br/> Terminal-Einstellungen wiederherstellen <br/> stop() <br/> "Fahrmodus beendet"]

    %% Speicherung Log
    E1 --> F1[Log in CSV speichern <br/> (writerows in fahrmodus_log.csv)]
    F1 --> Z((Ende Skript))
