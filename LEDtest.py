"""
micropython
test the binary clock LEDs in sequence
GPs lists the GPIO pins in use
"""
import machine
from machine import Pin
import time
from time import sleep

GPs = (18,19,20,21,22,26,12,13,14,15,16,17,0,1,2,3,4,28)
# Turn off all LEDs
for counter, GP in enumerate(GPs):
    object = Pin(GP,Pin.OUT)
    object.value(0)
    
# Turn on each LED in sequence - low seconds to high hours + status LED
sleep(1)
for counter, GP in enumerate(GPs):
    print ("counter =",counter," GP =",GP)
    object = Pin(GP,Pin.OUT)
    object.value(1)
    sleep(0.4)
    object.value(0)
