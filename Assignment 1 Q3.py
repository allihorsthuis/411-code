#Build a "night light" that turns on an LED when it gets dark,
#as determined by a light sensor. You can determine what threshold
#intensity value you wish to use.
#Alli Horsthuis and James Rideout

from machine import Pin, ADC
import time

lightSensor = ADC(Pin(34))
lightSensor.atten(ADC.ATTN_11DB)   

led = Pin(12, Pin.OUT)

THRESHOLD = 2000           

while True:
    light = lightSensor.read()     

    if light < THRESHOLD:  
        led.value(0)
    else:                  
        led.value(1)

    time.sleep(0.1)