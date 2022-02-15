import time
import board
from adafruit_lsm6ds.lsm6ds33 import LSM6DS33
import os

i2c = board.I2C()
sensor = LSM6DS33(i2c)

while True:
        print("acc: x = {:.2f}, y = {:.2f}, z = {:.2f} ".format(sensor.acceleration[0]/9.81, sensor.acceleration[1]/9.81, sensor.acceleration[2]/9.81), end='\r')
        time.sleep(0.1)