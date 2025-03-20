import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

buttonsw2 = Pin(7, Pin.IN, Pin.PULL_UP)
buttonsw1 = Pin(8, Pin.IN, Pin.PULL_UP)
buttonsw0 = Pin(9, Pin.IN, Pin.PULL_UP)

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)

oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

#seuraavat muutujat x ja y määräävät mistä piirrettävä linja alkaa
x = 0
y = 32

while True:
    
    
    if x == 128:
        x = 0
    
    if buttonsw0() == 0:
        y += 1
        if y == 64:
            #jos haluaa että piirros jatkuu vastakkaiselta puolelta näyttöä
            #pitää tähän vaihtaa arvoksi 0 ja buttonsw2 if lauseeseen arvoksi 63
            y = 63
            

    if buttonsw1() == 0:
        oled.fill(0)
        oled.show()
        x = 0
        y = 32
    
    if buttonsw2() == 0:
        y -= 1
        if y == -1:
            y = 0
    
    oled.pixel(x,y,1)
    oled.show()
    x += 1
