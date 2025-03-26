#2.2

from filefifo import Filefifo

data = Filefifo(10, name = 'capture_250Hz_01.txt')

def find_min_max(seconds):
    list = []
    for _ in range(seconds / 0.25 * 250):
        value = data.get()
        list.append(value)

    return min(list), max(list)
    
def scale_and_print(seconds, min_value, max_value):
    for _ in range(seconds / 0.25 * 250):
        value = data.get()
        scaled_value = ((value - min_value) / (max_value - min_value)) * 100
        print(scaled_value)

seconds = 2
min_value, max_value = find_min_max(seconds)
seconds = 10
scale_and_print(seconds, min_value, max_value)