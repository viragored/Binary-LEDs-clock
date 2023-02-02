import network
import time
from time import sleep
import machine
from machine import Pin, RTC
import urequests

ssid = 'Your WiFi network name'
password = 'Your WiFi password'
timeurl = "http://worldtimeapi.org/api/ip"
led = Pin(28, Pin.OUT)
Hpins = [Pin(4,Pin.OUT), Pin(3,Pin.OUT), Pin(2,Pin.OUT), Pin(1,Pin.OUT), Pin(0,Pin.OUT)]
Mpins = [Pin(17,Pin.OUT),Pin(16,Pin. OUT),Pin(15,Pin.OUT),Pin(14,Pin.OUT),Pin(13,Pin.OUT),Pin(12,Pin.OUT)]
Spins = [Pin(26,Pin.OUT), Pin(22,Pin. OUT),Pin(21,Pin.OUT), Pin(20,Pin.OUT),Pin(19,Pin.OUT),Pin(18,Pin.OUT)]
GPs = (18,19,20,21,22,26,12,13,14,15,16,17,0,1,2,3,4,28)

# blink white LED
def blink(blinktimes,howlong):
    for blinkcount in range (0, blinktimes):
        led.on()
        sleep(howlong)
        led.off()
        sleep(howlong)

def flasher ():
# Fast flash all LEDs in sequence
    for counter, GP in enumerate(GPs):
        object = Pin(GP,Pin.OUT)
        object.value(1)
        sleep(0.1)
        object.value(0)       
    
def connect():
    # Connect to wifi network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    blink(3,0.2) # 3 short blinks = got network connection
    return ip

def synctime(rtc, wait=True):
    response = None
    while True:
        try:
            response = urequests.get(timeurl)
            break
        except:
            if wait:
                response.close()
                continue
            else:
                response.close()
                return

    json = response.json()
    current_time = json["datetime"]
    the_date, the_time = current_time.split("T")
    year, month, mday = [int(x) for x in the_date.split("-")]
    the_time = the_time.split(".")[0]
    hours, minutes, seconds = [int(x) for x in the_time.split(":")]
    year_day = json["day_of_year"]
    week_day = json["day_of_week"]
    is_dst = json["dst"]
    response.close()
    rtc.datetime((year, month, mday, week_day, hours, minutes, seconds, 0)) # (year, month, month-day, weekday, hours, minutes, seconds, subseconds)
"""
Start of code
"""
flasher() # flash all LEDs in sequence
led.on() # Pin 28 white LED shows power on

try: # connect to network
    ip = connect()
except KeyboardInterrupt:
    machine.reset()
    
rtc = RTC()
synctime(rtc,wait=True)

Y, Mo, D, W, H, M, S, SS = rtc.datetime()
Syncday=W
# print ("Syncday =",W)
# print ("Time is: ",H,M,S)
# print (Y,Mo,D,W,H,M,S,SS)
def display_num(number, pins):    
    for counter, pin in enumerate(pins):
        if number >= pow(2, len(pins)-(counter+1)):
            number = number - pow(2, len(pins)- (counter+1))
            pin.value(1)
        else:
            pin.value(0)
def showtime ():
    display_num(H, Hpins)
    display_num(M, Mpins)
    display_num(S, Spins)

while True:
    Y, Mo, D, W, H, M, S, SS = rtc.datetime()
    # Resync from time server at 03.01 to catch Daylight savings changes
    if H == 3 and M == 1 and Syncday != W:
        Syncday += 1
        # print ("Resync")
        synctime(rtc,wait=False)
        #Syncday=W
    showtime()
    time.sleep(0.5)
