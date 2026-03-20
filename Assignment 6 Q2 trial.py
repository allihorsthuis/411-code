#Alli Horsthuis and James Ridout
from machine import Pin, ADC, I2C
from time import sleep_ms, ticks_ms, ticks_diff
from i2c_lcd import I2cLcd

I2C_ADDR = 0x27
lcd = I2cLcd(I2C(0, sda=Pin(21), scl=Pin(22)), I2C_ADDR, 2, 16)

light_sensor = ADC(Pin(34))
light_sensor.atten(ADC.ATTN_11DB)
light_sensor.width(ADC.WIDTH_12BIT)

clk = Pin(32, Pin.IN, Pin.PULL_UP)
dt = Pin(33, Pin.IN, Pin.PULL_UP)
sw = Pin(23, Pin.IN, Pin.PULL_UP)

led_b = Pin(12, Pin.OUT)

min_level = 800
max_level = 2000

# 0 = MIN, 1 = MAX
selected = 0

last_clk = clk.value()
last_button = sw.value()
last_press_time = 0
last_turn_time = 0

# temporary message on line 1 after button press
flash_message = None
flash_until = 0


def clamp(x, lo, hi):
    return max(lo, min(x, hi))


def get_bars(raw):
    if max_level <= min_level:
        return 0
    raw = clamp(raw, min_level, max_level)
    return int((raw - min_level) / (max_level - min_level) * 16)


def make_bar(n):
    return "O" * n + "-" * (16 - n)


def pad16(text):
    return text[:16] + " " * (16 - len(text[:16]))


def update_encoder():
    global last_clk, selected, last_turn_time

    c = clk.value()

    # falling edge detect
    if last_clk == 1 and c == 0:
        now = ticks_ms()

        if ticks_diff(now, last_turn_time) > 4:
            # with only 2 menu items, toggle each valid turn
            selected = 1 - selected
            last_turn_time = now

    last_clk = c


def check_button(raw):
    global last_button, last_press_time
    global min_level, max_level
    global flash_message, flash_until

    b = sw.value()

    if last_button == 1 and b == 0:
        now = ticks_ms()

        if ticks_diff(now, last_press_time) > 200:

            if selected == 0:
                min_level = raw
                if min_level >= max_level:
                    max_level = min_level + 1
                flash_message = pad16("NEW MIN={}".format(min_level))
            else:
                max_level = raw
                if max_level <= min_level:
                    min_level = max_level - 1
                flash_message = pad16("NEW MAX={}".format(max_level))

            flash_until = now + 800
            last_press_time = now

    last_button = b


def update_led(raw):
    if raw < min_level or raw > max_level:
        led_b.value(1)
    else:
        led_b.value(0)


def update_lcd(raw):
    global flash_message, flash_until

    now = ticks_ms()

    lcd.move_to(0, 0)
    if flash_message is not None and ticks_diff(flash_until, now) > 0:
        lcd.putstr(flash_message)
    else:
        flash_message = None
        bars = get_bars(raw)
        lcd.putstr(make_bar(bars))

    if selected == 0:
        line2 = pad16(">MIN:{:4d}".format(min_level))
    else:
        line2 = pad16(">MAX:{:4d}".format(max_level))

    lcd.move_to(0, 1)
    lcd.putstr(line2)


while True:
    raw = light_sensor.read()

    update_encoder()
    check_button(raw)
    update_led(raw)
    update_lcd(raw)

    sleep_ms(1)