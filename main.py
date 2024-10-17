from machine import Pin, SPI
import machine
from ST7735 import TFT,TFTColor
import random
from time import sleep
from time import time
import os
import framebuf

# Release any resources currently in use for the displays
spi = SPI(0, baudrate=20000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
tft=TFT(spi,5,22,21)
tft.initr()
tft.rgb(True)

tft._setwindowloc((2,1),(129,160))
buf = bytearray(128*160*2)
fb = framebuf.FrameBuffer(buf, 128, 160, framebuf.RGB565)
fb.fill(0x2421)
tft._writedata(buf)


p16 = Pin(16, Pin.IN, Pin.PULL_UP)
p17 = Pin(17, Pin.IN, Pin.PULL_UP)
p20 = Pin(20, Pin.OUT, value=0)


die_size = [4,4,4,4,4,4]
die_index = 0

sleeptimer = 0


def reshuf():
    bits = 3
    for i in [0,1,2,3,4,5]:
        random.seed()
        bits = (die_size[i]+2)//2
        num = random.getrandbits(bits)
        while num < 1 or num > die_size[i]:
            num = random.getrandbits(bits)
        drawDie(i,num)


def gotobed(p):
    tft._setwindowloc((2,1),(129,160))
    buf = bytearray(128*160*2)
    fb = framebuf.FrameBuffer(buf, 128, 160, framebuf.RGB565)
    fb.fill(0)
    fb.text('AU REVOIR', 50, 70, 0xffff)
    tft._writedata(buf)
    sleep(2)
    p20.value(1)
    machine.deepsleep()



def drawDieConfig(position):
    #display.fill(0)
    drawDie(position,die_size[position])
    if position == die_index:
        if position == 0:
            offsetx = 8
            offsety = 1
        if position == 1:
            offsetx = 70
            offsety = 1
        if position == 2:
            offsetx = 8
            offsety = 54
        if position == 3:
            offsetx = 70
            offsety = 54
        if position == 4:
            offsetx = 8
            offsety = 107
        if position == 5:
            offsetx = 70
            offsety = 107
        tft.rect((offsetx, offsety), (52, 52), 0xffff)


def drawDie(position,value):
    if position == 0:
        offsetx = 8
        offsety = 1
    if position == 1:
        offsetx = 70
        offsety = 1
    if position == 2:
        offsetx = 8
        offsety = 54
    if position == 3:
        offsetx = 70
        offsety = 54
    if position == 4:
        offsetx = 8
        offsety = 107
    if position == 5:
        offsetx = 70
        offsety = 107


    if die_size[position] in [4,6,8,10,12,20]:
        printDado(die_size[position],value,offsetx,offsety)


def cycleDieSides(p):
    global die_size
    global sleeptimer
    sleeptimer = time()
    die_size[die_index] += 1
    if die_size[die_index] == 5: die_size[die_index] = 6
    if die_size[die_index] == 7: die_size[die_index] = 8
    if die_size[die_index] == 9: die_size[die_index] = 10
    if die_size[die_index] == 11: die_size[die_index] = 12
    if die_size[die_index] in [13,14,15,16,17,18,19]: die_size[die_index] = 20
    if die_size[die_index] >= 21: die_size[die_index] = 4
    drawDieConfig(die_index)


def cycleDie(p):
    global die_index
    global sleeptimer
    sleeptimer = time()
    file = open("cfg.txt", "w")
    cfg = ','.join(str(x) for x in die_size)
    file.write(cfg)
    file.close()
    die_index += 1
    if die_index >= 6: die_index = 0
    for i in [0,1,2,3,4,5]:
        drawDieConfig(i)



def printDado(die_size,side,x,y):
    print("display image")
    img = "bmp/d"
    img += str(die_size)
    img += "l"
    img += str(side)
    img += ".rgb565"
    print(img)
    tft._setwindowloc((x,y),(x+52,y+52))
    with open(img,'rb') as f:
        #loadbmp(f,x,y)
            dummy = f.read(1)
            data = bytearray(f.read())
            #fbuf.fill(0)
            fbuf = framebuf.FrameBuffer(data, 53, 53, framebuf.RGB565)
            tft._writedata(fbuf)



###################################################

###################################################

#file.write(str(die_size[0]))

print("loading config")
file = open("cfg.txt", "r")
cfg = file.read()
file.close()
print("config loaded")

die_size_str = cfg.split(',', 6)
die_size[0] = int(die_size_str[0])
die_size[1] = int(die_size_str[1])
die_size[2] = int(die_size_str[2])
die_size[3] = int(die_size_str[3])
die_size[4] = int(die_size_str[4])
die_size[5] = int(die_size_str[5])
die_index = 0

reshuf()

sleeptimer = time()


while True:
    #pass
    #print("running")
    if p16.value() == 0:
        cycleDie(0)
        print("cycleDie")
        sleep(0.25)
    if p17.value() == 0:
        cycleDieSides(0)
        print("cycleDieSides")
        sleep(0.25)

    
    if (time() - sleeptimer) > 30:
        gotobed(0)






