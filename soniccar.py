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
        """
        Setzt die Geschwindigkeit und den Lenkwinkel und überprüft den Abstand zu Hindernissen.

        Args:
            speed (int): Geschwindigkeit des Fahrzeugs.
            steering_angle (int): Lenkwinkel des Fahrzeugs.
            min_dist (int): Minimaler Abstand zu Hindernissen in cm.
            f_modus (int): Fahrmodus.
        """
        # Setze die Geschwindigkeit und den Lenkwinkel des Fahrzeugs
        self.drive(speed=speed, steering_angle=steering_angle)
        # Logge den aktuellen Zustand des Fahrzeugs
        self.loggen(time.time() - self.start_time, self._speed, self._direction, self._steering_angle, self.get_distance, [0,0,0,0,0], f_modus)
        
        # Schleife um ein Unterbrechen während der Fahrt durch Tastendruck zu ermöglichen
        while not self.ismanually_stopped:
            distance = self.get_distance
            # Fahrzeug stoppen, wenn der Abstand zu einem Hindernis kleiner als min_dist ist
            if 0 < distance < min_dist:
                self.stop()
                break
        
        if self.ismanually_stopped:
            # Fahrzeug stoppen, wenn manuell gestoppt
            self.stop()
        
        # Logge den aktuellen Zustand des Fahrzeugs
        self.loggen(time.time() - self.start_time, self._speed, self._direction, self._steering_angle, self.get_distance, [0,0,0,0,0], f_modus)

    def fahrmodus_3(self, min_dist=12, speed=50, angle=90):
        """
        Fahrmodus 3: Fährt mit einer bestimmten Geschwindigkeit und Lenkwinkel, bis ein Hindernis erkannt wird.

        Args:
            min_dist (int): Minimaler Abstand zu Hindernissen in cm.
            speed (int): Geschwindigkeit des Fahrzeugs.
            angle (int): Lenkwinkel des Fahrzeugs.
        """
        # Setzen der Startzeit
        self.start_time = time.time() 
        # Erster Eintrag im Log auf Null setzen
        self.loggen(0.0, 0, 0, 90, 0, [0,0,0,0,0], 3)
        # Fahrzeug fahren lassen
        self.set_fahren(speed=speed, steering_angle=angle, min_dist=min_dist, f_modus=3)

    def fahrmodus_4(self, min_dist=12, speed=50, angle=135):
        """
        Fahrmodus 4: Fährt für 30 Sekunden mit zufälligem Lenkwinkel und überprüft den Abstand zu Hindernissen.

        Args:
            min_dist (int): Minimaler Abstand zu Hindernissen in cm.
            speed (int): Geschwindigkeit des Fahrzeugs.
            angle (int): Lenkwinkel des Fahrzeugs.
        """
        # Setzen der Startzeit
        self.start_time = time.time() 
        # Erster Eintrag im Log auf Null setzen
        self.loggen(0.0, 0, 0, 90, 0, [0,0,0,0,0], 4)
        
        # Schleife endet nach 30 Sekunden
        while time.time() - self.start_time < 30:
            self.set_fahren(speed=speed, steering_angle=random.randint(45, 135), min_dist=min_dist, f_modus=4)
            self.drive(speed=-speed, steering_angle=angle)
            self.loggen(time.time() - self.start_time, self._speed, self._direction, self._steering_angle, self.get_distance, [0,0,0,0,0], f_modus=4)
            time.sleep(2)
            self.stop()
            self.frontwheels.turn(90)
            self.loggen(time.time() - self.start_time, self._speed, self._direction, self._steering_angle, self.get_distance, [0,0,0,0,0], f_modus=4)

if __name__ == "__main__":
    car = SonicCar()
    log = []  # Liste zum Speichern der Log-Daten
    start_time = time.time()  # Startzeitpunkt speichern

    car.fahrmodus_1()  # Fahrmodus 1 starten

