import os, sys
import RPi.GPIO as GPIO
lib_path = os.path.abspath('lib/Adafruit/Adafruit_LEDBackpack/')
sys.path.append(lib_path)
from Adafruit_8x8 import ColorEightByEight

class Matrices(object):
    
    debug = False
    last_message = False
    num = 5
    matrix = []
    offset = 2
    x = 0
    
    def __init__(self, debug=False):
        self.debug = debug;
        self.x = self.offset
            
    def setup(self):
        ' Setup matrices '
        for i in range(0, self.num):
            self.matrix.append(ColorEightByEight(address=0x70+i))
            self.matrix[i].setTextWrap(False) # Allow text to run off edges
            self.matrix[i].setRotation(3)
            self.matrix[i].setBrightness(1)
            self.matrix[i].setTextSize(1)
    
    def set_matrcies(self, num):
        ' Set Number of Matrices '
        self.num = num
        
    def display_msg(self, message, color, bg):
            
        if message != self.last_message:
            # This means its a new message
            x = 8 * self.num
        
        if len(message) > 6:
            if self.debug: 
                print('TOO LONG')
            too_long=True
        else:
            x = self.offset
            too_long=False
            
        for i in range(0, self.num):
            # Draw message in each matrix buffer, offseting each by 8 pixels
            if too_long:
                self.matrix[i].clear() #This was causing flickering
            self.matrix[i].setCursor(self.x - i * 8, 1)
            self.matrix[i].printMessage(message)
            self.matrix[i].setTextColor(color, bg)
        
        # Write data to matrices in separate loop so it's less jumpy
        for i in range(0, self.num):
            self.matrix[i].writeDisplay()
            
        if too_long:    
            # Move text position left by 1 pixel.
            # When it's completely gone off left edge, start over off right.
            length = len(message) * 6 * self.matrix[i].getTextSize()
            self.x -= 1
            if(self.x < -(length)):
                self.x = 8 * self.num            
        # Update last message
        self.last_message=message
    
    def clear(self):
        for i in range(0,self.num):
            self.matrix[i].clear()
    