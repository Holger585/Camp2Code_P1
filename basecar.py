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
    def speed(self,speed_value):
        if speed_value == None:
            speed_value = self._speed
        self._speed = min(max(speed_value,-100),100)
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


    #--Einstellung Fahrtrichtung--#
    #Getter
    @property
    def direction(self):
        return self._direction
    
    def fahrmodus_1(self):
        self.speed = 0
        self.steering_angle = 80
        time.sleep(.1)
        self.steering_angle = 90
        self.speed = 30
        print(f'Geschwindigkeit : {self.speed}')
        time.sleep(3)
        self.speed = 0
        time.sleep(1)
        self.speed = -30
        print(f'Geschwindigkeit : {self.speed}')
        time.sleep(3)
        self.speed = 0
    
    def fahrmodus_2(self):
        speedvorgabe = 30
        lenkwinkelvorgabe = 120

        print('01-Initialisierung')
        self.speed = 0
        print(f'01-Geschwindigkeit : {self.speed}')
        self.steering_angle = 80
        time.sleep(.1)        
        self.steering_angle = 90 
        print(f'01-Lenkwinkel : {self.steering_angle}')
        time.sleep(.1)
        print('01-Initialisierung beendet')

        print('-----')

        print('02-1 Sekunde vorwärts')
        self.speed = speedvorgabe
        print(f'02-Geschwindigkeit : {self.speed}')
        self.steering_angle = 90 
        print(f'02-Lenkwinkel : {self.steering_angle}')        
        time.sleep(1)
        print('02-Fertig!')

        print('-----')

        print('03-Anhalten und einschlagen')
        self.speed = 0
        print(f'03-Geschwindigkeit : {self.speed}')
        self.steering_angle  = lenkwinkelvorgabe 
        print(f'03-Lenkwinkel : {self.steering_angle}')
        time.sleep(0.1)
        print('03-Angehalten')

        print('-----')

        print('04-8 Sekunden vorwärts rechtsrum fahren')
        self.speed = speedvorgabe
        print(f'04-Geschwindigkeit : {self.speed}')
        self.steering_angle  = lenkwinkelvorgabe 
        print(f'04-Lenkwinkel : {self.steering_angle}')        
        time.sleep(8)
        print('04-Fertig!')

        print('-----')

        print('05-Anhalten')
        self.speed = 0
        print(f'05-Geschwindigkeit : {self.speed}')
        self.steering_angle  = lenkwinkelvorgabe  
        print(f'05-Lenkwinkel : {self.steering_angle}')
        time.sleep(0.1)
        print('05-Angehalten')

        print('-----')

        print('06-8 Sekunden rückwärts fahren')
        self.speed = -(speedvorgabe)
        print(f'06-Geschwindigkeit : {self.speed}')
        self.steering_angle  = lenkwinkelvorgabe 
        print(f'06-Lenkwinkel : {self.steering_angle}')        
        time.sleep(8)
        print('06-Fertig!')

        print('-----')

        print('07-Anhalten und gerade stellen')
        self.speed = 0
        print(f'07-Geschwindigkeit : {self.speed}')
        self.steering_angle  = 90 
        print(f'07-Lenkwinkel : {self.steering_angle}')
        time.sleep(0.1)
        print('07-Angehalten')

        print('-----')

        print('08-1 Sekunde rückwärts')
        self.speed = -(speedvorgabe)
        print(f'08-Geschwindigkeit : {self.speed}')
        self.steering_angle = 80
        time.sleep(.1)        
        self.steering_angle = 90 
        print(f'08-Lenkwinkel : {self.steering_angle}')        
        time.sleep(1)
        print('08-Fertig!')

        self.speed = 0


if __name__ == '__main__':
    car = BaseCar()

    # Fahrmodus 1
    car.fahrmodus_2()

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