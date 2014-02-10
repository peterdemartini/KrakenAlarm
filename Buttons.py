import RPi.GPIO as GPIO
import random
import time

LEDBTNON = GPIO.LOW
LEDBTNOFF = GPIO.HIGH

BTNDELAY = 100 # In milliseconds



class Buttons(object):
    
    ledbtns = True
    debug = False
    
    def __init__(self, debug=False):
        self.debug = debug;
        self.setup_buttons();
    
    def setup_buttons(self):
        if not self.ledbtns:
            GPIO.cleanup()
            
        self.ledbtns = []
        #Green
        self.ledbtns.append({'id' : 1, 'color' : 'green', 'led' : 11, 'button' : 12})
        #Yellow
        self.ledbtns.append({'id' : 1, 'color' : 'yellow', 'led' : 13, 'button' : 16})
        #Red
        self.ledbtns.append({'id' : 1, 'color' : 'red', 'led' : 15, 'button' : 18})
    
        for elm in self.ledbtns:
            GPIO.setup(elm['led'], GPIO.OUT, initial=LEDBTNOFF)
            GPIO.setup(elm['button'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    def turn_off_all(self):
        for elm in self.ledbtns:
            GPIO.output(elm['led'], LEDBTNOFF)

    def turn_on_all(self):
        for elm in self.ledbtns:
            GPIO.output(elm['led'], LEDBTNOFF)
            GPIO.output(elm['led'], LEDBTNON)
            
    def get_random(self):
        return random.choice(self.ledbtns);
        
    def trigger_random(self, alarm, mtx, timeout):
        current = self.get_random();
        #Turn it on
        GPIO.output(current['led'], LEDBTNON);
        not_pressed = True

        #Wait until it is pressed
        s = 0
        while not_pressed and timeout > s:
            get_input = GPIO.input(current['button'])
            if not get_input:
                if self.debug:
                    print('Pressed!!!');
                not_pressed = False
                #TURN LIGHT OFF
                GPIO.output(current['led'], LEDBTNOFF)
                time.sleep(1)
            #Update Display
            if not s % 300:
                mtx.display_msg(message=alarm.display_msg(), color=alarm.get_color(), bg=alarm.get_bg())
            s += 1
            #Sleep
            time.sleep(BTNDELAY / 1000)
            
    def tigger_all(self, alarm, mtx, timeout):
        tmp_btns = self.ledbtns
        if self.debug:
            print(tmp_btns)
        time_elapsed = 0
        if self.debug:
            print('Pre-Final Game %i / %i ' % ((len(tmp_btns) > 0), time_elapsed < SHUTOFFPROMPTDELAY))
        s = 0
        starttime = time.time()
        while len(tmp_btns) > 0 and  time_elapsed < timeout:
            key = 0
            if not s % 100:
                if False:
                    print('Time elapsed %i ' % (time.time() - starttime))
                    print('Final Game %i / %i ' % ((len(tmp_btns) > 0), time_elapsed < SHUTOFFPROMPTDELAY))
                time_left = round(timeout - (time.time() - starttime))
                if time_left > 60:
                    time_left = str(round(time_left / 60)) + 'M'
                time_left_str = str("OFF ") + str(int(time_left))
                if self.debug:
                    print(time_left_str)
                mtx.display_msg(message=time_left_str.ljust(6, ' '), color=2, bg=0)
            for elm in tmp_btns:
                #Else check for button input
                if not GPIO.input(elm['button']):
                    if self.debug:
                        print('Button Pressed')
                    GPIO.output(elm['led'], LEDBTNOFF)
                    tmp_btns.pop(key)
                    if self.debug:
                        print(tmp_btns)  
                key += 1
            #Sleep
            s += 1
            time_elapsed = time.time() - starttime
            time.sleep(BTNDELAY / 1000)
        return len(tmp_btns) == 0
