from basecar import BaseCar
from basisklassen import Ultrasonic
import time
import random

class SonicCar(BaseCar):
    """
    Erweiterte Fahrzeugklasse mit Ultraschallsensor für Hinderniserkennung
    und Fahrmodi mit Log-Funktionalität.
    """

    def __init__(self):
        """
        Initialisiert das Fahrzeug und den Ultraschallsensor.
        """
        super().__init__()
        self.ultrasonic = Ultrasonic()
        self._distance = 0

    @property
    def get_distance(self):
        """
        Liest die aktuelle Entfernung vom Ultraschallsensor.

        Returns:
            int: Gemessene Entfernung in Zentimetern.
        """
        self._distance = self.ultrasonic.distance()
        return self._distance
    
    def set_fahren(self, speed: int, steering_angle: int, min_dist: int, f_modus: int):
        # Schleife um ein unterbrechen durch Tastendruck zu ermöglichen
        #while not self.ismanually_stopped:
        self.drive(speed=speed, steering_angle=steering_angle)
        self.loggen(time.time() - self.start_time, self._speed, self._direction, self._steering_angle, self.get_distance, [0,0,0,0,0], f_modus)
        while not self.ismanually_stopped:
            distance = self.get_distance
            if 0 < distance < min_dist:
                self.stop()
                break
        if self.ismanually_stopped:
            self.stop()
        self.loggen(time.time() - self.start_time, self._speed, self._direction, self._steering_angle, self.get_distance, [0,0,0,0,0], f_modus)

    def fahrmodus_3(self, min_dist=12, speed=50, angle=90):

        self.start_time = time.time() 
        self.loggen(0.0, 0, 0, 90, 0, [0,0,0,0,0], 3)
        self.set_fahren(speed=speed, steering_angle=angle, min_dist=min_dist, f_modus=3)

    def fahrmodus_4(self, min_dist=12, speed=50, angle=135):

        self.start_time = time.time() 
        self.loggen(0.0, 0, 0, 90, 0, [0,0,0,0,0], 4)
        while time.time() - self.start_time < 30:  # Schleife endet nach 30 Sekunden
            self.set_fahren(speed=speed, steering_angle=random.randint(45, 135), min_dist=min_dist, f_modus=4)
            self.drive(speed=-speed,steering_angle=angle)
            self.loggen(time.time() - self.start_time, self._speed, self._direction, self._steering_angle, self.get_distance, [0,0,0,0,0], f_modus=4)
            time.sleep(2)
            self.stop()
            self.frontwheels.turn(90)
            self.loggen(time.time() - self.start_time, self._speed, self._direction, self._steering_angle, self.get_distance, [0,0,0,0,0], f_modus=4)

if __name__ == "__main__":
    car = SonicCar()
    log = []  # Liste zum Speichern der Log-Daten
    start_time = time.time()  # Startzeitpunkt speichern

    car.fahrmodus_1()  # Fahrmodus 4 starten

