#!/usr/bin/python
# Example code to test scrolling text across multiple 8x8 matrices.
# WARNING! Make sure to use a level shifter between the Raspberry Pi
# and matrices running at 5v to avoid overpowering the Pi.

import RPi.GPIO as GPIO
import time
import random
from lib.Adafruit.Adafruit_LEDBackpack.Adafruit_8x8 import ColorEightByEight
from AlarmClock import AlarmClock

GPIO.setmode(GPIO.BOARD)

ledbtns = []
#Green
ledbtns.append({'led' : 11, 'button' : 12})
#Yello
ledbtns.append({'led' : 13, 'button' : 16})
#Red
ledbtns.append({'led' : 15, 'button' : 18})

for elm in ledbtns:
    GPIO.setup(elm['led'], GPIO.OUT)
    GPIO.output(elm['led'], GPIO.HIGH)
    GPIO.setup(elm['button'], GPIO.IN)

#GPIO.setup(11, GPIO.OUT)
#GPIO.output(11, GPIO.LOW)
#GPIO.output(11, GPIO.HIGH)

MATRICES = 5
matrix = []

alarm = AlarmClock(debug=True)

message = alarm.display_msg()

for i in range(0,MATRICES):
    matrix.append(ColorEightByEight(address=0x70+i))
    matrix[i].setTextWrap(False) # Allow text to run off edges
    matrix[i].setRotation(3)
    matrix[i].setBrightness(1)
    matrix[i].setTextSize(1)
    matrix[i].setTextColor(alarm.get_color(), alarm.get_bg())

# Defintions for Alarm Hardware

def update_matrixes():
    message = alarm.display_msg()
    
    for i in range(0,MATRICES):
        # Draw message in each matrix buffer, offseting each by 8 pixels
        #matrix[i].clear()
        matrix[i].setCursor(x - i * 8, 1)
        matrix[i].printMessage(message)
        matrix[i].setTextColor(alarm.get_color(), alarm.get_bg())
    
    # Write data to matrices in separate loop so it's less jumpy
    for i in range(0,MATRICES):
        matrix[i].writeDisplay()

# Horiz. position of text -- starts off right edge
x = 2
iter = 0

while True:
    iter += 1

    # Update Display
    update_matrixes()

    if alarm.check_alarm():
        #Start Game
        for i in range(0, 6):
            #Get Random LEDBUTTON
            current = random.choice(ledbtns);
            #Turn it on
            GPIO.output(current['led'], GPIO.LOW);
            not_pressed = True
            #Wait until it is pressed
            s = 0
            while not_pressed:
                if not GPIO.input(current['button']):
                    not_pressed = False
                    #TURN LIGHT OFF
                    GPIO.output(current['led'], GPIO.HIGH)
                    update_matrixes()
                    time.sleep(1)
                #Update Display
                if not s % 100:
                    update_matrixes()
                s += 1
                #Sleep
                time.sleep(0.01)
                
        #Stop Alarm
        alarm.stop_alarm()
    #Sleep for second before updating the display
    time.sleep(1)
