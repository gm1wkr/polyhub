#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test for si7021 Temp /RH sensor I2C"""

import os
import smbus
import time
import piNetMQTT
import polyhubLCD as lcd

# MQTT Base topic
mqtt_topic = "/piNet/polyhub/air/"
thisPi = os.uname()[1]
clientID = "si7120-{}".format(thisPi)
client = piNetMQTT.mqtt_connect(clientID)
#degC = (unichr(223) + 'C')


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
    out['cTemp'] = cTemp
    out['humidity'] = humidity

    return out

def lcd_write(data):
    line1 = "{:-^20}".format("AIR SENSOR")
    line2 = "{:_^20}".format("Si7021")
    line3 = "Temp    : {:0.2f}C".format(data['cTemp'])
    line4 = "Humidity: {:0.2f}%".format(data['humidity'])

    lcd.writeLcdScreen("{}\n\r{}\n\r{}\n\r{}".format(line1, line2, line3, line4))
    return True

def sendMQTT(data):
    temp = "{:0.1f}c".format(data['cTemp'])
    topic = "{}temperature".format(mqtt_topic)
    piNetMQTT.mqttSendMsg(client, temp, topic, 1)

    rh = "{:0.1f}%".format(data['humidity'])
    topic = "{}humidity".format(mqtt_topic)
    piNetMQTT.mqttSendMsg(client, rh, topic, 1)

    return True




if __name__ == '__main__':
    data = getTempRh()
    lcd_write(data)
    sendMQTT(data)
    print("{:0.2f}".format(data['cTemp']))
    print("{:0.2f}".format(data['humidity']))
