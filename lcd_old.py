#!/usr/bin/env python
# requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *

mylcd = RPi_I2C_driver.lcd()



def clearLCD():
	mylcd.lcd_clear()

def writeLcd(msg, row=2):
	mylcd.lcd_display_string_pos("PolyHub 0 PiNet", 1, 2)
	mylcd.lcd_display_string("{:^20}".format(msg), row)

def reset_lcd():
	#clearLCD()
	mylcd.lcd_display_string_pos("PolyHub 0 PiNet",1, 2)



