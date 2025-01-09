from basecar import *
from basisklassen import Ultrasonic

class SonicCar(BaseCar):
    def __init__(self):
        self.ultrasonic = Ultrasonic()
        self._distance = 0
    
    @property
    def get_distance(self):
        self._distance = self.ultrasonic.distance()
        return self._distance

if __name__ == "__main__":
    car = SonicCar() 
    print(car.get_distance)