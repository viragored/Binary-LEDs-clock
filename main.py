import network
import time
from time import sleep
import machine
from machine import Pin, RTC
import urequests
from secret import ssid,password
nethostname = "LEDclock"

timeurl = "http://worldtimeapi.org/api/ip"
led = Pin(28, Pin.OUT)
Hpins = [Pin(4,Pin.OUT), Pin(3,Pin.OUT), Pin(2,Pin.OUT), Pin(1,Pin.OUT), Pin(0,Pin.OUT)]
Mpins = [Pin(17,Pin.OUT),Pin(16,Pin. OUT),Pin(15,Pin.OUT),Pin(14,Pin.OUT),Pin(13,Pin.OUT),Pin(12,Pin.OUT)]
Spins = [Pin(26,Pin.OUT), Pin(22,Pin. OUT),Pin(21,Pin.OUT), Pin(20,Pin.OUT),Pin(19,Pin.OUT),Pin(18,Pin.OUT)]
GPs = (18,19,20,21,22,26,12,13,14,15,16,17,0,1,2,3,4,28)
retrytime = 20 # wait before re-trying urequests

# blink status LED
def blink(blinktimes,howlong):
    for blinkcount in range (0, blinktimes):
        led.on()
        sleep(howlong)
        led.off()
        sleep(howlong)
# Fast flashes all LEDs
def flasher ():
    for counter, GP in enumerate(GPs):
        object = Pin(GP,Pin.OUT)
        object.value(1)
        sleep(0.1)
        object.value(0)       
# turns off all LEDs
def blank ():
    for counter, GP in enumerate(GPs):
        print(counter)
        object = Pin(GP,Pin.OUT)
        object.value(0)
# Connects to wifi network
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected() and wlan.status() >= 0:
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    blink(10,0.1) # short blinks = got network connection
    return ip
# gets local time
def synctime(rtc):
    response = urequests.get(timeurl, timeout = retrytime)
    json = response.json()
    current_time = json["datetime"]
    print ("current_time =",current_time)
    the_date, the_time = current_time.split("T")
    year, month, mday = [int(x) for x in the_date.split("-")]
    the_time = the_time.split(".")[0]
    hours, minutes, seconds = [int(x) for x in the_time.split(":")]
    year_day = json["day_of_year"]
    week_day = json["day_of_week"]
    is_dst = json["dst"]
    response.close()
    rtc.datetime((year, month, mday, week_day, hours, minutes, seconds, 0)) # (year, month, month-day, weekday, hours, minutes, seconds, subseconds)
# displays the time on the LEDs
def display_num(number, pins):    
    for counter, pin in enumerate(pins):
        if number >= pow(2, len(pins)-(counter+1)):
            number = number - pow(2, len(pins)- (counter+1))
            pin.value(1)
        else:
            pin.value(0)
# tells the display module which pins to use
def showtime ():
    display_num(H, Hpins)
    display_num(M, Mpins)
    display_num(S, Spins)
"""
Start of code
"""
sleep(3) # sleep to allow Thonny into main.py
flasher() # flash all LEDs in sequence
led.on() # Pin 28 status LED steady shows power on

while True:
    try: # connect to network
        ip = connect()
        rtc = RTC()
        synctime(rtc)
        Y, Mo, D, W, H, M, S, SS = rtc.datetime()
        Syncday = D # At startup note what day the sync happened
        print ("Time is: ",H,M,S)
        print ("year, month, month-Day, weekday, hours, minutes, seconds, subseconds")
        print (Y,Mo,D,W,H,M,S,SS)
        while True: # Loop for ever
            Y, Mo, D, W, H, M, S, SS = rtc.datetime()
            # Resync from time server daily at 03.01 to catch Daylight savings changes
            if H == 3 and M == 1 and S == 0 and Syncday != D: # Has the day changed?
                print ("Resync")
                time.sleep(1.1) # ensure seconds won't match next loop
                synctime(rtc)
                Syncday = D # refresh day the sync happened
            showtime()
            time.sleep(0.5) # ensures daily time test will find 00 seconds
    except KeyboardInterrupt:
        print ("Keyboard interrupt")
        blank()
        break
    except KeyError:
        blink (5,0.5) # slow blink on error
        blank()
        print("KeyError")
        sleep (2)
        pass
    except ValueError:
        blink (5,0.5) # slow blink on error
        blank()
        print("ValueError")
        sleep (2)
        pass
    except OSError as e:
        blink (10,0.1) # fast blink on error
        print("urequests.get timed out or failed:", e)
        sleep (2)
        pass
