import json
import time
from basisklassen import FrontWheels, BackWheels

class BaseCar:
    """
    Basisklasse für ein ferngesteuertes Fahrzeug, das Vorder- und Hinterräder steuern kann.
    Die Konfiguration wird aus einer JSON-Datei geladen, mit Fallback auf Standardwerte.
    """

    def __init__(self):
        """
        Initialisiert das Fahrzeug, indem es Konfigurationsdaten lädt und die Räder initialisiert.
        """
        try:
            with open("config.json", "r") as f:
                self.data = json.load(f)
                self.turning_offset = self.data.get("turning_offset", 0)
                self.forward_A = self.data.get("forward_A", 1)
                self.forward_B = self.data.get("forward_B", 1)
        except FileNotFoundError:
            print("Fehler: config.json nicht gefunden. Standardwerte werden verwendet.")
            self.turning_offset = 0
            self.forward_A = 0
            self.forward_B = 0

        self.frontwheels = FrontWheels(turning_offset=self.turning_offset)
        self.backwheels = BackWheels(self.forward_A, self.forward_B)
        self._steering_angle = 90  # Standardwinkel in der Mitte
        self._speed = 0  # Initialgeschwindigkeit
        self._direction = 0  # Stillstand

    @property
    def steering_angle(self):
        """
        Gibt den aktuellen Lenkwinkel des Fahrzeugs zurück.
        """
        return self._steering_angle

    @steering_angle.setter
    def steering_angle(self, angle):
        """
        Setzt den Lenkwinkel und passt ihn an zulässige Grenzen an.

        Args:
            angle (int): Der gewünschte Lenkwinkel.
        """
        if angle < 45 or angle > 135:
            print(f"Warnung: Eingabewinkel {angle} ist nicht zulässig. Der Winkel wird angepasst.")
        self._steering_angle = max(45, min(135, angle))
        self.frontwheels.turn(self._steering_angle)

    @property
    def speed(self):
        """
        Gibt die aktuelle Geschwindigkeit des Fahrzeugs zurück.
        """
        return self._speed

    @speed.setter
    def speed(self, speed_value):
        """
        Setzt die Geschwindigkeit und begrenzt sie auf zulässige Werte.

        Args:
            speed_value (int): Die gewünschte Geschwindigkeit (-100 bis 100 ausgenommen -30 bis 30).
        """
        self._speed = max(-100, min(100, speed_value))
        if -30 < speed_value < 30:
            if speed_value == 0:
                pass
            elif speed_value < 0:
                self._speed = -30
                print(f"Geschwindigkeit angepasst: {speed_value} -> {self._speed} km/h")
            else:
                self._speed = 30        
                print(f"Geschwindigkeit angepasst: {speed_value} -> {self._speed} km/h")

    @property
    def direction(self):
        """
        Gibt die aktuelle Fahrtrichtung des Fahrzeugs zurück:
        1 = Vorwärts, -1 = Rückwärts, 0 = Stillstand.
        """
        return self._direction

    def drive(self, speed=None, steering_angle=None):
        """
        Steuert das Fahrzeug mit der angegebenen Geschwindigkeit und dem Lenkwinkel.

        Args:
            speed (int, optional): Die gewünschte Geschwindigkeit.
            steering_angle (int, optional): Der gewünschte Lenkwinkel.
        """
        if speed is not None:
            self.speed = speed
            if self._speed > 0:
                self.backwheels.forward()
                self._direction = 1
            elif self._speed < 0:
                self.backwheels.backward()
                self._direction = -1
            else:
                self.backwheels.stop()
                self._direction = 0
            self.backwheels.speed = abs(self._speed)
        if steering_angle is not None:
            self.steering_angle = steering_angle

    def stop(self):
        """
        Stoppt das Fahrzeug vollständig.
        """
        self.drive(speed=0)
        #print("Fahrzeug wurde angehalten.")

    def set_fahren_und_warten(self, speed, steering_angle, wait_time):
        """
        Bewegt das Fahrzeug mit gegebener Geschwindigkeit und Lenkwinkel und wartet anschließend.

        Args:
            speed (int): Die Geschwindigkeit.
            steering_angle (int): Der Lenkwinkel.
            wait_time (float): Die Wartezeit in Sekunden.
        """
        self.drive(speed=speed, steering_angle=steering_angle)
        print(f"Geschwindigkeit: {self._speed}, Lenkwinkel: {self._steering_angle}")
        time.sleep(wait_time)

    def fahrmodus_1(self):
        """
        Führt eine vordefinierte Abfolge von Bewegungen aus.
        """
        self.set_fahren_und_warten(0, 80, 0.1)
        self.set_fahren_und_warten(0, 90, 0)
        self.set_fahren_und_warten(30, 90, 5)
        self.set_fahren_und_warten(0, 90, 1)
        self.set_fahren_und_warten(-30, 90, 5)
        self.stop()

    def fahrmodus_2(self):
        """
        Führt eine komplexere vordefinierte Abfolge von Bewegungen aus.
        """
        speedvorgabe = 30
        lenkwinkelvorgabe = 135

        print("01-Initialisierung")
        self.set_fahren_und_warten(0, 80, 0.1)
        self.set_fahren_und_warten(0, 90, 0.1)
        print("01-Initialisierung beendet")

        print("02-1 Sekunde vorwärts")
        self.set_fahren_und_warten(speedvorgabe, 90, 1)
        print("02-Fertig!")

        print("03-Anhalten und einschlagen")
        self.set_fahren_und_warten(0, lenkwinkelvorgabe, 0.1)
        print("03-Angehalten")

        print("04-8 Sekunden vorwärts rechtsrum fahren")
        self.set_fahren_und_warten(speedvorgabe, lenkwinkelvorgabe, 8)
        print("04-Fertig!")

        print("05-Anhalten")
        self.set_fahren_und_warten(0, lenkwinkelvorgabe, 0.1)
        print("05-Angehalten")

        print("06-8 Sekunden rückwärts fahren")
        self.set_fahren_und_warten(-speedvorgabe, lenkwinkelvorgabe, 8)
        print("06-Fertig!")

        print("07-Anhalten und gerade stellen")
        self.set_fahren_und_warten(0, 90, 0.1)
        print("07-Angehalten")

        print("08-1 Sekunde rückwärts")
        self.set_fahren_und_warten(-speedvorgabe, 90, 1)
        print("08-Fertig!")

        self.set_fahren_und_warten(0, 90, 1)  # Sicherstellen, dass das Fahrzeug anhält

if __name__ == "__main__":
    car = BaseCar()
    #help(BaseCar)
    car.fahrmodus_1()
    #car.fahrmodus_2()