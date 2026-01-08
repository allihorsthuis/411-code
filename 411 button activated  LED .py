from machine import Pin
import utime

led= Pin(12, Pin.OUT)
button= Pin(14, Pin.IN, Pin.PULL_UP)

while True:
    if button.value() == 0:
        led.value(1)
    else:
            led.value(0)
            utime.sleep(0.1).

    
    