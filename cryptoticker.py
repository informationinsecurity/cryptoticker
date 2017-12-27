import psutil, sys,threading
import time,datetime
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import Adafruit_SSD1306
import json, urllib
import os
import netifaces as ni
import socket
import urllib2


from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

c = threading.Condition()

# Raspberry Pi pin configuration:
RST = None       # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Input pins:
L_pin = 27
R_pin = 23
C_pin = 4
U_pin = 17
D_pin = 22

A_pin = 5
B_pin = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up



disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize library.
disp.begin()
# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))


# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()
font35 = ImageFont.truetype('vcr.ttf',16)

#Variables cause 2 unsynchroned threads
flip = "0"
mode = 0
ETH = ""
BTC = ""
IP = ""
CPU = ""
LTC = ""
MemUsage = ""
Disk = ""
timer = 27 # on my system atleast?
kill = 0
btchigh = ""
btclow = ""
ethhigh = 0
ethlow = 100000
ltchigh = 0
ltclow = 100000
btchighscore = ""
btclowscore = ""

class varupdate(threading.Thread):
        #Thread to update variables every 30 seconds
        def __init__(self, name):
                threading.Thread.__init__(self)
                self.name = name
        def stop(self):
                return
                self._stop_event.set()
        def run(self):
                global flip
                global mode
                global BTC
                global IP
                global CPU
                global MemUsage
                global Disk
                global ETH
                global urleth
                global timer
                global LTC
                global btchighscore
                global urlltc
                global kill
                global btchigh
                global btclow
                global ethhigh
                global ethlow
                global ltchigh
                global ltclow
                btchigh = open('.btchighscore', 'r+').read()
                btchigh = float(btchigh)
                btclow = open('.btclowscore', 'r+').read()
                btclow = float(btclow)
                ethhigh = open('.ethhighscore', 'r+').read()
                ethhigh = float(ethhigh)
                ethlow = open('.ethlowscore', 'r+').read()
                ethlow = float(ethlow)
                ltchigh = open('.ltchighscore', 'r+').read()
                ltchigh = float(ltchigh)
                ltclow = open('.ltclowscore', 'r+').read()
                ltclow = float(ltclow)
                print("BTC Stored High Price: $" + str(btchigh))
                print("BTC Stored Low Price: $" + str(btclow))
                print "-----------------"
                print("ETH Stored High Price: $" + str(ethhigh))
                print("ETH Stored Low Price: $" + str(ethlow))
                print "-----------------"
                print("LTC Stored High Price: $" + str(ltchigh))
                print("LTC Stored Low Price: $" + str(ltclow))
                print "-----------------"
                #print "Stored Low Price"; print btclow
                while True:
                                url = "https://api.gdax.com/products/BTC-USD/ticker"
                                c.acquire()
                                BTC = float(json.load(urllib.urlopen(url))['price'])
                                urleth = "https://api.gdax.com/products/ETH-USD/ticker"
                                ETH = float(json.load(urllib.urlopen(urleth))['price'])
                                urlltc = "https://api.gdax.com/products/LTC-USD/ticker"
                                LTC = float(json.load(urllib.urlopen(urlltc))['price'])
                                st = datetime.datetime.now()
                                print (st.strftime("%Y-%m-%d %H:%M:%S"))
                                print("Current BTC Price: $" + str(BTC) + " | BTC High: $" + str(btchigh) + " | BTC Low: $" + str(btclow))
                                print("Current ETH Price: $" + str(ETH) + " | ETH High: $" + str(ethhigh) + " | ETH Low: $" + str(ethlow))
                                print("Current LTC Price: $" + str(LTC) + " | LTC High: $" + str(ltchigh) + " | LTC Low: $" + str(ltclow))
                                print "----------"
                                if BTC < btclow: print("Old BTC Low: $" + str(btclow)); print("Current BTC price: $" + str(BTC)); btclow = BTC; print("New BTC Low: $" + str(btclow) + "\n----------"); l = open('.btclowscore', 'w'); l.write(str(btclow)); l.close()
                                if BTC > btchigh: print("Old BTC High: $" + str(btchigh)); print("Current BTC price: $" + str(BTC)); btchigh = BTC; print("New BTC High: $" + str(btchigh)  + "\n----------"); l = open('.btchighscore', 'w'); l.write(str(btchigh)); l.close()

                                if ETH < ethlow: print("Old ETH Low: $" + str(ethlow)); print("Current ETH price: $" + str(ETH)); ethlow = ETH; print("New ETH Low: $" + str(ethlow) + "\n----------"); l = open('.ethlowscore', 'w'); l.write(str(ethlow)); l.close()
                                if ETH > ethhigh: print("Old ETH High: $" + str(ethhigh)); print("Current ETH price: $" + str(ETH)); ethhigh = ETH; print("New ETH High: $" + str(ethhigh) + "\n----------"); l = open('.ethhighscore', 'w'); l.write(str(ethhigh)); l.close()

                                if LTC < ltclow: print("Old LTC Low: $" + str(ltclow)); print("Current LTC price: $" + str(LTC)); ltclow = LTC; print("New LTC Low: $" + str(ltclow) + "\n----------"); l = open('.ltclowscore', 'w'); l.write(str(ltclow)); l.close()
                                if LTC > ltchigh: print("Old LTC High: $" + str(ltchigh)); print("Current LTC price: $" + str(LTC)); ltchigh = LTC; print("New LTC High: $" + str(ltchigh) + "\n----------"); l = open('.ltchighscore', 'w'); l.write(str(ltchigh)); l.close()


                                c.release()
                                timer=15
                                for i in range(15):
                                        time.sleep(1)
                                        if kill == 1:
                                                return


