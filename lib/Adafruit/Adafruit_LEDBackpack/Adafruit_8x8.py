#!/usr/bin/python
# Updated to allow for scrolling text with the Adafruit_GFX.py library
# ColorEightByEight not updated yet.

from Adafruit_LEDBackpack import LEDBackpack

# ===========================================================================
# 8x8 Pixel Display
# ===========================================================================

class EightByEight(LEDBackpack):
  #disp = None
  rotation = None

  # Constructor
  def __init__(self, address=0x70, debug=False):
    if (debug):
      print "Initializing a new instance of LEDBackpack at 0x%02X" % address
    LEDBackpack.__init__(self, 8, 8, address, debug)
    self.rotation = 0

  def writeRowRaw(self, charNumber, value):
    #"Sets a row of pixels using a raw 16-bit value"
    if (charNumber > 7):
      return
    # Set the appropriate row
    self.setBufferRow(charNumber, value)

  def clearPixel(self, x, y):
    #"A wrapper function to clear pixels (purely cosmetic)"
    self.setPixel(x, y, 0)

  def drawPixel(self, x, y, color=1):
    #"Sets a single pixel"
    if ((y < 0) or (y >= 8)):
      return
    if ((x < 0) or (x >= 8)):
      return    
      
    # Added rotation code 4/16/13 - RH
    if self.rotation == 1:
      x, y = self.swap(x, y)
      x = 8 - x - 1
    elif self.rotation == 2:
      x = 8 - x - 1
      y = 8 - y - 1
    elif self.rotation == 3:
      x, y = self.swap(x, y)
      y = 8 - y - 1

    x += 7   # ATTN: This might be a bug?  On the color matrix, this causes x=0 to draw on the last line instead of the first.
    x %= 8
    # Set the appropriate pixel
    buffer = self.getBuffer()
    if (color):
      self.setBufferRow(y, buffer[y] | 1 << x, False)    # disable update option to determine if writeDisplay() is called when 
    else:                                                # writing a bunch of pixels. Speeds things up dramatically when scrolling 
      self.setBufferRow(y, buffer[y] & ~(1 << x), False) # text on multiple matrices. Call writeDisplay() after updating buffer.
      
  # Used to rotate display 4/16/13 - RH
  # Corrected for dual output 6/5/13 - RH
  def swap(self, x, y):
      temp = x
      x = y
      y = temp
      return (x, y)

  # Added 6/3/13 - RH    
  def printMessage(self, text):
      for letter in range(0, len(text)):
        self.write(text[letter])
        if (self.debug):
            print(text[letter])

class ColorEightByEight(EightByEight):
  def setPixel(self, x, y, color=1):
    #"Sets a single pixel"
    if (x >= 8):
      return
    if (y >= 8):
      return

    x %= 8

    # Set the appropriate pixel
    buffer = self.disp.getBuffer()

    # TODO : Named color constants?
    # ATNN : This code was mostly taken from the arduino code, but with the addition of clearing the other bit when setting red or green.
    #        The arduino code does not do that, and might have the bug where if you draw red or green, then the other color, it actually draws yellow.
    #        The bug doesn't show up in the examples because it's always clearing.

    if (color == 1):
      self.disp.setBufferRow(y, (buffer[y] | (1 << x)) & ~(1 << (x+8)) )
    elif (color == 2):
      self.disp.setBufferRow(y, (buffer[y] | 1 << (x+8)) & ~(1 << x) )
    elif (color == 3):
      self.disp.setBufferRow(y, buffer[y] | (1 << (x+8)) | (1 << x) )
    else:
      self.disp.setBufferRow(y, buffer[y] & ~(1 << x) & ~(1 << (x+8)) )
  def drawPixel(self, x, y, color=1):
    #"Sets a single pixel"
    if ((y < 0) or (y >= 8)):
      return
    if ((x < 0) or (x >= 8)):
      return    
      
    # Added rotation code 4/16/13 - RH
    if self.rotation == 1:
      x, y = self.swap(x, y)
      x = 8 - x - 1
    elif self.rotation == 2:
      x = 8 - x - 1
      y = 8 - y - 1
    elif self.rotation == 3:
      x, y = self.swap(x, y)
      y = 8 - y - 1

    x += 7   # ATTN: This might be a bug?  On the color matrix, this causes x=0 to draw on the last line instead of the first.
    x %= 8
    # Set the appropriate pixel
    buffer = self.getBuffer()
    if (color == 1):
      self.setBufferRow(y, (buffer[y] | (1 << x)) & ~(1 << (x+8)) )
    elif (color == 2):
      self.setBufferRow(y, (buffer[y] | 1 << (x+8)) & ~(1 << x) )
    elif (color == 3):
      self.setBufferRow(y, buffer[y] | (1 << (x+8)) | (1 << x) )
    else:
      self.setBufferRow(y, buffer[y] & ~(1 << x) & ~(1 << (x+8)) )
