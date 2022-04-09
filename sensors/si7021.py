#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test for si7021 Temp /RH sensor I2C"""

import smbus
import time
import json


def getTempRh():

    # Get I2C bus
    bus = smbus.SMBus(1)

    # SI7021 address, 0x40(64)
    #		0xF5(245)	Select Relative Humidity NO HOLD master mode
    bus.write_byte(0x40, 0xF5)

    time.sleep(0.15)

    # SI7021 address, 0x40(64)
    # Read data back, 2 bytes, Humidity MSB first
    data0 = bus.read_byte(0x40)
    data1 = bus.read_byte(0x40)

    # Convert the data
    humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6

    time.sleep(0.15)

    # SI7021 address, 0x40(64)
    #		0xF3(243)	Select temperature NO HOLD master mode
    bus.write_byte(0x40, 0xF3)

    time.sleep(0.15)

    # SI7021 address, 0x40(64)
    # Read data back, 2 bytes, Temperature MSB first
    data0 = bus.read_byte(0x40)
    data1 = bus.read_byte(0x40)

    # Convert the data
    cTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85

    out = {}
    out['air-temperature'] = "{:0.2f}".format(cTemp)
    out['humidity'] = "{:0.2f}".format(humidity)

    return out





if __name__ == '__main__':
    
    
    print(json.dumps(getTempRh()))
