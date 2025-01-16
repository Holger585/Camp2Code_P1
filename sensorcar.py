from soniccar import SonicCar
from basisklassen import Infrared
import sys
import select
import tty
import termios
import time
import json
import os
import csv

class SensorCar(SonicCar):
    """
    Erweiterte Fahrzeugklasse mit Infrarotsensoren für Linienverfolgung und Hinderniserkennung.
    """

    def __init__(self):
        """
        Initialisiert das Fahrzeug und die Infrarotsensoren.
        """
        super().__init__()
        self._moduswahl = 5  # Moduswahl für das Fahrzeug
        self._log = []  # Liste zum Speichern der Log-Daten
        self.infrared = Infrared()  # Initialisierung der Infrarotsensoren
        self._ir_value = [0,0,0,0,0]  # Array zum Speichern der Infrarotwerte
        try:
            with open("config.json", "r") as f:
                self.data = json.load(f)
                self.infrared._references = self.data.get("ir_init", 0)
        except FileNotFoundError as e:
            print(f"Fehler: config.json nicht gefunden. Standardwerte werden verwendet. {e}")
            self.infrared._references = [300,300,300,300,300]
        except Exception as e:
            print(e)

    @property
    def get_infrared(self):
        """
        Liest die aktuellen Werte der Infrarotsensoren.

        Returns:
            list: Status der IR-LEDs.
        """
        self._ir_value = self.infrared.read_digital()
        return self._ir_value

    @property
    def get_moduswahl(self):
        """
        Gibt den aktuellen Fahrmodus zurück.

        Returns:
            int: Aktueller Fahrmodus.
        """
        return self._moduswahl

    def save_reference(self, reference):
        """
        Speichert die Kalibrierwerte der Infrarotsensoren in der Konfigurationsdatei.

        Args:
            reference (list): Kalibrierwerte der Infrarotsensoren.
        """
        try:
            with open("config.json", "r") as f:
                self.data = json.load(f)
            with open("config.json", "w") as f:
                self.data["ir_init"] = list(reference)
                json.dump(self.data, f, indent=4)
        except FileNotFoundError as e:
            print(f"Fehler: config.json nicht gefunden. Standardwerte werden verwendet. {e}")
            self.data["ir_init"] = list(self.infrared._references)
        except Exception as e:
            print(e)
            self.data["ir_init"] = list(self.infrared._references)   

    def ir_cali(self):
        """
        Kalibriert die Infrarotsensoren und speichert die Kalibrierwerte.
        """
        self.infrared.cali_references() 
        self.save_reference(self.infrared._references)   
        print(self.infrared._references)

    def fahrmodus_5_6_7(self, speed=30, angle=90, modus=5, mindist=12):
        """
        Fahrmodus 5, 6 und 7: Linienverfolgung mit optionaler Hinderniserkennung.

        Args:
            speed (int): Geschwindigkeit des Fahrzeugs.
            angle (int): Lenkwinkel des Fahrzeugs.
            modus (int): Fahrmodus (5, 6 oder 7).
            mindist (int): Minimaler Abstand zu Hindernissen in cm.
        """
        ir_value = self.get_infrared
        self._moduswahl = modus
        cnt = 0
        speed_value = speed
        start_time = time.time()  
        self.loggen(0, speed_value, 0, angle, self.get_distance, ir_value, self._moduswahl)  
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        self.drive(speed_value, angle)
        time.sleep(0.2)   

        try:
            while True:
                # 1) Zeitlimit prüfen (120 Sekunden)
                if time.time() - start_time > 120:
                    print("Zeitlimit (120s) erreicht. Fahrmodus beenden.")
                    break

                # 2) ESC-Abfrage: ohne Blockieren
                if select.select([sys.stdin], [], [], 0)[0]:
                    key = sys.stdin.read(1)
                    if ord(key) == 27:  # ESC-Taste
                        print("Abbruch durch ESC-Taste.")
                        break

                ir_value = self.infrared.read_digital() 
                distance = self.get_distance
                # Fahrzeug stoppen                
                if ir_value == [1,1,1,1,1]:
                    self.stop()
                    self.frontwheels.turn(90)   
                    break          
                # Links lenken Stufe 4
                elif ir_value[0] and ir_value[1] == False:
                    angle = 55
                    speed_value = int(speed * 0.6)
                    self.drive(speed_value,angle)
                # Rechts lenken Stufe 4
                elif ir_value[3] == False and ir_value[4]:
                    angle = 125
                    speed_value = int(speed * 0.6)
                    self.drive(speed_value,angle) 
                # Links lenken Stufe 3
                elif ir_value[0] and ir_value[1]:
                    angle = 70
                    speed_value = int(speed * 0.7)
                    self.drive(speed_value,angle) 
                # Rechts lenken Stufe 3
                elif ir_value[3] and ir_value[4]:
                    angle = 110
                    speed_value = int(speed * 0.7)
                    self.drive(speed_value,angle)  
                # Links lenken Stufe 2
                elif ir_value[0] == False and ir_value[1]:
                    angle = 80
                    speed_value = int(speed * 0.85)
                    self.drive(speed_value,angle) 
                # Rechts lenken Stufe 2
                elif ir_value[3] and ir_value[4] == False:
                    angle = 100
                    speed_value = int(speed * 0.85)
                    self.drive(speed_value,angle) 
                # Links lenken Stufe 1
                elif ir_value[1] and ir_value[2]:
                    angle = 85
                    speed_value = speed
                    self.drive(speed_value,angle)
                # Rechts lenken Stufe 1
                elif ir_value[2] and ir_value[3]:
                    angle = 95
                    speed_value = speed
                    self.drive(speed_value,angle)
                # Geradeaus fahren
                elif ir_value[2]:
                    angle = 90
                    speed_value = speed
                    self.drive(speed_value,angle) 
                # Linie nicht erkannt
                elif ir_value == [0,0,0,0,0]:  
                    # Aktivierung in Fahrmodus 6 & 7
                    # Counter cnt zur Verzögerung der Korrekturfahrt
                    if modus >= 6 and cnt > int(speed/15):
                        angle = 180 - angle
                        speed_value = -speed_value
                        self.drive(speed_value,angle) 
                        cnt = 0  
                    else:
                        cnt = cnt + 1
                    time.sleep(0.05)
                if (0 < distance < mindist) and modus == 7:
                    self.stop()
                    print("Mindistanz unterschritten, Fahrzeug stoppt")
                    break
                self.loggen(time.time() - start_time, speed_value, self._direction, angle, self.get_distance, ir_value, self._moduswahl)                                                              
                
        finally:
            # Terminal-Einstellungen wiederherstellen und Auto stoppen
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            self.stop()
            print("Fahrmodus beendet.")

    def fahrmodus(self, fmodus=1, speed=50, angle=90, mindist=12):
        """
        Wählt den Fahrmodus basierend auf der Eingabe aus und startet ihn.

        Args:
            fmodus (int): Fahrmodus (1 bis 7).
            speed (int): Geschwindigkeit des Fahrzeugs.
            angle (int): Lenkwinkel des Fahrzeugs.
            mindist (int): Minimaler Abstand zu Hindernissen in cm.
        """
        if fmodus == 1:
            self.fahrmodus_1(speed)
        elif fmodus == 2:
            self.fahrmodus_2(speed)
        elif fmodus == 3:
            self.fahrmodus_3(mindist, speed, angle)
        elif fmodus == 4:
            self.fahrmodus_4(speed=speed)
        elif fmodus >= 5:
            self.fahrmodus_5_6_7(speed, angle, fmodus, mindist)

        # Schreiben der Log-Daten in eine CSV-Datei
        file_name = f"fahrmodus_log.csv"
        file_exists = os.path.isfile(file_name)  # Prüfen, ob die Datei existiert

        with open(file_name, mode="a", newline="") as csv_file:
            fieldnames = ["Zeit", "Geschwindigkeit", "Fahrtrichtung", "Lenkwinkel", "Abstand", "IR_Status", "Fahrmodus"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Schreibe die Kopfzeile, falls die Datei neu erstellt wurde
            if not file_exists:
                writer.writeheader()

            writer.writerows(self._log)  # Log-Daten in die Datei schreiben

        print(f"Log-Daten wurden in '{file_name}' gespeichert.") 

if __name__ == "__main__":
    car = SensorCar()
    car.frontwheels.turn(90)
    car.fahrmodus(7)

