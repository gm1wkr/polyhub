#!/usr/bin/python
__author__ = 'Michael Langley'

import json
import os
import piNetMQTT
import polyhubLCD as lcd
from w1thermsensor import W1ThermSensor

# MQTT Base topic
mqtt_topic = "/piNet/polyhub/temp/"
thisPi = os.uname()[1]
clientID = "ds18b20-{}".format(thisPi)
client = piNetMQTT.mqtt_connect(clientID)

sid = {}
sid['blue']  = '8000001fa78c'
sid['red']   = '04168440afff'
sid['green'] = '0516852dc9ff'
sid['lillies']   = '0416844073ff'
sid['int']   = '051684ba67ff'

def lcd_write(msg):
	#Output to LCD display
	lcd.writeLcd(msg)

def readAll():
	for sensor in W1ThermSensor.get_available_sensors():
		print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))


def readAllTemp():
	out = {}
	for name, sensor_id in sid.iteritems():
		try:
			sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, sensor_id)
			tc = sensor.get_temperature()
			out[name] = tc
		except :
			out[name] = 999.99
	return out


def getTempFrom(probe):
	sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, sid[probe])
	tc = sensor.get_temperature()
	return("{}: {:0.2f}".format(probe, tc)) 

def lcd_write(msg):
	#setupLCD()
	out = "{:^20}\n\r{}".format("** PROBES **", msg)
	lcd.writeLcdScreen(out)

def format_lcd():
	temps = readAllTemp()
	lcd_msg = ""

	for probe, temp in temps.iteritems():
		lcd_msg += "{:<8}: {:0.2f}C\n\r".format(probe, temp)

	return lcd_msg


def sendTemps():
	temps = readAllTemp()

	for probe, temp in temps.iteritems():
		topic = "{}{}".format(mqtt_topic, probe)
		msg = "{:0.2f}c".format(temp)

		piNetMQTT.mqttSendMsg(client, msg, topic, 1)

def sendTempJson():
	temps = readAllTemp()

	for probe, temp in temps.iteritems():
		d = {}
		d['temperature'] = "{:0.1f}".format(temp)
		j ={}
		j['machine'] = thisPi
		j['type'] = "sensor"
		j['sensor_name'] = probe
		j['data'] = d

		piNetMQTT.mqttSendMsg(client, json.dumps(j), "/piNet/polyhub", 1)




lcd_write(format_lcd())
#getTempFrom('water')
# sendTemps()
sendTempJson()
