#coding=utf-8
#!/usr/bin/env python

"""
Diese Programm nutzt nur basisklassen.py!
"""

from basisklassen import  *
import traceback

class BaseCar:
    def __init__(self):
        pass


    
    @property
    def steering_angle(self):
        return 

    @property
    def speed(self):
        return

    @property
    def direction(self):
        return





class Fahrzeug:
    def __init__(self, marke, kennzeichen, fahrgestellnummer, baujahr, erstzulassung):
        self.marke = marke  # Marke des Fahrzeugs
        self.kennzeichen = kennzeichen  # Kennzeichen des Fahrzeugs
        self.fahrgestellnummer = fahrgestellnummer  # Fahrgestellnummer
        self.baujahr = baujahr  # Baujahr des Fahrzeugs
        self.erstzulassung = erstzulassung  # Datum der Erstzulassung
        self.fahrtenbuch = []  # Liste der Fahrten

    def __repr__(self):
        # Repräsentation des Objekts für die Debug-Ausgabe
        return '<{0}.{1} object at {2}>'.format(self.__module__, type(self).__name__, hex(id(self)))

    def __str__(self):
        # String-Repräsentation des Fahrzeugs mit Erstzulassung und Baujahr
        return "EZ: {}, BJ: {}".format(self.erstzulassung, self.baujahr)

    def get_last_journey(self):
        # Gibt die letzte Fahrt im Fahrtenbuch zurück, falls vorhanden
        if self.fahrtenbuch:
            return self.fahrtenbuch[-1]
        else:
            return None

try:

    
except:
    print('-- FEHLER --')
    print(traceback.format_exc())
