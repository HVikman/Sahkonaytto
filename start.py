from uos import stat
import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
from machine import Pin, I2C 
import json
import time
import sh1106
from program import main

global settings
try:
    if(stat("settings.json")):
        a_file = open("settings.json", "r")
        settings = json.load(a_file)
        a_file.close()
        print(settings)
except OSError:
    settings ={
    "ssid":"",
    "password":"",
    "version":"",
    "updateonboot":"",
    "rounding":""
    }
    a_file = open("settings.json","w")
    json.dump(settings,a_file)
    a_file.close()

i2c = I2C(0,scl=Pin(1), sda=Pin(0), freq=400000)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(29), 0x3c,rotate=180)




if settings["updateonboot"]==1:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    attempts=0
    wlan.connect(settings["ssid"], settings["password"])
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        display.sleep(False)
        display.fill(0)
        display.text('Connecting...', 0, 0, 1)
        display.show()
        time.sleep(1)
        attempts += 1
        if(attempts > 29):
            wlansettings = open("settings.json","w")
            wlansettings.close()
            machine.reset()
            
    r = urequests.get("http://api.henkka.one/prices.json")
    info = r.json()
    version = info['version']

    def getUpdate():
        display.sleep(False)
        display.fill(0)
        display.text('Updating...', 0, 0, 1)
        display.show()
        response = urequests.get("http://api.henkka.one/getupdate.php?file=program.py")
        print(version+" "+settings["version"])
        if len(response.text) <100:
            print("Failed to get update")
            return False
        else:
            x = response.text
            response = urequests.get("http://api.henkka.one/getupdate.php?file=program.py")
            if response.text == x:
                f = open("program.py","w")
                f.write(response.text)
                f.flush()
                f.close
                settings["version"] = version
                settings["updateonboot"] = 0
                a_file = open("settings.json","w")
                json.dump(settings,a_file)
                a_file.close()
                print("Updated program")
                
            
                response = urequests.get("http://api.henkka.one/getupdate.php?file=webpages.py")            
                if len(response.text) <100:
                    print("Failed to get update")
                    return False
                else:
                    f = open("webpages.py","w")
                    f.write(response.text)
                    f.flush()
                    f.close
                return True
            else:
                return False


    if(version == settings["version"]):
        print("same version")

    else:
        while getUpdate() == False:
            getUpdate()
            time.sleep(0.5)
elif settings["updateonboot"]==0:
    print("no update")
    main()
