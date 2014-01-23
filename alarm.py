#!/usr/bin/python
# Example code to test scrolling text across multiple 8x8 matrices.
# WARNING! Make sure to use a level shifter between the Raspberry Pi
# and matrices running at 5v to avoid overpowering the Pi.

import os, sys
import RPi.GPIO as GPIO
import time
import random
lib_path = os.path.abspath('lib/Adafruit/Adafruit_LEDBackpack/')
sys.path.append(lib_path)
from Adafruit_8x8 import ColorEightByEight
from AlarmClock import AlarmClock
from Skynet import Skynet
from KrakenMaster import KrakenMaster

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

ledbtns = []
#Green
ledbtns.append({'id' : 1, 'color' : 'green', 'led' : 11, 'button' : 12})
#Yellow
ledbtns.append({'id' : 1, 'color' : 'yellow', 'led' : 13, 'button' : 16})
#Red
ledbtns.append({'id' : 1, 'color' : 'red', 'led' : 15, 'button' : 18})

LEDBTNON = GPIO.LOW
LEDBTNOFF = GPIO.HIGH

DEBUG=False

for elm in ledbtns:
    GPIO.setup(elm['led'], GPIO.OUT, initial=LEDBTNOFF)
    GPIO.setup(elm['button'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

BTNDELAY = 100 # In milliseconds
SHUTOFFPROMPTDELAY = 30000 #  In milliseconds
GAMEPRESSES = 2 

kraken = KrakenMaster(debug=DEBUG)
skynet = Skynet(debug=DEBUG)
skynet.send_message(message={"status" : "Booted Up!"})

MATRICES = 5
matrix = []

alarm = AlarmClock(debug=DEBUG)

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
        #matrix[i].clear() #This was causing flickering
        matrix[i].setCursor(x - i * 8, 1)
        matrix[i].printMessage(message)
        matrix[i].setTextColor(alarm.get_color(), alarm.get_bg())
    
    # Write data to matrices in separate loop so it's less jumpy
    for i in range(0,MATRICES):
        matrix[i].writeDisplay()

def play_game():
    skynet.send_message(message={'status':'Alarm Triggered'})
    #Start Game
    for i in range(0, GAMEPRESSES):
        #Get Random LEDBUTTON
        if ledbtns:
            current = random.choice(ledbtns);
        else:
            if DEBUG:
                print('Bad LEDBTNS data')
                print(ledbtns)
            return False
        #Turn it on
        GPIO.output(current['led'], LEDBTNON);
        not_pressed = True
        if DEBUG:
            print(current);
        #Wait until it is pressed
        s = 0
        while not_pressed:
            get_input = GPIO.input(current['button'])
            if not get_input:
                if DEBUG:
                    print('Pressed!!!');
                not_pressed = False
                #TURN LIGHT OFF
                GPIO.output(current['led'], LEDBTNOFF)
                time.sleep(1)
            #Update Display
            if not s % 100:
                update_matrixes()
            s += 1
            #Sleep
            time.sleep(BTNDELAY / 1000)
    # Shut off sound    
    alarm.tigger_sound(False)
    #Sleep then ask to turn off alarm else snooze
    time.sleep(1)

    #Turn On LEDs
    for elm in ledbtns:
        GPIO.output(elm['led'], LEDBTNOFF)
        GPIO.output(elm['led'], LEDBTNON)

    tmp_btns = ledbtns
    if DEBUG:
        print(tmp_btns)
    time_elapsed = 0
    if DEBUG:
        print('Pre-Final Game %i / %i ' % ((len(tmp_btns) > 0), time_elapsed < SHUTOFFPROMPTDELAY))
    s = 0
    while len(tmp_btns) > 0 and  time_elapsed < SHUTOFFPROMPTDELAY:
        if DEBUG:
            print('Final Game %i / %i ' % ((len(tmp_btns) > 0), time_elapsed < SHUTOFFPROMPTDELAY))
        key = 0
        if not s % 100:
            update_matrixes()
        for elm in tmp_btns:
            #Else check for button input
            if not GPIO.input(elm['button']):
                if DEBUG:
                    print('Button Pressed')
                GPIO.output(elm['led'], LEDBTNOFF)
                tmp_btns.pop(key)
                if DEBUG:
                    print(tmp_btns)  
            key += 1
        #Sleep
        s += 1
        time_elapsed += BTNDELAY
        time.sleep(BTNDELAY / 1000)

    if len(tmp_btns) == 0:
        #Stop Alarm
        skynet.send_message(message={'status':'Alarm Stopped'})
        grade = alarm.stop_alarm()
        kraken.create_grade(grade)
    else:
        #Set Snooze
        alarm.set_snooze()

def update_settings():
    settings = kraken.get_settings()
    if settings:
        if not settings['alarm_status']:
            alarm.set_alarm('00:00') # Set Alarm time something that will never happen
            return True
        hrs = settings['alarm_hours']
        mins = settings['alarm_minutes']
        if hrs < 10:
            hrs = "0" + str(hrs)
        if mins < 10:
            mins = "0" + str(mins)
        if not DEBUG:
            alarm.set_alarm(str(hrs) + ':' + str(mins))
        alarm.set_alarm_text(str(settings['alarm_text']))
        if not DEBUG:
            alarm.set_snooze_time(settings['snooze_minutes'])
        return True
    return False
# Horiz. position of text -- starts off right edge
x = 2
iter = 0
settings_check = 0
loop_delay = 1
try:
    while True:
        # Update Display
        update_matrixes()

        #Update Settings if needed
        if not settings_check:
            if update_settings():
                if DEBUG:
                    print("Successfully updated settings.")
                settings_check = 60 * 60 # Try again 1 hour
            else:
                if DEBUG:
                    print("Unable to set settings.")
                settings_check = 60 * 3 # Try again in 3 min
            
        if alarm.check_alarm():
            #If alarm is triggered play game
            play_game()
        #Sleep for second before updating the display
        settings_check -= loop_delay
        time.sleep(loop_delay)
except KeyboardInterrupt:
    print 'Keyboad is Interrupted'
#except:
#   print 'Other error has occurred'
finally:
    for i in range(0,MATRICES):
        matrix[i].clear()
    GPIO.cleanup()
    alarm.self_destruct()
    
    
