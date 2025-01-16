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
                self.configdata = json.load(f)
                self.turning_offset = self.configdata.get("turning_offset", 0)
                self.forward_A = self.configdata.get("forward_A", 1)
                self.forward_B = self.configdata.get("forward_B", 1)
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
        self._log = [] #Log erstellen
        self.ismanually_stopped = False #Externe Stoppfunktion
        self.start_time = 0

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

    def loggen(self, time = 0.0, speed = 0, direction = 0, steering_angle = 0, distance = 0,  ir_value = [0,0,0,0,0], f_modus = 0):
        """
        Fügt die aktuellen Fahrzeugdaten einem Log hinzu und gibt diese aus.

        Args:
            time (float): Zeit seit Start in Sekunden.
            speed (int): Geschwindigkeit des Fahrzeugs.
            direction (int): Fahrtrichtung
            steering_angle (int): Aktueller Lenkwinkel.
            distance (int): Gemessener Abstand.
            ir_value (list): Status der IR-LED´s
            f_modus (int): Fahrmodusauswahl 
        """
        self._log.append({
            "Zeit": round(time, 3),
            "Geschwindigkeit": speed,
            "Fahrtrichtung": direction,
            "Lenkwinkel": steering_angle,
            "Abstand": distance,
            "IR_Status": ir_value,
            "Fahrmodus": f_modus
        })
        print(f"Zeit: {time:.1f}, Geschwindigkeit: {speed}, Fahrtrichtung: {direction}, Lenkwinkel: {steering_angle}, Abstand: {distance} cm, IR_Status: {ir_value}, Fahrmodus: {f_modus}")            

    def set_fahren_und_warten(self, speed: int, steering_angle: int, wait_time: float, f_modus: int):
        self.drive(speed=speed, steering_angle=steering_angle)
        self.loggen(time.time() - self.start_time, self._speed, self._direction, self._steering_angle, 0, [0,0,0,0,0], f_modus) 
        # Startzeit der Funktion zwischenspeichern
        run_time = time.time()
        # Schleife um ein unterbrechen wärend der wait Funktion durch Tastendruck zu ermöglichen
        while not self.ismanually_stopped:
            # Aktuelle Zeit zwischenspeichern
            current_time = time.time()
            # Schleife nach ablauf der Zeit verlassen
            if current_time - run_time >= wait_time:
                break
        if self.ismanually_stopped:
            self.stop()
        self.loggen(time.time() - self.start_time, self._speed, self._direction, self._steering_angle, 0, [0,0,0,0,0], f_modus) 


    def fahrmodus_1(self, speed=50):
        # Setzen der Startzeit
        self.start_time = time.time()  
        # Erster Eintrag im Log auf Null setzen         
        self.loggen(0.0, 0, 0, 90, 0, [0,0,0,0,0], 1)   
        self.set_fahren_und_warten(speed=speed, steering_angle=90, wait_time=2, f_modus=1)
        self.set_fahren_und_warten(speed=0, steering_angle=90, wait_time= 1, f_modus=1)
        self.set_fahren_und_warten(speed=-speed, steering_angle=90, wait_time=2, f_modus=1)
        self.stop()

    def fahrmodus_2(self, speed = 50):    
        # Setzen der Startzeit
        self.start_time = time.time()  
        # Erster Eintrag im Log auf Null setzen
        self.loggen(0, 0, 0, 90, 0, [0,0,0,0,0], 2)    
        self.set_fahren_und_warten(speed=speed, steering_angle=90, wait_time=1, f_modus= 2)
        self.set_fahren_und_warten(speed=speed, steering_angle=135, wait_time=8, f_modus= 2)
        self.set_fahren_und_warten(speed=-speed, steering_angle=135, wait_time=8, f_modus= 2)
        self.set_fahren_und_warten(speed=-speed, steering_angle=90, wait_time=1, f_modus=2)
        self.set_fahren_und_warten(speed=0, steering_angle=90, wait_time=1, f_modus=2)

        self.set_fahren_und_warten(speed=speed, steering_angle=90, wait_time=1, f_modus= 2)
        self.set_fahren_und_warten(speed=speed, steering_angle=45, wait_time=8, f_modus= 2)
        self.set_fahren_und_warten(speed=-speed, steering_angle=45, wait_time=8, f_modus= 2)
        self.set_fahren_und_warten(speed=-speed, steering_angle=90, wait_time=1, f_modus=2)
        self.set_fahren_und_warten(speed=0, steering_angle=90, wait_time=1, f_modus=2)

if __name__ == "__main__":
    car = BaseCar()
    car.fahrmodus_1(50)