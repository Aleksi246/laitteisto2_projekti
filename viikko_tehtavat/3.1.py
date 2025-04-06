from machine import Pin, PWM
from fifo import Fifo
import time

led_state = False

class Encoder:
    def __init__(self, rotary_right, rotary_left):
        self.right = Pin(rotary_right, mode = Pin.IN, pull = Pin.PULL_UP)
        self.left = Pin(rotary_left, mode = Pin.IN, pull = Pin.PULL_UP)
        self.fifo = Fifo(5, typecode = 'i')
        self.right.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        
    def handler(self, pin):
        #vaihtoehtoisesti getataan väkisin jotta led off -tilan data ei jää pööpöilemään, mutta hyi vittu t. mä
        #tai käydään sörkkimässä fifon koodia ja lisätään joku drop() tjsp
        #tailin voi toki täältäkin asettaa, jätin varuuksi tuonne pohjalle koodin kommentoituna ulos
        if self.left() and led_state:
            self.fifo.put(-1)
        elif led_state:
            self.fifo.put(1)
            
rotary = Encoder(10, 11)

button = Pin(12, mode = Pin.IN, pull = Pin.PULL_UP)
last_time = time.ticks_ms()
bounce_time = 300

led = PWM(Pin(20))
led.duty_u16(0)
led_brightness = 0
led.freq(1000)

def brightness_logic(rotary_value):
    global led_brightness
    steps = 10
    min_value = 0
    max_value = int(65535 * 0.30)
    change = max_value / steps
    
    led_brightness += int(rotary_value * change)
    led_brightness = max(min_value, min(max_value, led_brightness))
    led.duty_u16(led_brightness)

    print(led.duty_u16())

while True:
    current_time = time.ticks_ms()

    if (current_time - last_time) > bounce_time and button() == 0:
        last_time = current_time
        led_state = not led_state
    if led_state:
        if rotary.fifo.has_data(): brightness_logic(rotary.fifo.get())
        led.duty_u16(led_brightness)
    else:
        led.duty_u16(0)
        #if rotary.fifo.has_data():
        #    rotary.fifo.tail = (rotary.fifo.tail + 1) % rotary.fifo.size
    
    time.sleep(0.01)