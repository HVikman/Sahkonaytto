from uos import stat
import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
from machine import Pin, I2C 
import json
import time
import sh1106
import program
led4 = Pin(12, Pin.OUT)
button = Pin(17, Pin.IN, Pin.PULL_DOWN)

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
    "rounding":"",
    "limit":""
    }
    a_file = open("settings.json","w")
    json.dump(settings,a_file)
    a_file.close()
def connection():
    if len(settings['password'])>6:
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
            if(attempts > 59):
                wlansettings = open("settings.json","w")
                wlansettings.close()
                machine.reset()
        ip = wlan.ifconfig()[0]
        print(f'Connected on {ip}')
        
    else:
        ssid = "PicoW"
        password = "123456789"
        ap = network.WLAN(network.AP_IF)
        ap.config(essid=ssid, password=password) 
        ap.active(True)

        while ap.active == False:
            pass

        print("Access point active")
        print(ap.ifconfig())
        ip = ap.ifconfig()[0]
        print(f'Connected on {ip}')
            
    return ip


i2c = I2C(0,scl=Pin(1), sda=Pin(0), freq=400000)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(29), 0x3c,rotate=180)
ip = connection() 



if settings["updateonboot"]==1:
    connection() 
    r= urequests.get('https://raw.githubusercontent.com/HVikman/Sahkonaytto/main/version.json')
    info = r.json
    version = info['version']

    def getUpdate():
        display.sleep(False)
        display.fill(0)
        display.text('Updating...', 0, 0, 1)
        display.show()
        response = urequests.get("https://raw.githubusercontent.com/HVikman/Sahkonaytto/main/program.py")
        print(version+" "+settings["version"])
        if len(response.text) <100:
            print("Failed to get update")
            return False
        else:
            x = response.text
            response = urequests.get("https://raw.githubusercontent.com/HVikman/Sahkonaytto/main/program.py")
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
                
            
                response = urequests.get("https://raw.githubusercontent.com/HVikman/Sahkonaytto/main/webpages.py")            
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
else:
    print("no update")

    holdsec = 0
    while (button.value()==1):
        holdsec += 1
        led4.toggle()
        time.sleep(0.5)
        led4.toggle()
        time.sleep(0.5)
        if(holdsec==5):
            print("asetuksiin")
            program.settings(ip,settings)
    if(len(settings["password"]) > 0):
        program.main(button,settings)
    else:
        program.wlansettings(ip,settings)

