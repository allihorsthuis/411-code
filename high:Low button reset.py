import machine
from machine import I2C, Pin, time_pulse_us
import i2c_lcd
import time

trigger = Pin(18, Pin.OUT)
echo = Pin(5, Pin.IN)

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
lcd = i2c_lcd.I2cLcd(i2c, 0x27, 2, 16)

# Button: connect one side to 14, other side to GND make sure not to wire to the 5 volt side please!
btn = Pin(14, Pin.IN, Pin.PULL_UP)  

low = 9999
high = 0

while True:
    
    if btn.value() == 0:
        low = 9999
        high = 0
        time.sleep_ms(200)  

    trigger.off()
    time.sleep_us(2)
    trigger.on()
    time.sleep_us(10)
    trigger.off()

    duration = time_pulse_us(echo, 1)

    if duration > 0:
        distance_cm = (duration * 0.0343) / 2
        low = min(low, distance_cm)
        high = max(high, distance_cm)

        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Dist: {:.1f}cm".format(distance_cm))
        lcd.move_to(0, 1)
        lcd.putstr("L:{:.1f} H:{:.1f}cm".format(low, high))
    else:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("No echo")

    time.sleep(1)