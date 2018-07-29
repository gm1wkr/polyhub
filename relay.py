#!/usr/bin/env python

"""relay.py: Relay control for Polyhub0 of PiNet Primary adjunct."""

__author__ = 'Michael Langley'
import os
import subprocess
import piNetMQTT
import time
import serial
import RPi.GPIO as GPIO
import polyhubLCD as lcd
from threading import Thread
from time import sleep

#Command Listener MQTT Topic
mqtt_cmd_topic = "/piNet/polyhub/cmd/relay"
mqtt_announce = "/piNet/polyhub"
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)



thisPi = os.uname()[1]
clientID = "relay-{}".format(thisPi)

mqtt_topic = "/piNet/{}/relay".format(thisPi)

# RELAY CONTROL
# 5, 6, 13, 16, 19, 20, 21, 26
relayPins = {}
relayPins['port1'] = 5
relayPins['port2'] = 6
relayPins['port3'] = 13
relayPins['port4'] = 19
relayPins['port5'] = 16
relayPins['port6'] = 20
relayPins['port7'] = 21
relayPins['port8'] = 26

def setupRelayGPIO():
	for pin in relayPins.values():
		#iterate list of pins (UNSORTED!), Set to OUT and Logic High (Relay Off)
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, True)
	return True

def button_callback(channel):
	turnOnForSeconds('port1', 6)

GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set GPIO 9 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(9,GPIO.BOTH,callback=button_callback, bouncetime=400)

def initRelays():
	allRelaysOff()
	turnOn({'port6', 'port8'})
	time.sleep(.3)
	turnOff(['port8'])

def relaySequenceOn():
	state = {}
	for name, pin in relayPins.iteritems():
		GPIO.output(pin, False)
		msg = '{} > ON ({})'.format(name, pin)
		#print(msg)
		client.publish(mqtt_topic, msg, 1, False)
		state[name] = 'ON'
		time.sleep(0.4)
	return state


def relaySequenceOff():
	state = {}
	for name, pin in relayPins.iteritems():
		GPIO.output(pin, True)
		msg = '{} > OFF ({})'.format(name, pin)
		#print(msg)
		mqttSend(msg)
		state[name] = 'OFF'
		time.sleep(0.4)
	return state


def turnOnForSeconds(device, seconds):
	myThread = Thread(target=timedRelay, args=(device, seconds,))
	myThread.start()


def timedRelay(device, seconds):
	lcd_write('Timed Event', msg2="{} for {}".format(device, seconds))
	turnOn([device])
	sleep(seconds)
	lcd_write('Timed Event END', msg2="{} now OFF".format(device))
	turnOff([device])



def turnOn(devices):
	state = {}
	for device in devices:
		if device in relayPins:
			GPIO.output(relayPins[device], False)
			state[device] = 'ON'			

	return


def turnOff(devices):
	state = {}
	for device in devices:
		if device in relayPins:
			GPIO.output(relayPins[device], True)
			state[device] = 'OFF'

	return


def allRelaysOff():
	for pin in relayPins.values():
		GPIO.output(pin, True)

	return 'All relays Off'


def allRelaysOn():
	for pin in relayPins.values():
		GPIO.output(pin, False)

	return 'All relays On'


def readPin(pin):
	res = os.popen('gpio -g read {}'.format(pin)).readline()
	res = res.replace("\n","")

	if res == "0":
		return "ON"
	return "OFF"


def statusAllRelays():
	for name, pin in relayPins.iteritems():
		relay_state = readPin(pin)
		msg = '{} is {}'.format(name, relay_state)
		mqttSend(msg)


def parseTopic(topic):
	topic = topic.split("/")
	topic = topic[1:]
	return(topic)


def parseMsg(msg):
	msg = msg.split(">")
	return msg


def mqttSend(msg):
	client.publish(mqtt_topic, msg, 2, False)


