from threading import Lock
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import random
import serial
from time import sleep
import re
import numpy as np
import math
import sys
import time
import board
from adafruit_lsm6ds.lsm6ds33 import LSM6DS33
import os

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread2 = None
thread_lock = Lock()

def read_accelerometer_data():
    i2c = board.I2C()
    sensor = LSM6DS33(i2c)
    """Example of how to send server generated events to clients."""
    while True:
        acc = [round(sensor.acceleration[0]/9.81,2), round(sensor.acceleration[1]/9.81,2), round(sensor.acceleration[2]/9.81,2)]
        socketio.emit('acc_data',
                      {'acc': acc})
        socketio.sleep(0.05)


def read_gps_data():
    """Example of how to send server generated events to clients."""
    # while True:
    #     socketio.sleep(2)
    #     print('data')
    #     num = random.randint(0, 10)
    #     socketio.emit('gps_data',
    #                   {'data': num})
    ser = serial.Serial("/dev/ttyS0", 9600)  # Open port with baud rate
    last_lat = 0
    last_lon = 0
    while True:
        received_data = ser.read()  # read serial port
        data_left = ser.inWaiting()  # check for remaining byte
        received_data += ser.read(data_left)
        my_list = received_data.decode("utf-8").split('$')
        try:
            lat = np.mean(
                [math.modf(float(item.split(',')[1]) / 100)[1] + math.modf(float(item.split(',')[1]) / 100)[0] * (100 / 60)
                for item in my_list if item.startswith('GNGLL')])
            last_lat = lat
        except:
            lat = last_lat
        try:
            lon = np.mean(
                [math.modf(float(item.split(',')[3]) / 100)[1] + math.modf(float(item.split(',')[3]) / 100)[0] * (100 / 60)
                 for item in my_list if item.startswith('GNGLL')])
            last_lon = lon
        except:
            lon = last_lon
        if (not np.isnan(lat)) and (not np.isnan(lon)):
            try:
                socketio.emit('gps_data', {'cords': [lat,lon]})
            except:
                print('Could not emit')
        print(lat, lon)
        socketio.sleep(1)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.event
def connect():
    global thread, thread2
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(read_accelerometer_data)
        if thread2 is None:
            thread2 = socketio.start_background_task(read_gps_data)
    emit('acc_data', {'data': 'Connected'})
    emit('gps_data', {'data': 'Connected'})


if __name__ == '__main__':
    socketio.run(app, host=str(sys.argv[1]))
