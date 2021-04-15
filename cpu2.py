#!/usr/bin/env python

"""
cpuTemp.py: Read Raspberry Pi CPU TEmp and report to MQTT Broker.
Version 2.0.1  Include hostname and load averages as JSON.
E.g., 
{
    "uptime": "1828270",  # SECONDS 
    "users": "1",
    "loadAvg": {
        "L15": "0.00",
        "L5": "0.00",
        "L1": "0.00"
    },
    "cpuTemp": "42.9",
    "device": "nexus",
    "cpuType": "Pi 3 Model B (Sony)"
}
"""

__author__ = 'Mike Langley'

import os
import platform
import json
import piNetMQTT
import piNetDate

thisPi = platform.uname()[1]
mqtt_topic = "/piNet/{}/system".format(thisPi)

dRev = {}
dRev['0002'] = "Pi B Rev 1"
dRev['0003'] = "Pi B Rev 1"
dRev['0004'] = "Pi B Rev 2"
dRev['0005'] = "Pi B Rev 2"
dRev['0006'] = "Pi B Rev 2"
dRev['0007'] = "Pi A"
dRev['0008'] = "Pi A"
dRev['0009'] = "Pi A"
dRev['000d'] = "Pi B Rev 2"
dRev['000e'] = "Pi B Rev 2"
dRev['000f'] = "Pi B Rev 2"
dRev['0010'] = "Pi B+"
dRev['0013'] = "Pi B+"
dRev['900032'] = "Pi B+"
dRev['0011'] = "Pi Compute Module"
dRev['0014'] = "Pi Compute Module"
dRev['0012'] = "Pi A+"
dRev['0015'] = "Pi A+"
dRev['a01041'] = "Pi 2 Model B V1.1 (Sony)"
dRev['a21041'] = "Pi 2 Model B V1.1 (Embest)"
dRev['a22042'] = "Pi 2 Model B V1.2"
dRev['900092'] = "Pi Zero v1.2"
dRev['900093'] = "Pi Zero v1.3"
dRev['9000C1'] = "Pi Zero W"
dRev['a02082'] = "Pi 3 Model B (Sony)"
dRev['a22082'] = "Pi 3 Model B (Embest)"
dRev['a020d3'] = "Pi 3 Model B+ (Sony)"
dRev['a03111'] = "Pi 4B (1GB)"
dRev['b03111'] = "Pi 4B (2GB)"
dRev['c03111'] = "Pi 4B (4GB)"



def getCPUrevision():
    # Read rPi /proc/cpu info & return poc type
    rev = "0000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:8] == 'Revision':
                rev = line[11:len(line)-1]
        f.close()
    except:
        rev = "0000"  # error

    return rev


def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    res = res.replace("temp=", "").replace("\n", "")
    res = res[0:4]

    return(res)


def getUptimeLoads():
    res = os.popen('uptime').readline()
    res = res.split(",")
    upDays = res[0]
    upDays = res[0].split("up")
    upDays = upDays[1]
    upDays = upDays.replace(" days", "").strip()
    upHours = res[1].strip()
    upHours = upHours.split(":")
    upTime = "{}d{}h{}m".format(upDays, upHours[0], upHours[1])
    users = res[2].replace(" user", "").strip()
    loadAv = res[3].split(":")
    loadAv = loadAv[1]
    L1 = res[3].split(":")
    dLoad = {"L1": L1[1].strip(), "L5": res[4].strip(), "L15": res[5].strip()}
    dOut = {"uptime": upTime, "users": users, "loadAvg": dLoad}

    return dOut

def getUserCount():
    res = os.popen('uptime').readline()
    res = res.split(",")
    users = res[2].replace(" user", "").strip()
    
    return users

def getLoadAverages():
    res = os.popen('w').readlines()
    loads = res[0].split('average:')
    loads = loads[1].replace(",", "").strip()
    la = loads.split(" ")
    dLoad = {"L1":la[0], "L5": la[1], "L15": la[2]}


    return dLoad

def secondsUptime():
    res = os.popen("uptime -s").readline()

    return res.strip()


def main(client):
    dOut = {}
    dOut['device'] = thisPi
    dOut['cpuTemp'] = getCPUtemperature()
    dOut['cpuType'] = dRev[getCPUrevision()]
    dOut['users'] = getUserCount()
    dOut['uptime'] = int(piNetDate.secondsSince(piNetDate.dateStr2Ts(secondsUptime())))
    dOut['loadAvg'] = getLoadAverages()

    j = {}
    j['machine'] = thisPi
    j['type'] = "cpu"
    j['data'] = dOut

    client.publish(mqtt_topic, json.dumps(j), 1, False)
    print(json.dumps(j, indent=4, sort_keys=False))


if __name__ == '__main__':
    client = piNetMQTT.mqtt_connect(thisPi)
    main(client)
    piNetMQTT.mqtt_disconnect(client)
    os._exit(0)
