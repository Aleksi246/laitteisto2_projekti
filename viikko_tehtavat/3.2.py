from machine import Pin ,PWM, UART, I2C, Timer, ADC
from fifo import Fifo
from led import Led
from ssd1306 import SSD1306_I2C
import time

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)

oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

#kopioin Led luokan tähän koska tein siihen pieniä muutoksia
# tee uudestaan periytymisellä super init

class Ledi(Led):
    def __init__(self, pin, name, mode = Pin.OUT, brightness = 1, value = None):
        super().__init__(pin, mode = Pin.OUT, brightness = 1, value = None)
        
        self.name = name
        self.texsti = name
    
    def ledtext(self):
        if self.value() == 0:
            self.texsti = self.name + " OFF"
        else:
            self.texsti = self.name + " ON"

class Encoder:
    
    def __init__(self, rot_a, rot_b, button):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.button = Pin(button, Pin.IN, Pin.PULL_UP)
        self.fifo = Fifo(30, typecode = 'i')
        self.button.irq(handler = self.handler2, trigger = Pin.IRQ_FALLING, hard = True)
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        self.start = time.ticks_ms()
        self.end = time.ticks_ms()
        
    def handler(self, pin):
        if self.button.value():
            if self.b():
                self.fifo.put(-1)
            else:
                self.fifo.put(1)
            
    def handler2(self, pin):
        self.start = time.ticks_ms()
        
    
        if not self.button() and time.ticks_diff(self.start,self.end) > 200:
            self.fifo.put(0)
            self.end = time.ticks_ms()
            


rot = Encoder(10, 11,12)


encodersum = 0
chosenmenuitem = 0

data = None
led1 = Ledi(22,"LED1")
led2 = Ledi(21,"LED2")
led3 = Ledi(20,"LED3")

while True:
    oled.fill(0)
    
    led1.ledtext()
    led2.ledtext()
    led3.ledtext()
    
    if chosenmenuitem == 0:
        oled.text(">"+led1.texsti,0,0,1)
        oled.text(" "+led2.texsti,0,7,1)
        oled.text(" "+led3.texsti,0,13,1)
    if chosenmenuitem == 1:
        oled.text(" "+led1.texsti,0,0,1)
        oled.text(">"+led2.texsti,0,7,1)
        oled.text(" "+led3.texsti,0,13,1)
    if chosenmenuitem == 2:
        oled.text(" "+led1.texsti,0,0,1)
        oled.text(" "+led2.texsti,0,7,1)
        oled.text(">"+led3.texsti,0,13,1)
    
    if rot.fifo.has_data():
        
        data = rot.fifo.get()
        
        encodersum += data
        
    if data == 0:
            if chosenmenuitem == 0:
                led1.toggle()
            if chosenmenuitem == 1:
                led2.toggle()
            if chosenmenuitem == 2:
                led3.toggle()
            data = None
        
    if encodersum == 2:
            
        chosenmenuitem -= 1
        encodersum = 0
        if chosenmenuitem == -1:
            chosenmenuitem = 2
            
    if encodersum == -2:
            
        chosenmenuitem += 1
        encodersum = 0
        if chosenmenuitem == 3:
            chosenmenuitem = 0
        
    oled.show()     
