import micropython
from machine import Pin, ADC
from piotimer import Piotimer
from fifo import Fifo

#needed for reasons explained in slides
micropython.alloc_emergency_exception_buf(200)

#adc1 is pin 27 and adc0 is pin 26
heartratemonitorpin = Pin(27,Pin.IN)
heartadc = ADC(heartratemonitorpin)

debugpin = Pin(0, Pin.OUT)

fifo = Fifo(500)

#this function needs something in the bracket for strange reasons
def handler(nothing):
    data = heartadc.read_u16()
    fifo.put(data)
    debugpin.toggle()
    

#does callback every 4 ms or in 250 hz
timer = Piotimer(mode = Piotimer.PERIODIC,freq = 250, callback=handler)

#slidingaveragelist used in counting the average of 5 most resent datapoints
slidingaveragelist = []
slidingaverage = 0

#average liist and average used in comparing the currnet datapoint to average datapoint
averagelist =[]
average = 0

#counter used to keep track of datapoints between peaks. each datapoint is 4 ms so total time between peaks is (counter * 4ms)
counter = 0

#60 bpm => 1000 ms p2p,
#70 bpm => 859 ms p2p,
#80 bpm => 726 ms p2p
#240 bpm => 250 ms p2p
#hr = 60/p2p_ms/1000


while True:
    
    if fifo.has_data():
        
        data = fifo.get()
        slidingaveragelist.append(data)
        counter += 1
        
        
        if len(slidingaveragelist) == 5:
            
            slidingaverage = int((slidingaveragelist[0]+slidingaveragelist[1]+slidingaveragelist[2]+slidingaveragelist[3]+slidingaveragelist[4])/5)
            
            averagelist.append(slidingaverage)
            
            slidingaveragelist.pop(0)
        
        #print(slidingaverage)
        if len(averagelist) == 20:
            avsumma = 0
            for i in range(20):
                avsumma += averagelist[i]
                average = avsumma/20
            averagelist.pop(0)
        
        if slidingaverage > average + 1300 and counter > 60:
            
            print(counter*4)
            counter = 0
        
        
        
        
        
        
