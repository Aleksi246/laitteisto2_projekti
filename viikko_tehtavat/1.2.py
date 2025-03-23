#1.2

import time
import fifo
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

data = []

def print_text(text):
    global data
    
    data.append(text)
    if len(data) > 6:
        data.pop(0)
    
    oled.fill(0)
    
    for index, word in enumerate(data):
        oled.text(word, 0, (index * 10), 1)
    
    oled.show()

while True:
    word = input("sana: ")
    print_text(word)
    