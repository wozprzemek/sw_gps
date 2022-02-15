from threading import Lock
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import random
import serial
from time import sleep
import re
import numpy as np
import math

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
    """Example of how to send server generated events to clients."""
    while True:
        socketio.sleep(0.1)
        num = random.randint(0, 10)
        socketio.emit('acc_data',
                      {'data': num})


def read_gps_data():
    """Example of how to send server generated events to clients."""
    # while True:
    #     socketio.sleep(2)
    #     print('data')
    #     num = random.randint(0, 10)
    #     socketio.emit('gps_data',
    #                   {'data': num})
    ser = serial.Serial("/dev/ttyS0", 9600)  # Open port with baud rate
    while True:
        received_data = ser.read()  # read serial port
        data_left = ser.inWaiting()  # check for remaining byte
        received_data += ser.read(data_left)
        socketio.sleep(1)
        my_list = received_data.decode("utf-8").split('$')
        lat = np.mean(
            [math.modf(float(item.split(',')[1]) / 100)[1] + math.modf(float(item.split(',')[1]) / 100)[0] * (100 / 60)
                         for item in my_list if item.startswith('GNGLL')])
        lon = np.mean(
            [math.modf(float(item.split(',')[3]) / 100)[1] + math.modf(float(item.split(',')[3]) / 100)[0] * (100 / 60)
             for item in my_list if item.startswith('GNGLL')])
        socketio.emit('gps_data', {'lat': lat}, {'lon': lon})


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
    socketio.run(app, host='192.168.4.1')