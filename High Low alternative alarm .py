#Alli Horsthuis and James Rideout Question 4
import machine
from machine import I2C, Pin, time_pulse_us
import i2c_lcd
import time

trigger = Pin(18, Pin.OUT)
echo = Pin(5, Pin.IN)

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
lcd = i2c_lcd.I2cLcd(i2c, 0x27, 2, 16)

led = Pin(12, Pin.OUT) #wire LED to Pin 12 please!

low = 9999
high = 0

def blink(n):
    for _ in range(n):
        led.on()
        time.sleep_ms(120)
        led.off()
        time.sleep_ms(120)

while True:
    trigger.off()
    time.sleep_us(2)
    trigger.on()
    time.sleep_us(10)
    trigger.off()

    duration = time_pulse_us(echo, 1)

    if duration > 0:
        distance_cm = (duration * 0.0343) / 2

        if distance_cm < low:
            blink(1)     #LED blinks once for new low 
            low = distance_cm

        if distance_cm > high:
            blink(2)      #LED blinks twice for new high
            high = distance_cm

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