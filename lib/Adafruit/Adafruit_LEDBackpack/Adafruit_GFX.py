#!/usr/bin/python

#/******************************************************************
# This is the core graphics library for all our displays, providing
# basic graphics primitives (points, lines, circles, etc.). It needs
# to be paired with a hardware-specific library for each display
# device we carry (handling the lower-level functions).
# Adafruit invests time and resources providing this open
# source code, please support Adafruit and open-source hardware
# by purchasing products from Adafruit!
# Written by Limor Fried/Ladyada for Adafruit Industries.
# BSD license, check license.txt for more information.
# All text above must be included in any redistribution.
#
# Port of library from the C++ library for Arduino
# 6/6/2013 - R Heironimus (cameraready)
#******************************************************************/

#import time
from glcdfont import glcdfont


class Adafruit_GFX(object):

    def __init__(self, w, h):
        self.WIDTH = w
        self.HEIGHT = h
        self._width = w
        self._height = h

        self.rotation = 0
        self.cursor_x = 0
        self.cursor_y = 0
        
        self.textsize = 1
        self.textcolor = 0xFFFF
        self.textbgcolor = 0xFFFF
        
        self.wrap = True
        self.font = glcdfont().getfont()
    
    #  this must be defined by the subclass
    def drawPixel(self, x, y, color):
        pass
    
    def invertDisplay(self, i):
        pass

    # bresenham's algorithm - thx wikpedia
    def drawLine(self, x0, y0, x1, y1, color=1):
        steep = abs(y1 - y0) > abs(x1 - x0)
        if (steep):
            x0, y0 = self.swap(x0, y0)
            x1, y1 = self.swap(x1, y1)

        if (x0 > x1):
            x0, x1 = self.swap(x0, x1)
            y0, y1 = self.swap(y0, y1)

        dx = x1 - x0
        dy = abs(y1 - y0)
        err = dx / 2

        if (y0 < y1):
            ystep = 1
        else:
            ystep = -1

        while (x0 <= x1):
            if (steep):
                self.drawPixel(y0, x0, color)
            else:
                self.drawPixel(x0, y0, color)

            err -= dy
            if (err < 0):
                y0 += ystep
                err += dx
                
            x0 += 1

    def drawFastVLine(self, x, y, h, color=1):
        # stupidest version - update in subclasses if desired!
        self.drawLine(x, y, x, y+h-1, color)
        
    def drawFastHLine(self, x, y, w, color=1):
        #stupidest version - update in subclasses if desired!
        self.drawLine(x, y, x+w-1, y, color)

    # draw a rectangle
    def drawRect(self, x, y, w, h, color=1):
        self.drawFastHLine(x, y, w, color)
        self.drawFastHLine(x, y+h-1, w, color)
        self.drawFastVLine(x, y, h, color)
        self.drawFastVLine(x+w-1, y, h, color)
            
    def fillRect(self, x, y, w, h, color=1):
        # stupidest version - update in subclasses if desired!
        for i in range(x, x+w):
            self.drawFastVLine(i, y, h, color)
    
    def fillScreen(self, color=1):
        self.fillRect(0, 0, self._width, self._height, color)

    # draw a circle outline
    def drawCircle(self, x0, y0, r, color=1):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r

        self.drawPixel(x0, y0+r, color);
        self.drawPixel(x0, y0-r, color);
        self.drawPixel(x0+r, y0, color);
        self.drawPixel(x0-r, y0, color);

        while (x<y):
            if (f >= 0):
                y -= 1
                ddF_y += 2
                f += ddF_y

            x += 1
            ddF_x += 2
            f += ddF_x

            self.drawPixel(x0 + x, y0 + y, color)
            self.drawPixel(x0 - x, y0 + y, color)
            self.drawPixel(x0 + x, y0 - y, color)
            self.drawPixel(x0 - x, y0 - y, color)
            self.drawPixel(x0 + y, y0 + x, color)
            self.drawPixel(x0 - y, y0 + x, color)
            self.drawPixel(x0 + y, y0 - x, color)
            self.drawPixel(x0 - y, y0 - x, color)
            
    def drawCircleHelper(self, x0, y0, r, cornername, color=1):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r

        while (x<y):
            if (f >= 0):
                y -= 1
                ddF_y += 2
                f += ddF_y

            x += 1
            ddF_x += 2
            f += ddF_x
            if (cornername & 0x4):
                self.drawPixel(x0 + x, y0 + y, color)
                self.drawPixel(x0 + y, y0 + x, color)

            if (cornername & 0x2):
                self.drawPixel(x0 + x, y0 - y, color)
                self.drawPixel(x0 + y, y0 - x, color)

            if (cornername & 0x8):
                self.drawPixel(x0 - y, y0 + x, color)
                self.drawPixel(x0 - x, y0 + y, color)

            if (cornername & 0x1):
                self.drawPixel(x0 - y, y0 - x, color)
                self.drawPixel(x0 - x, y0 - y, color)

    def fillCircle(self, x0, y0, r, color=1):
        self.drawFastVLine(x0, y0-r, 2*r+1, color)
        self.fillCircleHelper(x0, y0, r, 3, 0, color)
        
    # used to do circles and roundrects!
    def fillCircleHelper(self, x0, y0, r, cornername, delta, color=1):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r

        while (x<y):
            if (f >= 0):
                y -= 1
                ddF_y += 2
                f += ddF_y
                
            x += 1
            ddF_x += 2
            f += ddF_x

            if (cornername & 0x1):
                self.drawFastVLine(x0+x, y0-y, 2*y+1+delta, color)
                self.drawFastVLine(x0+y, y0-x, 2*x+1+delta, color)

            if (cornername & 0x2):
                self.drawFastVLine(x0-x, y0-y, 2*y+1+delta, color)
                self.drawFastVLine(x0-y, y0-x, 2*x+1+delta, color)

    # Draw a triangle!
    def drawTriangle(self, x0, y0, x1, y1, x2, y2, color=1):
        self.drawLine(x0, y0, x1, y1, color)
        self.drawLine(x1, y1, x2, y2, color)
        self.drawLine(x2, y2, x0, y0, color)
        
    # fill a triangle!
    def fillTriangle(self, x0, y0, x1, y1, x2, y2, color=1):
        # Sort coordinates by Y order (y2 >= y1 >= y0)
        if (y0 > y1):
            y0, y1 = self.swap(y0, y1)
            x0, x1 = self.swap(x0, x1)

        if (y1 > y2):
            y2, y1 = self.swap(y2, y1)
            x2, x1 = self.swap(x2, x1)

        if (y0 > y1):
            y0, y1 = self.swap(y0, y1)
            x0, x1 = self.swap(x0, x1)

        if(y0 == y2): # Handle awkward all-on-same-line case as its own thing
            a = x0
            b = x0
            if(x1 < a):
                a = x1
            elif(x1 > b):
                b = x1
            if(x2 < a):
                a = x2
            elif(x2 > b):
                b = x2
            self.drawFastHLine(a, y0, b-a+1, color)
            return

        dx01 = x1 - x0
        dy01 = y1 - y0
        dx02 = x2 - x0
        dy02 = y2 - y0
        dx12 = x2 - x1
        dy12 = y2 - y1
        sa = 0
        sb = 0

        # For upper part of triangle, find scanline crossings for segments
        # 0-1 and 0-2. If y1=y2 (flat-bottomed triangle), the scanline y1
        # is included here (and second loop will be skipped, avoiding a /0
        # error there), otherwise scanline y1 is skipped here and handled
        # in the second loop...which also avoids a /0 error here if y0=y1
        # (flat-topped triangle).
        if(y1 == y2): # true
            last = y1 # Include y1 scanline
        else:
            last = y1-1 # Skip it

        y = y0
        for y in range(y0, last+1): # 0, 8 (not skipped)
            a = x0 + sa / dy01
            b = x0 + sb / dy02
            sa += dx01
            sb += dx02
            #/* longhand:
            #a = x0 + (x1 - x0) * (y - y0) / (y1 - y0);
            #b = x0 + (x2 - x0) * (y - y0) / (y2 - y0);
            #*/
            if(a > b):
                a,b = self.swap(a,b)
            self.drawFastHLine(a, y, b-a+1, color)

        y += 1 # added this line since python for loops don't increment the variable on the last pass - RH
        # For lower part of triangle, find scanline crossings for segments
        # 0-2 and 1-2. This loop is skipped if y1=y2.
        sa = dx12 * (y - y1)
        sb = dx02 * (y - y0)
        for y in range(y,y2+1):
            a = x1 + sa / dy12
            b = x0 + sb / dy02
            sa += dx12
            sb += dx02
            #/* longhand:
            #a = x1 + (x2 - x1) * (y - y1) / (y2 - y1);
            #b = x0 + (x2 - x0) * (y - y0) / (y2 - y0);
            #*/
            if(a > b):
                a,b = self.swap(a,b)
            self.drawFastHLine(a, y, b-a+1, color)
    
    # draw a rounded rectangle!
    def drawRoundRect(self, x, y, w, h, r, color=1):
        # smarter version
        self.drawFastHLine(x+r , y , w-2*r, color) # Top
        self.drawFastHLine(x+r , y+h-1, w-2*r, color) # Bottom
        self.drawFastVLine( x , y+r , h-2*r, color) # Left
        self.drawFastVLine( x+w-1, y+r , h-2*r, color) # Right
        # draw four corners
        self.drawCircleHelper(x+r , y+r , r, 1, color)
        self.drawCircleHelper(x+w-r-1, y+r , r, 2, color)
        self.drawCircleHelper(x+w-r-1, y+h-r-1, r, 4, color)
        self.drawCircleHelper(x+r , y+h-r-1, r, 8, color)
    
    # fill a rounded rectangle!
    def fillRoundRect(self, x, y, w, h, r, color=1):
        # smarter version
        self.fillRect(x+r, y, w-2*r, h, color)

        # draw four corners
        self.fillCircleHelper(x+w-r-1, y+r, r, 1, h-2*r-1, color)
        self.fillCircleHelper(x+r , y+r, r, 2, h-2*r-1, color)

    #def drawBitmap(int16_t x, int16_t y, const uint8_t *bitmap, int16_t w, int16_t h, uint16_t color):
    
    def write(self, c):
        if (c == '\n'):
            self.cursor_y += textsize*8
            self.cursor_x = 0
        elif (c == '\r'):
            pass # skip em
        else:
            self.drawChar(self.cursor_x, self.cursor_y, c, self.textcolor, self.textbgcolor, self.textsize)
            self.cursor_x += self.textsize*6
            if (self.wrap and (self.cursor_x > (self._width - self.textsize*6))):
                self.cursor_y += self.textsize*8
                self.cursor_x = 0

    # self.draw a character
    def drawChar(self, x, y, c, color, bg, size):
        if ((x >= self._width)            or  # Clip right \
            (y >= self._height)           or  # Clip bottom
            ((x + 5 * size - 1) < 0)      or  # Clip left
            ((y + 8 * size - 1) < 0)):        # Clip top
            return

        for i in range(0,6): #(i=0; i<6; i+=1)
            if (i == 5):
                line = 0x0
            else:
                line = self.font[(ord(c)*5)+i] #pgm_read_byte(font+(c*5)+i)
            for j in range(0,8): #(j = 0; j<8; j+=1)
                if (line & 0x1):
                    if (size == 1): # default size
                        self.drawPixel(x+i, y+j, color)
                    else:           # big size
                        self.fillRect(x+(i*size), y+(j*size), size, size, color)
                elif (bg != color):
                    if (size == 1): # default size
                        self.drawPixel(x+i, y+j, bg)
                    else:           # big size
                        self.fillRect(x+i*size, y+j*size, size, size, bg)
                line >>= 1

    def setCursor(self, x, y):
        self.cursor_x = x
        self.cursor_y = y

    def getCursor(self):
        return ('' + str(self.cursor_x) + ',' + str(self.cursor_y))

    def setTextSize(self, s):
        if s > 0:
            self.textsize = s
        else:
            self.textsize = 1
            
    def getTextSize(self):
        return self.textsize

    def setTextColor(self, c):
        self.textcolor = c
        self.textbgcolor = c
        # for 'transparent' background, we'll set the bg 
        # to the same as fg instead of using a flag

    def setTextColor(self, c, b=None):
        self.textcolor = c
        self.textbgcolor = b

    def setTextWrap(self, w):
        self.wrap = w

    def getRotation(self):
        self.rotation %= 4
        return self.rotation

    def setRotation(self, x):
        x %= 4    # cant be higher than 3
        self.rotation = x
        if x == 0 or x == 2:
            self._width = self.WIDTH
            self._height = self.HEIGHT
        elif x == 1 or x == 3:
            self._width = self.HEIGHT
            self._height = self.WIDTH
        else:
            return

    # return the size of the display which depends on the rotation!
    def width(self):
        return self._width

    def height(self):
        return self._height
        
