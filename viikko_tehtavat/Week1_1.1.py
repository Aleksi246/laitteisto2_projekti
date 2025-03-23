import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

button0 = Pin(9, Pin.IN, Pin.PULL_UP)
button2 = Pin(7, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

ufo = '<=>'
x = int((oled.width / 2) - (len(ufo) * 4))
y = oled.height - 8


while True:
    oled.fill(0)
    oled.text(ufo ,x , y, 1)
    oled.show()
    if button0.value() == 0:
        x += 1
        if x + (len(ufo) * 8) > oled_width:
            x = oled.width - (len(ufo) * 8)
    elif button2.value() == 0:
        x -= 1
        if x < 0:
            x = 0
    