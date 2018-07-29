#!/usr/bin/env python
# requires RPi_I2C_driver.py


from RPLCD.i2c import CharLCD
from time import *
from threading import Thread

lcd = CharLCD(i2c_expander='PCF8574', address=0x3f, port=1,
              cols=20, rows=4, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=False)

lcd.cursor_mode = "hide"
lcd.write_string('CONTACTING THE BORG.')
lcd.cursor_pos = (2, 0)
lcd.write_string('UNIMATRIX ZERO')
lcd.cursor_pos = (3, 0)
lcd.write_string("{:^20}".format("PolyHub 0 Listening..."))

def turnOnForSeconds(seconds=5):
  backlightThread = Thread(target=timedBacklight, args=(seconds,))
  backlightThread.start()


def timedBacklight(seconds):
  lcd.backlight_enabled=True
  sleep(seconds)
  lcd.backlight_enabled=False

def clearLCD():
        turnOnForSeconds()
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("{:^20}".format("PolyHub 0 PiNet"))
        lcd.cursor_pos = (1, 0)


def writeLcd(msg):
        turnOnForSeconds()
        clearLCD()
        lcd.write_string("{:^20}".format(msg))


def writeLcdScreen(msg):
        turnOnForSeconds()
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("{}".format(msg))


