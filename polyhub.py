#!/usr/bin/env python

"""Simplified 
2022 - All Relay control off loaded  

"""

__author__ = 'Michael Langley'
import json
import os
import subprocess
import piNetMQTT
import time
import polyhubLCD as lcd
from threading import Thread
from sensors import ds18
from sensors import si7021
from sensors import cpu



#Command Listener MQTT Topic
mqtt_cmd_topic = "/piNet/polyhub/cmd/relay"
mqtt_announce = "/piNet/polyhub"



thisPi = os.uname()[1]
clientID = "relay-{}".format(thisPi)

mqtt_topic = "/piNet/{}/".format(thisPi)


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
    # lcd.writeLcd("{:-^20}".format("RELAY CMD"))
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
        
        msg = parseMsg(msg)

        


def main(client):
    # try:
        
    #     lcd_write("piNet Client ID: ", "{}".format(clientID))
    #     mqttSend("Sensors STARTED")
        last_cpu = 0
        interval_cpu = 30
        last_ds18 = 0
        interval_ds18 = 20
        last_si7021 = 0
        interval_si7021 = 30

        
        while True:

            time.sleep(1)
            now = int(time.time())
            time.sleep(1)
            j = {}
            j['machine'] = thisPi
            j['epoch'] = now

            if now >= (last_cpu + interval_cpu):
                last_cpu = now
                j['type'] = "cpu"
                j['data'] = cpu.getData()
                mqttSend(json.dumps(j))

            if now >= (last_ds18 + interval_ds18):
                last_ds18 = now
                j['type'] = "sensor"
                data = ds18.sendJson()

                for sensor, value in data.items():
                    j['sensor_name'] = "ph-probes-{}".format(sensor)
                    j['data'] = {'temperature': value}
                    mqttSend(json.dumps(j))

            if now >= (last_si7021 + interval_si7021):

                last_si7021 = now
                j['type'] = "sensor"
                data = si7021.getTempRh()

                for sensor, value in data.items():
                    j['sensor_name'] = "ph-{}".format(sensor)
                    j['data'] = {sensor: value}
                    mqttSend(json.dumps(j))



            j.clear()
    # finally:
    #     lcd_write("{:*^20}".format(" RELAY CMD STOPPED ! "))
    #     piNetMQTT.mqtt_disconnect(client)
    #     os._exit(0)



if __name__ == '__main__':
    client = piNetMQTT.mqtt_connect(clientID)
    client.on_message = onMessage
    client.subscribe(mqtt_cmd_topic)	
    main(client)

