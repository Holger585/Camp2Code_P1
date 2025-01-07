#coding=utf-8
#!/usr/bin/env python

"""
Diese Programm nutzt nur basisklassen.py!
"""

from basisklassen import  *
import traceback



try:
    #Wackeln mit den Vorderrädern als Gruß
    fw=FrontWheels()
    fw.turn(90)
    time.sleep(1)
    fw.turn(45)
    time.sleep(n)
    fw.turn(135)
    time.sleep(n)
    fw.turn(90)
    time.sleep(n)
    fw.turn(135)
    time.sleep(n)
    fw.turn(45)
    time.sleep(n)
    fw.turn(90)
    time.sleep(1)
    
except:
    print('-- FEHLER --')
    print(traceback.format_exc())
