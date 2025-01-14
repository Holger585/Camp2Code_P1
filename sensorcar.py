from soniccar import SonicCar
from basisklassen import Infrared
import sys
import select
import tty
import termios
import time
import json

class SensorCar(SonicCar):
    def __init__(self):
        """
        Initialisiert das Fahrzeug .
        """
        super().__init__()
        self.infrared = Infrared()
        self._ir_value = 0
        try:
            with open("config.json", "r") as f:
                self.data = json.load(f)
                # self._ir_init = self.data.get("ir_init", 0)
                self.infrared._references = self.data.get("ir_init", 0)

        except FileNotFoundError as e:
            print(f"Fehler: config.json nicht gefunden. Standardwerte werden verwendet. {e}")
            self.infrared._references = [300,300,300,300,300]
            # self.ir_cali()   
        except Exception as e:
            print(e)

    @property
    def get_infrared(self):
        self._ir_value = self.infrared.read_analog()
        return self._ir_value

    def ir_cali(self):
        self.infrared.cali_references()    
        try:
            #config.json öffnen
            with open("config.json", "r") as f:
                self.data = json.load(f)

            #config.json mit neuem Datensatz schreiben
            with open("config.json", "w") as f:
                self.data["ir_init"] = list(self.infrared._references)
                json.dump(self.data, f, indent=4)

        except FileNotFoundError as e:
            print("Fehler: config.json nicht gefunden. Standardwerte werden verwendet. {e}")
            self.data["ir_init"] = list(self.infrared._references)
        except Exception as e:
            print(e)
            self.data["ir_init"] = list(self.infrared._references)

        print(self.infrared._references)


    def fahrmodus_5(self, speed = 30, angle = 90):

        input('Bitte das Fahrzeug auf die Linie stellen.')
        while True:
            if self.infrared.read_digital != [0,0,1,0,0]:
                print(self.infrared.read_digital)
                input('Fahrzeug steht nicht auf der Linie. Bitte mittig positionieren.')
            else:
                print('Linie erkannt. Fahrmodus 5 wird gestartet.')
                break

        start_time = time.time()
        
        # Terminal-Einstellungen für ESC-Abbruch vorbereiten
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        self.drive(speed, angle)        
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

                ir_value = self.infrared.read_digital 
                # Geradeaus fahren
                if ir_value == [0,0,1,0,0] | [0,1,1,1,0]:
                    self.frontwheels.turn(90)
                # Rechts lenken Stufe 1
                elif ir_value[2] == 1 & ir_value[3] == 1:
                    self.frontwheels.turn(95)
                # Rechts lenken Stufe 2
                elif ir_value[3] == 1:
                    self.frontwheels.turn(100)                    
                # Rechts lenken Stufe 3
                elif ir_value[3] == 1 & ir_value[4] == 1:
                    self.frontwheels.turn(110)  
                # Rechts lenken Stufe 4
                elif ir_value[4] == 1:
                    self.frontwheels.turn(125) 
                # Links lenken Stufe 1
                elif ir_value[2] == 1 & ir_value[3] == 1:
                    self.frontwheels.turn(85)
                # Links lenken Stufe 2
                elif ir_value[3] == 1:
                    self.frontwheels.turn(80)                    
                # Links lenken Stufe 3
                elif ir_value[3] == 1 & ir_value[4] == 1:
                    self.frontwheels.turn(70)  
                # Links lenken Stufe 4
                elif ir_value[4] == 1:
                    self.frontwheels.turn(55)                                           
                time.sleep(0.5)

                
        finally:
            # Terminal-Einstellungen wiederherstellen und Auto stoppen
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            self.stop()
            print("Fahrmodus beendet.")
            






if __name__ == "__main__":
    car = SensorCar()
    car.frontwheels.turn(90)
    # print(car._ir_init)
    # print(car.get_infrared)
    # car.ir_cali()
    print(car.infrared._references)
    print(car.infrared.read_digital())
