#!/usr/bin/env python3

"""
cpu.py 2022
Return dictonary to controller.
E.g., 
{
    {
    "cpuType": "Pi 3 Model B (Sony)", 
    "uptime": 122391, 
    "loadAvg": {"L15": "0.02", "L5": "0.03", "L1": "0.00"}, 
    "users": "1", 
    "cpuTemp": "19.3"
    }
}
"""

__author__ = 'Mike Langley'

import os
import platform
import json

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
    rev = "0000"
    try:
        # f = open('/proc/cpuinfo', 'r')
        with open("/proc/cpuinfo") as f:
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



def getUptime():
    with open("/proc/uptime") as f:
        data = f.read()
        uptime = data.split(" ")
        uptime = uptime[0].split(".")

        return int(uptime[0])


def getData():
    dOut = {}
    dOut['hostname'] = platform.uname()[1]
    dOut['cpuTemp'] = getCPUtemperature()
    dOut['cpuType'] = dRev[getCPUrevision()]
    dOut['users'] = getUserCount()
    dOut['uptime'] = getUptime()
    dOut['loadAvg'] = getLoadAverages()

    return(dOut)




if __name__ == '__main__':
    print(json.dumps(getData()))
