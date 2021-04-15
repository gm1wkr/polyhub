

import time
import datetime


gmtm = time.localtime()


def getNow():
    return time.time()


def secondsSince(seconds):
    return getNow() - seconds


def dateStr2Ts(dateStr):
    """YYY-MM-DD HH:MM:SS to Timestamp"""
    timestamp = time.mktime(time.strptime(dateStr, '%Y-%m-%d %H:%M:%S'))
    return timestamp


# Date Time Functions
def randSec(x=3, y=6):
    return random.randrange(x, y)


def sec2Deci(sec):
    "return 10 of MilliSecs"
    return sec / float(10)


def ts2date(ts):
    return datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')


def str2tpl(str):
    return time.strptime(str, "%Y-%m-%d %H:%M:%S")


def tpl2ts(tpl):
    return int(time.mktime(tpl))


def expStr2dateStr(ex_str):
    c_dow = time.strftime("%a", gmtm)
    c_year = time.strftime("%Y", gmtm)
    c_mon = time.strftime("%m", gmtm)
    c_day = time.strftime("%d", gmtm)
    ex_h = ex_str[0:2]
    ex_m = ex_str[2:4]
    ex_dom = ex_str[4:6]
    exp = '{0}-{1}-{2} {3}:{4}:00'.format(c_year, c_mon, ex_dom, ex_h, ex_m)
    return exp


def seconds2HMS(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return "%dh %02dm %02ds" % (h, m, s)


# Expiration Check Fn
def isCurrent(expires):
    expire_time = expires[0:4]
    expire_dom = expires[4:6]

    c_dom = datetime.datetime.now().strftime("%d")
    c_mon = datetime.datetime.now().strftime("%b")
    c_tod = datetime.datetime.now().strftime("%H%M")

    if expire_dom >= c_dom:
        if expire_time >= c_tod:
            return True
    else:
        return False


def inForce(validFrom, expires, now):
    "Within Time Range?  Unix TS"
    start = False
    expired = False

    if now >= validFrom:
        started = True
    else:
        return False

    if now >= expires:
        expired = True
    else:
        expired = False

    if started == True and expired == True:
        return False

    if started and expired == False:
        return True
    else:
        return False
