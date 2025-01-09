#coding=utf-8
#!/usr/bin/env python

"""
Diese Programm nutzt nur basisklassen.py!
"""

from basisklassen import FrontWheels, BackWheels
#import traceback
import json
import time

class BaseCar():
    def __init__(self):
        try:
            with open("config.json", "r") as f:
                self.data = json.load(f)
                self.turning_offset = self.data["turning_offset"]
                self.forward_A = self.data["forward_A"]
                self.forward_B = self.data["forward_B"]
                print("Daten in config.json:")
                print(" - Turning Offset: ", self.turning_offset)
                print(" - Forward A: ", self.forward_A)
                print(" - Forward B: ", self.forward_B)
        except:
            print("Keine geeignete Datei config.json gefunden!")
        self.frontwheels = FrontWheels(turning_offset=self.turning_offset)
        self.backwheels = BackWheels(self.forward_A, self.forward_B)
        self._steering_angle = self.frontwheels.turn(90)
        self._speed = 0
        self._direction = 0       

    #--Lenkwinkel--#
    #Getter
    @property
    def steering_angle(self):
        return self._steering_angle
    
    #Setter
    @steering_angle.setter
    def steering_angle(self,angle):
        if 45 <= angle <= 135:
            self._steering_angle = angle
        else:
            print("kann den Winkel so nicht setzen")
            print("Setze den Winkel")
            self._steering_angle = min(max(angle,45),135)
        self.frontwheels.turn(self._steering_angle)


    #--Geschwindigkeit--#
    #Getter
    @property
    def speed(self):
        return self._speed
    
    #Setter
    @speed.setter
    def speed(self, speed_value):
        if speed_value is None:
            speed_value = self._speed  # Behalte den aktuellen Wert, falls kein neuer Wert gesetzt wird
        self._speed = min(max(speed_value, -100), 100)  # Begrenzung auf den Bereich -100 bis 100
        if self._speed > 0:
            self.backwheels.forward()  # Fahrtrichtung: vorwärts
            self._direction = 1
        elif self._speed < 0:
            self.backwheels.backward()  # Fahrtrichtung: rückwärts
            self._direction = -1
        else:
            self.backwheels.stop()  # Fahrzeug stoppt
            self._direction = 0
        self.backwheels.speed = abs(self._speed)  # Geschwindigkeit an die Hinterräder weitergeben

    #--Einstellung Fahrtrichtung--#
    #Getter
    @property
    def direction(self):
        return self._direction
    
    #Drive Methode
    def drive(self, speed=None, steering_angle=None):
        if speed is not None:
            self.speed = speed
        if steering_angle is not None:
            self.steering_angle = steering_angle
    
    def fahrmodus_1(self):

        def set_fahren_und_warten(speed, steering_angle, wait_time):
            #Funktion, um Geschwindigkeit und Lenkwinkel zu setzen und eine Pause einzulegen.
            self.drive(speed=speed, steering_angle=steering_angle)
            print(f'Geschwindigkeit : {speed}, Lenkwinkel : {steering_angle}')
            time.sleep(wait_time)

        # Initialisierung
        set_fahren_und_warten(0, 80, 0.1)
        set_fahren_und_warten(0, 90, 0)

        # Vorwärtsfahrt
        set_fahren_und_warten(30, 90, 5)

        # Zwischenstopp
        set_fahren_und_warten(0, 90, 1)

        # Rückwärtsfahrt
        set_fahren_und_warten(-30, 90, 5)

        # Endstopp
        set_fahren_und_warten(0, 90, 0)
    
    def fahrmodus_2(self):
        def set_fahren_und_warten(speed, steering_angle, wait_time):
            #Funktion, um Geschwindigkeit und Lenkwinkel zu setzen und eine Pause einzulegen.
            self.drive(speed=speed, steering_angle=steering_angle)
            print(f'Geschwindigkeit : {speed}, Lenkwinkel : {steering_angle}')
            time.sleep(wait_time)

        speedvorgabe = 30
        lenkwinkelvorgabe = 135

        # Initialisierung
        print('01-Initialisierung')
        set_fahren_und_warten(0, 80, 0.1)
        set_fahren_und_warten(0, 90, 0.1)
        print('01-Initialisierung beendet')

        print('-----')

        # Vorwärtsfahrt für 1 Sekunde
        print('02-1 Sekunde vorwärts')
        set_fahren_und_warten(speedvorgabe, 90, 1)
        print('02-Fertig!')

        print('-----')

        # Anhalten und Einschlagen
        print('03-Anhalten und einschlagen')
        set_fahren_und_warten(0, lenkwinkelvorgabe, 0.1)
        print('03-Angehalten')

        print('-----')

        # Vorwärts rechts herum fahren
        print('04-8 Sekunden vorwärts rechtsrum fahren')
        set_fahren_und_warten(speedvorgabe, lenkwinkelvorgabe, 8)
        print('04-Fertig!')

        print('-----')

        # Anhalten
        print('05-Anhalten')
        set_fahren_und_warten(0, lenkwinkelvorgabe, 0.1)
        print('05-Angehalten')

        print('-----')

        # Rückwärtsfahrt rechts herum
        print('06-8 Sekunden rückwärts fahren')
        set_fahren_und_warten(-speedvorgabe, lenkwinkelvorgabe, 8)
        print('06-Fertig!')

        print('-----')

        # Gerade stellen
        print('07-Anhalten und gerade stellen')
        set_fahren_und_warten(0, 90, 0.1)
        print('07-Angehalten')

        print('-----')

        # Rückwärtsfahrt für 1 Sekunde
        print('08-1 Sekunde rückwärts')
        set_fahren_und_warten(-speedvorgabe, 90, 1)
        print('08-Fertig!')

        # Endstopp
        set_fahren_und_warten(0, 90, 0)


if __name__ == '__main__':
    car = BaseCar()

    # Fahrmodus 1
    car.fahrmodus_1()

    # print(car.steering_angle)
    # car.steering_angle = 20
    # print(car.steering_angle)
    # time.sleep(2)
    # car.steering_angle = 120
    # time.sleep(2)
    # car.steering_angle = 90

    # t= 1
    # car.speed = 30
    #car.backwheels.forward()
    # print('Geschwindigkeit : {}'.format(car.speed))
    # print('Fahrtrichtung : {}'.format(car.direction))
    # time.sleep(t)
    # car.backwheels.speed = 40
    # print('forward speed : {}'.format(car.speed))

    # time.sleep(t)
    # car.backwheels.speed = 20
    # print('forward speed : {}'.format(car.speed))

    # time.sleep(t)
    # car.backwheels.stop()
    # print('stop speed : {}'.format(car.speed))
    # time.sleep(t * 2)
    # car.backwheels.speed = 20
    # print('forward speed : {}'.format(car.speed))

    # time.sleep(t)
    # car.backwheels.backward()
    # print('now backward')
    # print('backward speed : {}'.format(car.speed))

    # time.sleep(t * 4)
    # car.speed = 0
    # print('stop speed : {}'.format(car.speed))