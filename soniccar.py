from basecar import BaseCar
from basisklassen import Ultrasonic
import time
import random

class SonicCar(BaseCar):
    def __init__(self):
        super().__init__()
        self.ultrasonic = Ultrasonic()
        self._distance = 0
    
    @property
    def get_distance(self):
        self._distance = self.ultrasonic.distance()
        return self._distance

    def fahrmodus_3(self,min_dist = 8,speed = 50, angle=90):
        
        self.drive(speed,angle)
        self.loggen(self.get_distance,self._speed,self._steering_angle,(time.time() - start_time))
        while True:
            distance = self.get_distance
            if 0 < distance < min_dist:
                self.stop()
                self.loggen(self.get_distance,self._speed,self._steering_angle,time.time() - start_time)
                break
            time.sleep(0.2)
        self.stop()
    
    
    def fahrmodus_4(self, speed = 30, lenken = 135):
        #start_time = time.time()
        while time.time() - start_time < 30: # Schleife endet nach 30 Sekunden
            print("---")
            self.fahrmodus_3(speed = speed, angle= random.randint(45, 135))
            self.drive(0,lenken)
            self.loggen(self.get_distance,self._speed,self._steering_angle,(time.time() - start_time))
            self.drive(-speed)
            time.sleep(2)
            self.loggen(self.get_distance,self._speed,self._steering_angle,time.time() - start_time)
            self.stop()
            self.loggen(self.get_distance,self._speed,self._steering_angle,time.time() - start_time)
        self.stop()
        print("Fahrmodus 4 beendet")
    
    def loggen(self, distance, speed, steering_angle, time):
            log.append({
            "Abstand": distance,
            "Geschwindigkeit": speed,
            "Lenkwinkel": steering_angle,
            "Laufzeit": time
            })
            print(f"Gemessene Entfernung: {distance} cm, Geschwindigkeit: {speed}, Lenkwinkel: {steering_angle}, Laufzeit: {time:.1f}")

       
if __name__ == "__main__":
    car = SonicCar() 
    log = []
    start_time = time.time()
    car.fahrmodus_4()
    #print(car.get_distance)