class screenctl(threading.Thread):
        #Thread to refresh oled display
        def __init__(self, name):
                threading.Thread.__init__(self)
                self.name = name
        def stop(self):
                self._stop_event.set()
                return
        def run(self):
                global flip
                global mode
                global BTC
                global ETH
                global timer
                global kill
                global btchigh
                global btclow
                global ethhigh
                global ethlow
                global ltchigh
                global ltclow
                try:
                        while True:
                                c.acquire()
                                # Draw a black filled box to clear the image.
                                draw.rectangle((0,0,width,height), outline=0, fill=0)
                                if not GPIO.input(D_pin):
                                        kill = 1
                                        break
                                if GPIO.input(U_pin): # button is released
                                        mode = mode
                                else: # button is pressed:
                                        if mode == 0:
                                                mode = 1
                                        else:
                                                mode = 0
                                if mode == 1:
                                        #Stats Mode
                                        font = ImageFont.load_default()
                                        # Writes text.
                                        draw.text((x, top),        "BTC High: " + str(btchigh),  font=font, fill=255)
                                        draw.text((x, top+8),      "BTC Low: " + str(btclow),  font=font, fill=255)
                                        draw.text((x, top+10),  "______________________    ",  font=font, fill=255)
                                        draw.text((x, top+22),     "ETH High: " + str(ethhigh),  font=font, fill=255)
                                        draw.text((x, top+30),      "ETH Low: " + str(ethlow),  font=font, fill=255)
                                        draw.text((x, top+32),  "______________________    ",  font=font, fill=255)
                                        draw.text((x, top+44),     "LTC High: " + str(ltchigh),  font=font, fill=255)
                                        draw.text((x, top+52),      "LTC Low: " + str(ltclow),  font=font, fill=255)
                                        draw.text((x+110, top+55),      str(timer),  font=font, fill=255)
                                        timer = timer - 1
                                        disp.image(image.rotate(180)) #rotated 180
                                        disp.display()
                                        if kill == 1:
                                                c.release()
                                                return
                                        time.sleep(1)
                                        c.release()
                                else:
                                        #Stats Mode
                                        font = ImageFont.load_default()
                                        draw.text((x, top),     "BTC/USD:",  font=font, fill=255)
                                        draw.text((x, top+16),  str(BTC),  font=font35, fill=255)
                                        draw.text((x, top+36),  "ETH/USD:",  font=font, fill=255)
                                        draw.text((x+70, top+36),  "LTC/USD:",  font=font, fill=255)
                                        draw.text((x+70, top+50),  str(LTC),  font=font35, fill=255)
                                        draw.text((x, top+50),  str(ETH),  font=font35, fill=255)
                                        draw.text((x+110, top),      str(timer),  font=font, fill=255)
                                        timer = timer - 1
                                        disp.image(image.rotate(180)) #rotated 180
                                        disp.display()
                                        if kill == 1:
                                                c.release()
                                                return
                                        time.sleep(1)
                                        c.release()

                except KeyboardInterrupt:
                        GPIO.cleanup()

a = varupdate("varupdate")
b = screenctl("screenctl")
b.start()
a.start()
def bye( display ):
        "Program is exiting"
        print "Bye..."
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        disp.image(image)
        disp.display()
        draw.text((x, top+16),  str("Bye!"),  font=font35, fill=255)
        disp.image(image.rotate(180)) #rotated 180
        disp.display()
        time.sleep(1)
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        disp.image(image)
        disp.display()
        return

while True:
        try:
        #Keep main thread from exiting, trying to exit threads correctly...
                time.sleep(1)
                if kill == 1:
                        bye(disp)
                        kill = 1
                        a.join()
                        b.join()
                        # Draw a black filled box to clear the image.
                        break
        except (KeyboardInterrupt, SystemExit, kill):
                bye(disp)
                kill = 1
                a.join()
                b.join()
                break
