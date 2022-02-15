# **sw_gps**

## **Packages**

```
pip install flask
pip install flask-socketio
pip install adafruit-circuitpython-lsm6ds
pip install pyserial
pip install numpy
pip install smbus2
pip install eventlet
```

## **Additional configuration**

### **Enable serial and I2C**

```
sudo raspi-config
```

Go to Interface Options -> Serial Port -> Select No -> Select Yes -> OK


Go to Interface Options -> I2C -> Select Yes -> OK

```
sudo reboot
```
