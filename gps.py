import serial
from time import sleep
import re
import numpy as np
import math
ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
while True:
    received_data = ser.read()              #read serial port
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)
    sleep(1)
    my_list = received_data.decode("utf-8").split('$')
    print(np.mean([math.modf(float(item.split(',')[1])/100)[1] + math.modf(float(item.split(',')[1])/100)[0]*(100/60) for item in my_list if item.startswith('GNGLL')]))
    print(np.mean([math.modf(float(item.split(',')[3])/100)[1] + math.modf(float(item.split(',')[3])/100)[0]*(100/60) for item in my_list if item.startswith('GNGLL')]))