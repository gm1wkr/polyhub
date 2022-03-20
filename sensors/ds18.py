#!/usr/bin/env python3

import json
import os
from w1thermsensor import W1ThermSensor
import time

# Sensor hardware ID
sid = {}
sid['blue']  = '8000001fa78c'
sid['red']   = '04168440afff'
sid['green'] = '0516852dc9ff'
sid['yellow']   = '0416844073ff'
sid['enclosure']   = '051684ba67ff'


reverseSid = {}
reverseSid['8000001fa78c']  = 'blue'
reverseSid['04168440afff']   = 'red'
reverseSid['0516852dc9ff'] = 'green'
reverseSid['0416844073ff']   = 'yellow'
reverseSid['051684ba67ff']   = 'enclosure'


def readAllTemp():
    out = {}
    for name, sensor_id in sid.items():
        try:
            sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, sensor_id)
            tc = sensor.get_temperature()
            out[name] = tc
        except :
            out[name] = 9999.99
    return out

def sendJson():
    
    j ={}
    return readAllTemp()
    # return(json.dumps(j))


def getData():
    out = {}
    for sensor in W1ThermSensor.get_available_sensors():
        # print("Sensor {} has temperature {:.2f}".format(reverseSid[sensor.id], sensor.get_temperature()))
        tempC = sensor.get_temperature()
        out[reverseSid[sensor.id]] = "{0:.2f}".format(tempC)
        # out[reverseSid[sensor.id]] = f"{tempC:.2f}"

    return out






if __name__ == "__main__":
    print(getData()) 