#!/usr/bin/python
# add exception handling
# add logging to a file
# add timestamp ?
import os
import sys
import urllib.request, urllib.parse, urllib.error;
import time

def ultimatenotification(msg):
    try:
        msg = urllib.parse.quote(msg);
        a = 'https://www.ultimatenotifier.com/items/User/send/uber.koob/message=' + msg + '/password=fuckfacebook'
        #print a
        os.system("wget -nv -nc --no-check-certificate " + a)
        
        # crude rate-limiter
        time.sleep(1)

    except Exception as e:
        errMsg = "kojoney_ultimatenotification.py : ultimatenotification() exception caught = " + repr(e) + " msg=" + msg
        print("Exception : " + errMsg)
        syslog.syslog(errMsg)
                    
if __name__ == "__main__":
    msg = time.ctime() + " -> " + sys.argv[1]
    print("message to send : [" + msg + "]")
    ultimatenotification(msg)
    




