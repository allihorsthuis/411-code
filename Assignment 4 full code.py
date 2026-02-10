from machine import Pin, ADC, I2C, PWM
import time
import i2c_lcd

class Timer:
    def __init__(self):
        self.m = 0
        self.s = 0
        self.running = False
        self.mode = "MIN"
        self.last = time.ticks_ms()

    def total(self):
        return self.m * 60 + self.s

    def toggle(self):
        self.mode = "SEC" if self.mode == "MIN" else "MIN"

    def start(self):
        if self.total() > 0:
            self.running = True
            self.last = time.ticks_ms()

    def tick(self):
        if not self.running:
            self.last = time.ticks_ms()
            return False
        now = time.ticks_ms()
        if time.ticks_diff(now, self.last) >= 1000:
            self.last = time.ticks_add(self.last, 1000)
            if self.total() == 0:
                self.running = False
                return True
            if self.s > 0:
                self.s -= 1
            else:
                self.m -= 1
                self.s = 59
        return False

BTN_MODE = Pin(25, Pin.IN, Pin.PULL_UP)
BTN_GO = Pin(26, Pin.IN, Pin.PULL_UP)

POT = ADC(Pin(32))
POT.atten(ADC.ATTN_11DB)

LED = Pin(12, Pin.OUT)
BUZ = Pin(27, Pin.OUT)
BUZ.value(1)

i2c = I2C(0, scl=Pin(21), sda=Pin(22), freq=400000)
lcd = i2c_lcd.I2cLcd(i2c, 0x27, 2, 16)

def pot_to(maxv):
    return int(POT.read() * maxv / 4095)

def display(t, alarm):
    lcd.move_to(0, 0)
    lcd.putstr(f"{t.m:02d}:{t.s:02d}            "[:16])
    lcd.move_to(0, 1)
    if alarm:
        lcd.putstr("ALARM           "[:16])
    elif t.running:
        lcd.putstr("RUNNING        "[:16])
    else:
        lcd.putstr(f"SET {t.mode}        "[:16])

t = Timer()
alarm = False
phase = 0
last_m = 1
last_g = 1
lcd.clear()

while True:
    m = BTN_MODE.value()
    g = BTN_GO.value()

    if last_m == 1 and m == 0 and not t.running and not alarm:
        t.toggle()
        time.sleep_ms(150)

    if last_g == 1 and g == 0:
        if alarm:
            alarm = False
        else:
            t.start()
        time.sleep_ms(150)

    last_m = m
    last_g = g

    if not t.running and not alarm:
        if t.mode == "MIN":
            t.m = min(pot_to(100), 99)
        else:
            t.s = min(pot_to(60), 59)

    if t.tick():
        alarm = True

    if alarm:
        on = phase % 2 == 0
        LED.value(on)
        BUZ.value(0 if on else 1)
        phase += 1
    else:
        LED.value(0)
        BUZ.value(1)

    display(t, alarm)
    time.sleep_ms(100)
