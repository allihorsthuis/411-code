from machine import Pin, ADC, I2C
from time import sleep_ms, ticks_ms, ticks_diff
from i2c_lcd import I2cLcd

# -----------------------------
# LCD setup
# -----------------------------
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# -----------------------------
# Light sensor setup
# -----------------------------
light_sensor = ADC(Pin(34))
light_sensor.atten(ADC.ATTN_11DB)
light_sensor.width(ADC.WIDTH_12BIT)

# -----------------------------
# Rotary encoder + button
# -----------------------------
clk = Pin(32, Pin.IN, Pin.PULL_UP)
dt = Pin(33, Pin.IN, Pin.PULL_UP)
sw = Pin(23, Pin.IN, Pin.PULL_UP)

# -----------------------------
# Blue LED
# -----------------------------
led_b = Pin(12, Pin.OUT)

# -----------------------------
# Initial min/max values
# -----------------------------
min_level = 800
max_level = 2000

# 0 = MIN selected, 1 = MAX selected
selected = 0

# -----------------------------
# State variables
# -----------------------------
last_clk = clk.value()
last_button = sw.value()
last_turn_time = 0
last_press_time = 0

# Optional short message after saving
flash_message = None
flash_until = 0

# -----------------------------
# Helper functions
# -----------------------------
def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value

def pad16(text):
    text = str(text)
    if len(text) > 16:
        return text[:16]
    return text + " " * (16 - len(text))

def get_bar_count(raw):
    global min_level, max_level

    # safety check
    if max_level <= min_level:
        return 0

    # raw at or below min = empty bar
    if raw <= min_level:
        return 0

    # raw at or above max = full bar
    if raw >= max_level:
        return 16

    # scale raw between min and max
    raw = clamp(raw, min_level, max_level)
    fraction = (raw - min_level) / (max_level - min_level)
    filled = round(fraction * 16)

    # extra safety clamp
    if filled < 0:
        filled = 0
    if filled > 16:
        filled = 16

    return filled

def make_bar(raw):
    filled = get_bar_count(raw)
    empty = 16 - filled
    return "O" * filled + "-" * empty

# -----------------------------
# Encoder handling
# -----------------------------
def update_encoder():
    global last_clk, selected, last_turn_time

    c = clk.value()

    # detect falling edge of CLK
    if last_clk == 1 and c == 0:
        now = ticks_ms()

        # small debounce
        if ticks_diff(now, last_turn_time) > 4:
            # toggle between MIN and MAX on each valid turn
            selected = 1 - selected
            last_turn_time = now

    last_clk = c

# -----------------------------
# Button handling
# -----------------------------
def check_button(raw):
    global last_button, last_press_time
    global min_level, max_level
    global flash_message, flash_until

    b = sw.value()

    # detect button press
    if last_button == 1 and b == 0:
        now = ticks_ms()

        # debounce button
        if ticks_diff(now, last_press_time) > 200:

            if selected == 0:
                # save new MIN
                min_level = raw

                # keep range valid
                if min_level >= max_level:
                    max_level = min_level + 1

                flash_message = pad16("MIN={}".format(min_level))

            else:
                # save new MAX
                max_level = raw

                # keep range valid
                if max_level <= min_level:
                    min_level = max_level - 1

                flash_message = pad16("MAX={}".format(max_level))

            flash_until = now + 800
            last_press_time = now

    last_button = b

# -----------------------------
# LED update
# -----------------------------
def update_led(raw):
    if raw < min_level or raw > max_level:
        led_b.value(1)
    else:
        led_b.value(0)

# -----------------------------
# LCD update
# -----------------------------
def update_lcd(raw):
    global flash_message, flash_until

    now = ticks_ms()

    # Line 1
    lcd.move_to(0, 0)
    if flash_message is not None and ticks_diff(flash_until, now) > 0:
        lcd.putstr(flash_message)
    else:
        flash_message = None
        lcd.putstr(make_bar(raw))

    # Line 2
    if selected == 0:
        line2 = pad16(">MIN:{:4d}".format(min_level))
    else:
        line2 = pad16(">MAX:{:4d}".format(max_level))

    lcd.move_to(0, 1)
    lcd.putstr(line2)

# -----------------------------
# Main loop
# -----------------------------
lcd.clear()

while True:
    raw = light_sensor.read()

    update_encoder()
    check_button(raw)
    update_led(raw)
    update_lcd(raw)

    sleep_ms(1)

        