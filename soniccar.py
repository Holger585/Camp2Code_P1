from basecar import BaseCar
from basisklassen import Ultrasonic
import time
import random
import csv
import os

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

    def fahrmodus_3(self, min_dist=12, speed=50, angle=90):
        """
        Fahrmodus 3: Fährt vorwärts, bis ein Hindernis erkannt wird.

        Args:
            min_dist (int): Mindestabstand zum Stoppen (in cm).
            speed (int): Geschwindigkeit des Fahrzeugs.
            angle (int): Lenkwinkel (in Grad).
        """
        self.drive(speed, angle)
        self.loggen(self.get_distance, self._speed, self._steering_angle, (time.time() - start_time))
        while True:
            distance = self.get_distance
            if 0 < distance < min_dist:
                self.stop()
                self.loggen(self.get_distance, self._speed, self._steering_angle, time.time() - start_time)
                break
            time.sleep(0.2)
        self.stop()

    def fahrmodus_4(self, speed=50, lenken=135):
        """
        Fahrmodus 4: Erkundungstour mit zufälligem Lenkwinkel und Rückwärtsfahrt bei Hindernissen.

        Args:
            speed (int): Geschwindigkeit des Fahrzeugs.
            lenken (int): Lenkwinkel für Richtungsänderungen.
        """
        self.loggen(self.get_distance, self._speed, self._steering_angle, 0)
        while time.time() - start_time < 30:  # Schleife endet nach 30 Sekunden
            print("---")
            self.fahrmodus_3(speed=speed, angle=random.randint(45, 135))
            self.drive(0, lenken)
            self.loggen(self.get_distance, self._speed, self._steering_angle, (time.time() - start_time))
            self.drive(-speed)
            self.loggen(self.get_distance, self._speed, self._steering_angle, time.time() - start_time)
            time.sleep(2)
            self.stop()
            self.loggen(self.get_distance, self._speed, self._steering_angle, time.time() - start_time)
        self.stop()
        print("Fahrmodus 4 beendet")

    def loggen(self, distance, speed, steering_angle, time):
        """
        Fügt die aktuellen Fahrzeugdaten einem Log hinzu und gibt diese aus.

        Args:
            distance (int): Gemessener Abstand.
            speed (int): Geschwindigkeit des Fahrzeugs.
            steering_angle (int): Aktueller Lenkwinkel.
            time (float): Zeit seit Start in Sekunden.
        """
        log.append({
            "Zeit": round(time, 3),
            "Geschwindigkeit": speed,
            "Fahrtrichtung": self.direction,
            "Lenkwinkel": steering_angle,
            "Abstand": distance
        })
        print(f"Zeit: {time:.1f}, Geschwindigkeit: {speed}, Fahrtrichtung: {self.direction}, Lenkwinkel: {steering_angle}, Abstand: {distance} cm")

if __name__ == "__main__":
    car = SonicCar()
    log = []  # Liste zum Speichern der Log-Daten
    start_time = time.time()  # Startzeitpunkt speichern

    car.fahrmodus_4()  # Fahrmodus 4 starten

    # Schreiben der Log-Daten in eine CSV-Datei
    file_name = "fahrmodus_log.csv"
    file_exists = os.path.isfile(file_name)  # Prüfen, ob die Datei existiert

    with open(file_name, mode="a", newline="") as csv_file:
        fieldnames = ["Zeit", "Geschwindigkeit", "Fahrtrichtung", "Lenkwinkel", "Abstand"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Schreibe die Kopfzeile, falls die Datei neu erstellt wurde
        if not file_exists:
            writer.writeheader()

        writer.writerows(log)  # Log-Daten in die Datei schreiben

    print(f"Log-Daten wurden in '{file_name}' gespeichert.")

