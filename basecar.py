#coding=utf-8
#!/usr/bin/env python

"""
Diese Programm nutzt nur basisklassen.py!
"""

from basisklassen import  FrontWheels, BackWheels
#import traceback
import time

class BaseCar():
    def __init__(self):
        self.frontwheels = FrontWheels()
        self.backwheels = BackWheels()
        self._steering_angle = self.frontwheels.turn(90)
        self._speed = 0

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

    #--Einstellung Motor--#
    #Getter
    @property
    def direction(self):
        return 1
    
car = BaseCar()

print(car.steering_angle)
car.steering_angle = 20
print(car.steering_angle)
time.sleep(2)
car.steering_angle = 120
time.sleep(2)
car.steering_angle = 90