#Write some micropython code that can register and report short vs long #presses of the button.
#You can decide the threshold between a short and long press (example, short is less than 0.5 s, long is greater than 1 s).
# Alli Horsthuis and James Rideout

from machine import Pin
import time
button = Pin(14, Pin.IN, Pin.PULL_UP)

LONG_PRESS_MS = 1000
SHORT_PRESS_MS = 500

while True:
    
    if button.value() == 0:
       
        start_time = time.ticks_ms()
        while button.value() == 0:
            time.sleep_ms(10)
            
        press_duration = time.ticks_diff(times.ticks_ms(), start_time)
        
        if press_duration >= LONG_PRESS_MS:
            print ('long')
        elif press_duration < SHORT_PRESS_MS
            print('short')