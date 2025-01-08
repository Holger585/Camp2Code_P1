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
    def speed(self,speed_value):
        if speed_value == None:
            speed_value = self._speed
        self._speed = min(max(speed_value,-100),100)
        if self._speed > 0:
            self.backwheels.forward()
        elif self._speed < 0:
            self.backwheels.backward()
        else: 
            self.backwheels.stop()
        self.backwheels.speed = abs(self._speed)


    #--Einstellung Motor--#
    #Getter
    @property
    def direction(self):
        return 1

if __name__ == '__main__':
    car = BaseCar()

    print(car.steering_angle)
    car.steering_angle = 20
    print(car.steering_angle)
    time.sleep(2)
    car.steering_angle = 120
    time.sleep(2)
    car.steering_angle = 90

    t= 1
    car.speed = 30
    #car.backwheels.forward()
    print('forward speed : {}'.format(car.speed))

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
    # car.backwheels.speed = 0
    # print('stop speed : {}'.format(car.speed))