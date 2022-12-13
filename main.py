# A simple example that:
# - Connects to a WiFi Network defined by "ssid" and "password"
# - Performs a GET request (loads a webpage)
# - Queries the current time from a server

import uos
import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
from machine import Pin
import json
import time

led1 = Pin(9, Pin.OUT)
led2 = Pin(10, Pin.OUT)
led3 = Pin(11, Pin.OUT)
led4 = Pin(12, Pin.OUT)
led5 = Pin(13, Pin.OUT)
led6 = Pin(14, Pin.OUT)
led7 = Pin(15, Pin.OUT)

button = Pin(16, Pin.IN, Pin.PULL_DOWN)
holdsec = 0

while (button.value()==1):
    holdsec += 1
    led1.value(1)
    led7.value(1)
    time.sleep(0.5)
    led1.value(0)
    led7.value(0)
    time.sleep(0.5)
    if(holdsec==30):
        print("resetoidaan")
        wlansettings = open("settings.csv","w")
        wlansettings.close()
        break
        



try:
    filesize = uos.stat("settings.csv")[6]
except OSError:
    wlansettings = open("settings.csv","w")
    wlansettings.close()
    filesize = uos.stat("settings.csv")[6]


if(filesize>0):
    attempts=0
    wlansettings = open("settings.csv","r")
    wlaninfo = wlansettings.read()
    splitinfo = wlaninfo.split(",")
    wlansettings.close()



    # Connect to network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    wlan.connect(splitinfo[0], splitinfo[1])
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
        attempts += 1
        if(attempts > 19):
            wlansettings = open("settings.csv","w")
            wlansettings.close()
            machine.reset()
            
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
    
else:
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
        
        wlansettings = open("settings.csv","w")
        ssid = request.split("&")[0]
        ssid = ssid.split("=")[1]
        password = request.split("&")[1]
        password = password.split("=")[1]
        
        print(ssid + ' , ' + password)

        wlansettings.write(ssid+"," +password)
        wlansettings.close()
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
        connection = open_socket(ip)
        serve(connection)
    except KeyboardInterrupt:
        machine.reset()       



