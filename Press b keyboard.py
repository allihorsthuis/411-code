from hid_services import Keyboard
from machine import Pinbb
import time

button = Pin(14, Pin.IN, Pin.PULL_UP)
ab = Keyboard('allikeyboard')
ab.start()
ab.start_advertising()


codes = {'b': 0x05}

while True:
    ab.set_keys(0x05) #set keys
    ab.notify_hid_report() #press
    time.sleep(0.05)
    ab.set_keys()
    ab.notify_hid_report()
    time.sleep(1)






