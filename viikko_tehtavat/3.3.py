import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
from fifo import Fifo
from filefifo import Filefifo
import framebuf

#Change this data
#data to read
data = Filefifo(10, name = 'capture_250Hz_01.txt')
#how many data points is taken from "data"
sample_amount = 1000
#how many pixel is moved every time
scroll_distance = 16


#rotater class
class Encoder:
    def __init__ (self, rot_a, rot_b):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.fifo = Fifo(50, typecode = 'i')
        self.a.irq(handler = self.handler, trigger =Pin.IRQ_RISING, hard = True)

    def handler(self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)

#Rotator (pinA, pinB)
rot = Encoder(10, 11)

#OLED
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

#Make empty list and setup framebuffer
lista = []

buffer = bytearray(sample_amount * oled_height // 8)
fb = framebuf.FrameBuffer(buffer, sample_amount, oled_height, framebuf.MONO_HLSB)


#Go trough data and find min and max values.
for _ in range(sample_amount):
    lista.append(data.get())

max_val = max(lista)
min_val = min(lista)

scale = (oled_height / (max_val - min_val))

#draw the line in to framebuffer
x = 0
n = 0
for _ in range(sample_amount):
        y = int(scale * (lista[n] - min_val))
        fb.pixel(x, y, 1)
        x += 1
        n += 1


#Main procram
offset = 0

oled.fill(0)
oled.blit(fb, -offset, 0)
oled.show()

while True:
             
    if rot.fifo.has_data():
        offset += rot.fifo.get() * scroll_distance
        if offset < 0:
            offset = 0
        elif offset > sample_amount - oled.width:
            offset = sample_amount - oled.width
        
        oled.fill(0)
        oled.blit(fb, -offset, 0)
        oled.show()
