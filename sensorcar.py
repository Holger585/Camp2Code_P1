from soniccar import SonicCar
from basisklassen import Infrared
import json
import time
import random
import csv
import os

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

    def fahrmodus_5(self):
        input('Bitte das Fahrzeug auf die Linie stellen.')
        while True:
            
            input('Fahrzeug steht nicht auf der Linie. Bitte positionieren.')
            






if __name__ == "__main__":
    car = SensorCar()
    car.frontwheels.turn(90)
    # print(car._ir_init)
    # print(car.get_infrared)
    # car.ir_cali()
    print(car.infrared._references)
    print(car.infrared.read_digital())
    input('Bitte das Fahrzeug auf die Linie stellen.')

