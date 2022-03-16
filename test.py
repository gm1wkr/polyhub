#!/usr/bin/env python

"""relay.py: Relay control for Polyhub0 of PiNet Primary adjunct."""

__author__ = 'Michael Langley'
import os
from time import sleep
import RPi.GPIO as GPIO

def button_callback(channel):
	print("Button was pushed!")
	sleep(4)
	print("Launching Nukes")


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 
GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set GPIO 9 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(9,GPIO.BOTH,callback=button_callback, bouncetime=200)



i = 0
while True:
	print("Iteration: {}".format(i))
	i += 1
	sleep(2)