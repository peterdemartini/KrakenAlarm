#!/usr/bin/python
# A bunch of random tests for drawing GFX on the matrices

import time
from glcdfont import glcdfont
from Adafruit_8x8 import EightByEight

grid1 = EightByEight(address=0x70)
grid2 = EightByEight(address=0x71)
grid3 = EightByEight(address=0x72)
grid1.setBrightness(8)
grid2.setBrightness(8)
grid3.setBrightness(8)
font = glcdfont().getfont()

#print(font)
grid1.fillScreen()
grid1.writeDisplay()
time.sleep(.25)
grid1.clear()

grid2.fillScreen()
grid2.writeDisplay()
time.sleep(.25)
grid2.clear()

grid3.fillScreen()
grid3.writeDisplay()
time.sleep(.25)
grid3.clear()

for i in range (0, 24):
    grid1.drawLine(7,7-i,0,-16+i)
    grid2.drawLine(7,15-i,0,-8+i)
    grid3.drawLine(7,23-i,0,0+i)
    grid1.writeDisplay()
    grid2.writeDisplay()
    grid3.writeDisplay()
    time.sleep(.05)
    grid1.clear()
    grid2.clear()
    grid3.clear()

for i in range (0, 16, 2):
    grid1.drawCircle(4,4-8,i+1)
    grid2.drawCircle(4,4,i+1)
    grid3.drawCircle(4,4+8,i+1)
    grid1.writeDisplay()
    grid2.writeDisplay()
    grid3.writeDisplay()
    time.sleep(.05)
grid1.clear()
grid2.clear()
grid3.clear()

for i in range (0,8):
    grid1.drawCircle(4,4,i+1)
    grid2.fillCircle(4,4,i+1)
    grid3.drawPixel(i,0)
    grid1.writeDisplay()
    grid2.writeDisplay()
    grid3.writeDisplay()
    time.sleep(.05)
    grid1.clear()
    grid2.clear()
    grid3.clear()
    
for i in range (0,8):
    grid1.drawPixel(0,i)
    grid2.drawTriangle(0,0,7,i,0,7)
    grid3.fillTriangle(7,7,0,i,7,0)
    grid1.writeDisplay()
    grid2.writeDisplay()
    grid3.writeDisplay()
    time.sleep(.05)
    grid1.clear()
    grid2.clear()
    grid3.clear()

    
grid1.drawRoundRect(0,0,7,7,2)
grid2.fillRoundRect(0,0,8,8,2)
grid1.writeDisplay()
grid2.writeDisplay()
time.sleep(.5)
grid2.clear()
grid1.clear()

for i in range (1,9):
    grid2.drawRect(0,0,i,i)
    grid2.writeDisplay()
    time.sleep(.05)
    grid2.clear()

for i in range (1,9):
    grid3.fillRect(0,0,i,i)
    grid3.writeDisplay()
    time.sleep(.05)
    grid3.clear()

while True:
    #binary = 0b10101010
    #for k in range(0,8):
        #print('binary = ' + str(bin(binary)))
        #binary >>= 1
        #time.sleep(.01)
    
    for i in range(0,255,3):
    #for i in range(0,10):
        for j in range(0,5):
            #print "printing i: " + str(i) + " j: " + str(j) + " char(i+j): " + str(i*5+j) + " " + bin(font[i*5+j])
            grid1.writeRowRaw(5-j, font[i*5+j]) 
            grid2.writeRowRaw(5-j, font[(i+1)*5+j]) 
            grid3.writeRowRaw(5-j, font[(i+2)*5+j]) 
            #print "Buffer: " + str(i) + "-" + str(j) + " " + str(bin(font[i*5+j]))
            #grid.writeRowRaw(j, font[i*5+j]) 
            #print "Buffer: " + str(i) + "-" + str(j) + " " + str(bin(font[i*5+j]))
        time.sleep(.25)
        #grid.clear()