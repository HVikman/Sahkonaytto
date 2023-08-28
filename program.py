from uos import stat
import urequests # handles making and servicing network requests
from machine import Pin, I2C
import machine
import json
import time
import sh1106
import socket
import webpages

i2c = I2C(0,scl=Pin(1), sda=Pin(0), freq=400000)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(29), 0x3c,rotate=180)

led1 = Pin(9, Pin.OUT)
led2 = Pin(10, Pin.OUT)
led3 = Pin(11, Pin.OUT)
led4 = Pin(12, Pin.OUT)
led5 = Pin(13, Pin.OUT)
led6 = Pin(14, Pin.OUT)
led7 = Pin(15, Pin.OUT)
green = Pin(22, Pin.OUT)
red = Pin(21, Pin.OUT)
raver = 0
rounded =0

def getPrices(settings):
    print("Querying backend:")
    r = urequests.get("http://api.henkka.one/prices.json").json()
    global price
    global average
    price = r['PriceWithTax']*100
    r.close()
    r=urequests.get('https://api.spot-hinta.fi/Today').json()
    total = sum(item['PriceWithTax']*100 for item in r)
    average = round((total / len(r)),1)
    r.close()
    print(settings['rounding'])
    if settings['rounding']==1:
        average = round(float(average))
        price = round(float(price))
    display.fill(0)
    display.text("Hinta on nyt: ", 0, 0, 1)
    display.text(str(price)+"snt/kwh", 0, 9, 1)
    display.text("Paivan ka:", 0, 24, 1)
    display.text(str(average)+"snt/kwh", 0, 33, 1)
    display.show()

    if(info['version'] == settings["version"]):
        print("same version")
    else:
        settings["updateonboot"] = 1
        a_file = open("settings.json","w")
        json.dump(settings,a_file)
        a_file.close()
        print("ota update scheduled")
    if settings["limit"]>=round(float(price)):
        red.value(0)
        green.value(1)
    elif settings['limit']==0:
        if average<price:
            red.value(1)
            green.value(0)
        else:
            red.value(0)
            green.value(1)
    else:
        red.value(1)
        green.value(0)
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
def main(button,settings):
           
    getPrices(settings)

    nextTime = time.time()+600
    print(nextTime)
    while True:
        if (nextTime < time.time()):
            getPrices(settings)
            nextTime = time.time()+600
        else:
            leds(round(float(price)))
            buttonpressed = button.value()
            if (buttonpressed == 1):
                print("nappi")
                leds(round(float(average)))
                time.sleep(10)
                
def open_socket(ip):
        # Open a socket
        address = (ip, 80)
        connection = socket.socket()
        connection.bind(address)
        connection.listen(1)
        print(connection)
        return connection
def parsestring(request, settings):
        
    setting = request.split("=")[0]
    try:
        value = int(request.split("=")[1])
    except:
        value=request.split("=")[1]
        
    if setting=="updatenow":
        print("Update things will be here")
        
    elif setting=="ssid":
        ssid = request.split("&")[0]
        ssid = ssid.split("=")[1]
        password = request.split("&")[1]
        password = password.split("=")[1]
        settings["ssid"]=ssid
        settings["password"]= password
    else:
        settings[setting]=value
        print(settings)
        
    a_file = open("settings.json","w")
    json.dump(settings,a_file)
    a_file.close()

    return

def serve(connection, html, settings):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split("?")[1]
            request = request.split()[0]
            print(request)
            parsestring(request, settings)

        except IndexError:
            pass
        if request == '/lighton?':
            print("ok")
        client.send(html)
        client.close()

def wlansettings(ip,settings):
    html = webpages.wlansettings()
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
        serve(connection,html, settings)
    except KeyboardInterrupt:
        machine.reset()
            
            
def settings(ip,settings):
    html = webpages.settings(settings['version'])    
    try:
        display.sleep(False)
        display.fill(0)
        display.text('Yhdista samaan', 0, 0, 1)
        display.text('wlan verkkoon', 0, 8, 1)
        display.text('laitteen kanssa', 0, 16, 1)
        display.text('ja avaa', 0, 40, 1)
        display.text('selaimella:', 0, 48, 1)
        display.text(str(ip), 0, 56, 1)
        display.show()

        connection = open_socket(ip)
        serve(connection,html, settings)
        
    except KeyboardInterrupt:
        machine.reset()   