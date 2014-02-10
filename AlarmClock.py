#!/usr/bin/python

import time
import pygame
import math

class AlarmClock(object):
    COLOR_TRANSPARENT=0
    COLOR_GREEN=1
    COLOR_RED=2
    COLOR_YELLOW=3
    current_color=1
    bg_color=0
    alarm_time='06:30'
    org_alarm_time='06:30'
    alarm_text='ALARM!'
    snooze_time=1
    org_snooze_time=10
    snooze_count=0
    start=0
    end=0
    debug=False
    flash=True
    sound='/home/pi/alarm.mp3'
    alarm_triggered=False
    sound_paused=True

    def __init__(self, debug=False):
        self.debug=debug
        #copy over originals
        self.org_alarm_time=self.alarm_time
        self.org_snooze_time=self.snooze_time
        
        #Debug Set Alarm for 2 minutes from now
        #if(self.debug):
        #    self.set_snooze()

    def set_alarm_text(self, text):
        if self.debug:
            print("Setting Alarm Text to '%s'" % text)
        self.alarm_text = text
        return True
    
    def set_alarm(self, time=False):
        " Set alarm time in Hours : Minutes (05:59) "
        if self.debug:
            print('Setting Alarm Time %s ' % time)
        if(time):
            self.alarm_time=time
        else:
            self.alarm_time=self.get_time()
        self.org_alarm_time=self.alarm_time

    def set_snooze_time(self, mins=10):
        " Set Snooze time, format in minutes "
        self.snooze_time=int(mins)
        self.org_snooze_time=self.snooze_time

    def set_snooze(self):
        " Set snooze "
        if(self.debug):
            print("Setting snooze")
        ++self.snooze_count
        # Increment Alarm Time
        hrs = int(time.strftime('%H'))
        mins = int(time.strftime('%M')) + self.snooze_time
        if(mins > 59):
            r = mins % 60
            hrs += (mins - r) / 60
            mins = r
            if(hrs > 12):
                hrs = hrs - 12
        if(hrs < 10):
            hrs = "0" + str(hrs)
        if(mins < 10):
            mins = "0" + str(mins)
        #Set alarm time
        self.alarm_time="%s:%s"%(hrs, mins)
        if(self.debug):
            print("New Alarm Time %s" % self.alarm_time)
        if(self.snooze_time > 3):
            --self.snooze_time
        self.alarm_triggered=False
        #Stop Sound
        self.trigger_sound(False)

    def stop_alarm(self):
        " Stop Alarm and reset object "
        if(self.debug):
            print("Stopping alarm")
        self.alarm_triggered=False
        self.end = time.time()
        if self.org_alarm_time == self.get_time():
            self.alarm_time=self.set_time_plus()
        else:
            self.alarm_time=self.org_alarm_time
        self.snooze_time=self.org_snooze_time
        self.trigger_sound(False)
        data = {'end' : int(round(self.end)), 'start' : int(round(self.start)), 'snooze_count' : self.snooze_count}
        self.end = 0
        self.start = 0
        self.snooze_count = 0
        return data

    def set_time_plus(minutes=1, time=False):
        if not time:
            time = self.org_alarm_time
        arr = time.split(':')
        hrs = int(arr[0]);
        mins = int(arr[1])
        mins += minutes
        if hrs < 10:
            hrs = str('0') + str(hrs)
        if mins < 10:
            mins = str('0') + str(mins)
        return hrs + ':' + mins

    def start_alarm(self):
        " Start the Alarm "
        if(self.debug):
            print("Starting alarm " + self.get_time())
        self.trigger_sound(True)
        self.start = time.time()
        self.alarm_triggered = True

    def self_destruct(self):
        ' Stop Sound '
        pygame.mixer.stop()
        pygame.mixer.quit()
    
    def trigger_sound(self, on):
        " Trigger Sound "
        if pygame.mixer.get_init() == None:
            pygame.mixer.init()
            pygame.mixer.music.load(self.sound)
        if on:
            if not self.sound_paused:
                return
            if self.debug:
                print("Playing sound")
            # Play sound up to 25 times
            self.sound_paused=False
            pygame.mixer.music.play(25)
        else:
            if(self.debug):
                print("Pausing sound")
            # Pause sound
            self.sound_paused=True
            pygame.mixer.music.stop()

    def get_time(self):
        " Get Time "
        return time.strftime("%H:%M")
    
    def get_dsp_time(self):
        " GetDisplay Time "
        return time.strftime("%I:%M%p")[:-1]

    def is_am(self):
        " Returns true if it is AM "
        return time.strftime("%p") == 'AM'

    def check_alarm(self):
        " Check to see if the alarm should be triggered "
        if self.alarm_triggered:
            return True
        if self.get_time() == self.alarm_time:
            return True
        return False

    def display_msg(self):
        " Get the Current Display MSG"
        self.set_colors()
        if(self.check_alarm()):
            if not self.alarm_triggered:
                self.start_alarm()
            return self.alarm_text
        else:
            return self.get_dsp_time()

    def set_colors(self):
        " Get the Current Colors "
        #Set the default BG to transparent
        self.bg_color=self.COLOR_TRANSPARENT
        if(self.is_am()):
            self.current_color=self.COLOR_GREEN
        else:
            self.current_color=self.COLOR_YELLOW
        #Check if alarm triggered
        if(self.check_alarm()):
            if(self.flash):
                self.current_color=self.COLOR_TRANSPARENT
                self.bg_color=self.COLOR_RED
                self.flash=False
            else:
                self.current_color=self.COLOR_RED
                self.bg_color=self.COLOR_TRANSPARENT
                self.flash=True

    def get_color(self):
        " Get the Current Color "
        return self.current_color

    def get_bg(self):
        " Get the Current BG "
        return self.bg_color
