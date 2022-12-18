#0.0.1¤
from uos import stat
import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
from machine import Pin, I2C 
import json
import time
import sh1106


led1 = Pin(9, Pin.OUT)
led2 = Pin(10, Pin.OUT)
led3 = Pin(11, Pin.OUT)
led4 = Pin(12, Pin.OUT)
led5 = Pin(13, Pin.OUT)
led6 = Pin(14, Pin.OUT)
led7 = Pin(15, Pin.OUT)
global settings
settingsmode=False
button = Pin(17, Pin.IN, Pin.PULL_DOWN)
holdsec = 0
i2c = I2C(0,scl=Pin(1), sda=Pin(0), freq=400000)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(29), 0x3c,rotate=180)
while (button.value()==1):
    holdsec += 1
    led1.value(1)
    led7.value(1)
    time.sleep(0.5)
    led1.value(0)
    led7.value(0)
    time.sleep(0.5)
    if(holdsec==5):
        print("resetoidaan")
        settingsmode=True
        break
        
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
    }
    a_file = open("settings.json","w")
    json.dump(settings,a_file)
    a_file.close()

if(len(settings["password"]) > 0):
    wlansettings=False

else:
    wlansettings=True




if(settingsmode==False and wlansettings==False):
    attempts=0
    a_file = open("settings.json", "r")
    settings = json.load(a_file)
    a_file.close()
    




    # Connect to network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

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
            settings ={
            "ssid":"",
            "password":"",
            }
            a_file = open("settings.json","w")
            json.dump(settings,a_file)
            a_file.close()


            
    rounded = 0
    raver = 0
    def getPrices():

        print("Querying backend:")
        r = urequests.get("http://api.henkka.one/prices.json")
        print(r.json())

        info = r.json()
        r.close()
        price = info['price']
        average = info['average']
        global raver
        global rounded
        raver = round(float(average))
        rounded = round(float(price))
        print(rounded)
        display.fill(0)
        display.text("Hinta on nyt: ", 0, 0, 1)
        display.text(str(rounded)+"snt/kwh", 0, 8, 1)
        display.text("Keskihinta: ", 0, 16, 1)
        display.text(str(raver)+"snt/kwh", 0, 24, 1)
        display.show()
        version = info['version']
        if(version == settings["version"]):
            print("same version")
        else:
            settings["updateonboot"] = 1
            a_file = open("settings.json","w")
            json.dump(settings,a_file)
            a_file.close()
            print("ota update scheduled")
        return

    def leds(hinta):
        led1.value(hinta & 0x01)
        led2.value(hinta & 0x02)
        led3.value(hinta & 0x04)
        led4.value(hinta & 0x08)
        led5.value(hinta & 0x10)
        led6.value(hinta & 0x20)
        led7.value(hinta & 0x40)
        return

    getPrices()

    nextTime = time.time()+300
    print(nextTime)


    while True:
        if (nextTime < time.time()):
            getPrices()
            nextTime = time.time()+300
        else:
            leds(rounded)
            buttonpressed = button.value()
            if (buttonpressed == 1):
                leds(raver)
                time.sleep(10)
    
elif(wlansettings==True or settingsmode==True):
    import socket
    def connect():
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
    

    
    def open_socket(ip):
        # Open a socket
        address = (ip, 80)
        connection = socket.socket()
        connection.bind(address)
        connection.listen(1)
        print(connection)
        return connection

    def webpage():
        html = f"""
            <!DOCTYPE html>
            <html>
            <body>
            <form action="./" method="GET">
            <div>
            <label for="ssid">Wifi ssid</label>
            <input name="ssid" id="ssid" value="" />
            </div>
            <div>
            <label for="to">Wifi password</label>
            <input name="password" id="password" value="" />
            </div>
            <div>
            <button>Save and restart</button>
            </div>
            </form>
            </body>
            </html>
            """
        return str(html)
    
    def parsestring(request):
        
        ssid = request.split("&")[0]
        ssid = ssid.split("=")[1]
        password = request.split("&")[1]
        password = password.split("=")[1]
        
        settings["ssid"]=ssid
        settings["password"]= password
        print(settings)
        a_file = open("settings.json","w")
        json.dump(settings,a_file)
        a_file.close()
        machine.reset()
        
        return
    
    def serve(connection):
        #Start a web server
        while True:
            client = connection.accept()[0]
            request = client.recv(1024)
            request = str(request)
            try:
                request = request.split("?")[1]
                request = request.split()[0]
                print(request)
                parsestring(request)

            except IndexError:
                pass
            if request == '/lighton?':
                print("ok")
            html = webpage()
            client.send(html)
            client.close()
            

    try:
        ip = connect()
        display.sleep(False)
        display.fill(0)
        display.text('Yhdista laitteen', 0, 0, 1)
        display.text('wlan verkkoon', 0, 8, 1)
        display.text('SSID:Picow', 0, 16, 1)
        display.text('Salasana:', 0, 24, 1)
        display.text('123456789', 0, 32, 1)
        display.text('Sitten mene ', 0, 40, 1)
        display.text('selaimella:', 0, 48, 1)
        display.text(str(ip), 0, 56, 1)
         
        display.show()


        connection = open_socket(ip)
        serve(connection)
    except KeyboardInterrupt:
        machine.reset()       
else:
    print("kives")


