#!/usr/bin/python
# Example code to test scrolling text across multiple 8x8 matrices.
# WARNING! Make sure to use a level shifter between the Raspberry Pi
# and matrices running at 5v to avoid overpowering the Pi.

import time
from Adafruit_8x8 import ColorEightByEight

def get_time():
	return time.strftime("%I:%M %p")

MATRICES = 4
matrix = []
color = 2

for i in range(0,MATRICES):
    matrix.append(ColorEightByEight(address=0x70+i))
    matrix[i].setTextWrap(False) # Allow text to run off edges
    matrix[i].setRotation(3)
    matrix[i].setBrightness(4)
    matrix[i].setTextSize(1)

message = get_time()

# Horiz. position of text -- starts off right edge
x = 1
while True:
    message = get_time()
    
    for i in range(0,MATRICES):
        # Draw message in each matrix buffer, offseting each by 8 pixels
        matrix[i].clear()
        matrix[i].setCursor(x - i * 8, 1)
        matrix[i].printMessage(message)
    
    # Write data to matrices in separate loop so it's less jumpy
    for i in range(0,MATRICES):
        matrix[i].writeDisplay()

    time.sleep(60)