def setupLCD():
	lcd.clearLCD()
	lcd.cursor_pos = (0, 0)
	lcd.writeLcd("{:-^20}".format("RELAY CMD"))
	lcd.cursor_pos = (1, 0)


def lcd_write(msg, msg2=""):
	line1 = "{:-^20}".format("RELAY CMD")
 	line2 = "{:_^20}".format("12V Bus Zero")
 	line3 = msg
 	line4 = msg2
 	lcd.turnOnForSeconds()
	lcd.writeLcdScreen("{}\n\r{}\n\r{}\n\r{}".format(line1, line2, line3, line4))


def onMessage(client, userdata, message):
	msg = str(message.payload.decode("utf-8"))
	topic = message.topic
	topic_parts = parseTopic(message.topic)

	if topic == mqtt_cmd_topic:
		#print "here"
		msg = parseMsg(msg)
		#print(msg[0])

		if msg[0] == "RELAYRESET":
			res = subprocess.Popen('sudo /bin/systemctl restart piNet.service', shell=True)

		if msg[0] == "ALLOFF":
			allRelaysOff()
			mqttSend("ALLOFF")
			lcd_write("{:-^20}".format(" ALL RELAYS "), "{:*^20}".format("  OFF  "))

		if msg[0] == "ALLON":
			allRelaysOn()
			mqttSend("ALLON")
			lcd_write("{:-^20}".format(" ALL RELAYS "), "{:*^20}".format("  ON  "))

		

		if msg[0] == "STATUSALL":
			statusAllRelays()

		if msg[0] == "TESTSEQ":
			lcd_write(" TEST SEQUENCE ", "{:*^20}".format(" STARTING "))
			relaySequenceOn()
			relaySequenceOff()
			mqttSend("SEQ COMPLETE")
			lcd_write(" TEST SEQUENCE ", "{:*^20}".format(" COMPLETE "))

	if msg[0] in relayPins.keys():
		relay = msg[0]
		relay_state = readPin(relayPins[relay])
		command = msg[1]

		#print "for {} command {}".format(relay, command)

		if command == "status":
			#print (relay_state)
			msg = '{} is {}'.format(relay, relay_state)
			lcd_write(msg)
			mqttSend(msg)

		if command[:4] == "time":
			secs = float(command[4:])
			turnOnForSeconds(relay, secs)
			msg = "{} {} Secs".format(relay, secs)
			lcd_write(msg)
			mqttSend(msg)

		if command == "ON":
			if relay_state == "ON":
				msg = "{} already ON".format(relay)
				lcd_write(msg)
				mqttSend(msg)
			else:
				new_state = readPin(relayPins[relay])
				turnOn([relay])
				msg = "{} ON".format(relay)
				lcd_write(msg)
				mqttSend(msg)

		if command == "OFF":
			if relay_state == "OFF": 
				msg = "{} already OFF".format(relay)
				lcd_write(msg)
				mqttSend(msg)
			else:
				new_state = readPin(relayPins[relay])
				turnOff([relay])
				msg = "{} OFF".format(relay)
				lcd_write(msg)
				mqttSend(msg)


def loop():
	while True:
		subprocess.Popen('python /home/pi/piNet/ds18.py', shell=True)
		time.sleep(10)
		subprocess.Popen('python /home/pi/piNet/si7021.py', shell=True)
		mqttSend("Relay Network OK")
		time.sleep(10)

def main(client):
	try:
		setupRelayGPIO()
		initRelays()
		lcd_write("piNet Client ID: ", "{}".format(clientID))
		mqttSend("Relay CMD START")
		loop()
	finally:
		lcd_write("{:*^20}".format(" RELAY CMD STOPPED ! "))
		piNetMQTT.mqtt_disconnect(client)
		os._exit(0)



if __name__ == '__main__':
	client = piNetMQTT.mqtt_connect(clientID)
	client.on_message = onMessage
	client.subscribe(mqtt_cmd_topic)	
	main(client)

