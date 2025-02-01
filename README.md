# Binary LEDs clock Raspberry Pi Pico W
Code for a Pico W binary clock with individual LEDs.
This will fetch the internet time wherever in the world you are and display it on the LEDs. 
Summertime / wintertime changes are handled automatically.
## Update January 2025
I've made some changes to the code to improve error trapping, and to separate wifi password entry from the main code. That is no more secure than any other way of getting and storing the password, but it stops me accidentally publishing my own wifi password along with the code.
### secret.py
You will need to create on the Pico, in the same directory as 'main.py', a file called 'secret.py'. This file needs to contain two lines:
* ssid = 'your wifi network name'
* password = 'Your wifi password'
As you'll no doubt already know, ssid and password must be as shown, and the characters in between the quote marks must be exactly as used for your wifi network. No extra capitals, trailing spaces, etc.

## Inspirations
### Hackspace
Issue 63 of Hackspace Magazine, pages 54-57 showed a basic binary clock. I thought I'd have a go at making one, and making it a bit more featured.

Download the magazine for free (or you might think they're worth giving a donation to): https://hackspace.raspberrypi.com/issues/63/pdf 
### Youtube
"Gary Explains" showed a clock with Python closer to what I wanted, but using NeoPixels: https://www.youtube.com/watch?v=DIvLfKdn15I 
## My Python code
Requires **micropython** on the Pico W 

I've taken elements from both inspirations and tried to blend the result into something understandable.

### main.py
I'm a novice with Python so what I've done can surely be improved!

My goal was to have the clock start and get internet time for my local time zone. I then want to synchronise the Pico real-time clock daily, to counter any clock drift, and pick up changes between standard time and daylight saving time when they occur.

There's a spare space on the left end of the hours row, so I've used an LED there to signal status:
* Steady = power connected
* Blinking = network connected
* No light when the time is displayed

I've tested the code as far as I'm able, and think it all works as it should. But I can't actually test the Daylight Saving Time switch for quite a while - when it  happens I'll know if my testing was good enough.

[Update January 2025: The twice-yearly overnight time changes have happened correctly for two years now.]

If the clock happens to start up between 00.00 and 03.01, it won't do an update time sync so could miss a Daylight Saving Time change on that occasion. (If someone would like to kill that bug and send a Pull request, I'd be delighted!)

There are some "print" commands in the code. They helped me get everything working properly so I have left them in.
### LEDtest.py
This code flashes all the LEDs in turn. I found that useful to check my soldering was successful.
## 3D model
My model is on Printables.com with customisable options. I designed that in OpenSCAD with the parameters labelled for easy customising. 
https://www.printables.com/model/386623

I've put below a picture showing the GPIO wiring connections. 

As the Hackspace Magazine authors point out, you can put the clock into anything that tickles your fancy!
## Images
![13 47 30 on binary clock](https://user-images.githubusercontent.com/28804416/216216111-f2e749db-85fd-4063-8f82-b9e7062ee9fd.jpg "13:47:30")
![final clock GPIO layout](https://user-images.githubusercontent.com/28804416/216257041-c2eab93f-9c94-4c49-a68f-4616a36768c5.png)

There's a short video on YouTube showing the start-up sequence:
https://youtu.be/ZOUNjKuRbA0
