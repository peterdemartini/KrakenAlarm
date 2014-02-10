#!/usr/bin/python
# Example code to test scrolling text across multiple 8x8 matrices.
# WARNING! Make sure to use a level shifter between the Raspberry Pi
# and matrices running at 5v to avoid overpowering the Pi.

import RPi.GPIO as GPIO
import time

from AlarmClock import AlarmClock
from Buttons import Buttons
from Matrices import Matrices
from Skynet import Skynet
from KrakenMaster import KrakenMaster

#Set Debug
DEBUG=True

GAMEPRESSES = 3
GAMETIMEOUT= 60 * 10 * 100
SHUTOFFPROMPTDELAY = 30 #  In seconds

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Buttons Object
btns = Buttons(debug=DEBUG);

#Matrixes Object
mtx = Matrices(debug=DEBUG);
mtx.set_matrcies(5);

kraken = KrakenMaster(debug=DEBUG)
skynet = Skynet(debug=False)
skynet.send_message(message={"status" : "Booted Up!"})

alarm = AlarmClock(debug=DEBUG)

mtx.display_msg(message=alarm.display_msg(), color=alarm.get_color(), bg=alarm.get_bg());

# Defintions for Alarm Hardware

def play_game():
    skynet.send_message(message={'status':'Alarm Triggered'})
    #Turn Off LEDs
    btns.turn_off_all();
    
    #Start Game
    for i in range(0, GAMEPRESSES):    
        btns.trigger_random(alarm=alarm, mtx=mtx, timeout=GAMETIMEOUT)
        
    # Shut off sound    
    alarm.set_snooze()
    #Sleep then ask to turn off alarm else snooze
    time.sleep(1)

    #Start Turn off Alarm Logic
    btns.tigger_all(alarm=alarm, mtx=mtx, timeout=SHUTOFFPROMPTDELAY)
    
    #Turn On LEDs
    btns.turn_on_all();

    #Turn Off LEDs
    btns.turn_off_all();
    
    if turned_off:
        #Stop Alarm
        skynet.send_message(message={'status':'Alarm Stopped'})
        grade = alarm.stop_alarm()
        kraken.create_grade(grade)
        

def update_settings():
    settings = kraken.get_settings()
    if settings:
        if not settings['alarm_status']:
            alarm.set_alarm('00:00') # Set Alarm time something that will never happen
            return True
        hrs = settings['alarm_hours']
        mins = settings['alarm_minutes']
        if int(hrs) < 10:
            hrs = "0" + str(hrs)
        if int(mins) < 10:
            mins = "0" + str(mins)
        if DEBUG:
            print(str(hrs) + ':' + str(mins));
        alarm.set_alarm(str(hrs) + ':' + str(mins))
        alarm.set_alarm_text(str(settings['alarm_text']))
        if not DEBUG:
            alarm.set_snooze_time(settings['snooze_minutes'])
        return True
    return False
    
# Horiz. position of text -- starts off right edge
iter = 0
settings_check = 0
loop_delay = 1

try:
    while True:
        # Update Display
        mtx.display_msg(message=alarm.display_msg(), color=alarm.get_color(), bg=alarm.get_bg())

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
    mtx.clear()
    GPIO.cleanup()
    alarm.self_destruct()
    
    
