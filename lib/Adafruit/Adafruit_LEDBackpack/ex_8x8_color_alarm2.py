#!/usr/bin/python
# Example code to test scrolling text across multiple 8x8 matrices.
# WARNING! Make sure to use a level shifter between the Raspberry Pi
# and matrices running at 5v to avoid overpowering the Pi.

import time
from Adafruit_8x8 import ColorEightByEight

def get_time():
	s = time.strftime("%I:%M")
	if(s[0] == '0'):
		s=s[1:]
        if(time.strftime('%p') == 'AM'):
		s=s+'A'
	else:
		s=s+'P'
	return s

MATRICES = 3
matrix = []
color=2

info_matrix = ColorEightByEight(address=0x73)
info_matrix.setTextWrap(False) # Allow text to run off edges
info_matrix.setRotation(3)
info_matrix.setBrightness(4)
info_matrix.setTextSize(1)

for i in range(0,MATRICES):
    matrix.append(ColorEightByEight(address=0x70+i))
    matrix[i].setTextWrap(False) # Allow text to run off edges
    matrix[i].setRotation(3)
    matrix[i].setBrightness(4)
    matrix[i].setTextSize(1)

#message = 'Hello World!!!'
message = get_time()

# Horiz. position of text -- starts off right edge
x = 0
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

    info_matrix.clear()
    info_matrix.setCursor(2,1)
    info_matrix.printMessage(time.strftime('%p')[0])
    info_matrix.writeDisplay()

    time.sleep(60)
    message = get_time()
