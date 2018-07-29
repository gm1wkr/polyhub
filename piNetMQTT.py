#!/usr/bin/env python

__author__ = 'Michael Langley'

"""
Common functions for PiNet
"""

import paho.mqtt.client as mqtt
from ConfigParser import SafeConfigParser

#Config
config = SafeConfigParser()
config.read('/home/pi/piNet/config/config.ini')
broker = config.get('mqtt', 'broker')
base_topic = config.get("mqtt", "baseTopic")

## MQTT Functions

def mqtt_connect(clientID):
    client = mqtt.Client(clientID)
    client.on_connect = onConnect
    client.username_pw_set(config.get('mqtt', 'username'), config.get('mqtt', 'password'))
    client.connect(broker)
    client.loop_start()
    return client

def mqtt_disconnect(client):
    client.disconnect()
    client.loop_stop()

def onConnect(client, userdata, flags, rc):
    m = "Flags {}.  Code: {}.  Client: {}".format(str(flags), str(rc), str(client))
    return (m)

def mqttSendMsg(client, msg, topic, qos):
	client.publish(topic, msg, qos, False)
