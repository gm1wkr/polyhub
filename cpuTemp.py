#!/usr/bin/env python

"""cpuTemp.py: Read Raspberry Pi CPU TEmp and report to MQTT Broker."""

__author__ = 'Michael Langley'

import os
import piNetMQTT

thisPi = os.uname()[1]
mqtt_topic = "/piNet/{}/cputemp".format(thisPi)

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    res = res.replace("temp=","").replace("\n","")
    res = res[0:4]
    return(res)

def main(client):
    msg = "{}".format(getCPUtemperature())
    client.publish(mqtt_topic, msg, 1, False)


if __name__ == '__main__':

    client = piNetMQTT.mqtt_connect(thisPi)
    main(client)
    piNetMQTT.mqtt_disconnect(client)

    os._exit(0)
