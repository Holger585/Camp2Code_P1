from basecar import BaseCar
from basisklassen import Ultrasonic
import time

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
        
        while True:
            distance = self.get_distance
            print(f"Hindernis erkannt in  {distance} cm.")
            if 0 < distance < min_dist:
                self.stop()
                print(f"Hindernis erkannt in  {distance} cm.")
                break
            time.sleep(0.2)
                
if __name__ == "__main__":
    car = SonicCar() 
    car.fahrmodus_3()
    print(car.get_distance)