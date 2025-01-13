from basecar import BaseCar
from soniccar import SonicCar
from basisklassen import Ultrasonic, Infrared
import time
import random
import csv
import os

class SensorCar():
    def __init__(self):
        """
        Initialisiert das Fahrzeug und den Ultraschallsensor.
        """
        super().__init__()
