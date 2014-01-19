#!/usr/bin/python
# Example code to test scrolling text across multiple 8x8 matrices.
# WARNING! Make sure to use a level shifter between the Raspberry Pi
# and matrices running at 5v to avoid overpowering the Pi.

import time
from Adafruit_8x8 import ColorEightByEight

MATRICES = 4
matrix = []

for i in range(0,MATRICES):
    matrix.append(ColorEightByEight(address=0x70+i))
    matrix[i].setTextWrap(False) # Allow text to run off edges
    matrix[i].setRotation(3)
    matrix[i].setBrightness(4)
    matrix[i].setTextSize(1)

#message = 'Hello World!!!'
message = 'Super Sweet!!!'

# Horiz. position of text -- starts off right edge
x = 8 * MATRICES

while True:
    for i in range(0,MATRICES):
        # Draw message in each matrix buffer, offseting each by 8 pixels
        matrix[i].clear()
        matrix[i].setCursor(x - i * 8, 1)
        matrix[i].printMessage(message)
    
    # Write data to matrices in separate loop so it's less jumpy
    for i in range(0,MATRICES):
        matrix[i].writeDisplay()
        
    #print('Test')
    
    # Move text position left by 1 pixel.
    # When it's completely gone off left edge, start over off right.
    length = len(message) * 6 * matrix[i].getTextSize()
    x -= 1
    if(x < -(length)):
        x = 8 * MATRICES

    time.sleep(0.15)
