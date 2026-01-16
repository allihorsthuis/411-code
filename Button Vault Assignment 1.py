#Create a program that "unlocks" a vault by requiring the user to input a code using one or two buttons.
#For example, you could use only a single button, and combination of long and short presses (eg SSLS).
#You could use two buttons (left and right), and the code could be (LLRL), ignoring the press duration.
#Or a combination of those for a more secure password!

#Alli Horsthuis and James Rideout

from machine import Pin
import time
button = Pin(14, Pin.IN, Pin.PULL_UP)

CODE = "LSLSS"
LONG_PRESS_MS = 1000
SHORT_PRESS_MS = 500

entered = ""

while True:
    
    if button.value() == 0:
       start_time = time.ticks_ms()
       
       while button.value() == 0:
            time.sleep_ms(10)
            
        press_duration = time.ticks_diff(time.ticks_ms(), start_time)
        
        if press_duration < SHORT_PRESS_MS:
            entered += "S"
            print("S")
        elif press_duration >= LONG_PRESS_MS:
            entered += "L"
            print("L")
        if not CODE.startswith(entered): #this may or may not be needed
            entered = ""
        if entered == CODE:
            print("unlocked")
            entered = ""
        
        time.sleep_ms(250)    
            