#import packages

from datetime import  datetime
import pytz
from epdconfig import RaspberryPi
import epd2in7
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import locale
import os
import time


import RPi.GPIO as GPIO


####################
# Define Constants #
####################

#Use saved font as the font for the clock
timefont = os.path.join( os.path.realpath(os.getcwd()), 'CoffeeHealing.ttf')

#save font as a font object, with a large fontsize
timefont = ImageFont.truetype(timefont, 35)


#Pin button numbers
PIN_BTN1 = 5
PIN_BTN2 = 6
PIN_BTN3 = 13
PIN_BTN4 = 19

#Whatever this is
BOUNCETIME = 500

#display states
DISPMODE_IST = 1
DISPMODE_EST = 2
DISPMODE_UK = 3
DISPMODE_PST = 4


######################################
# Wrap everything in a Display Class #
######################################

class Display:
    """
    Define a class called display to wrap all display related functions
    """
    
    #initialise these to None? idk why.
    epd = None
    fonts = None
    #set initial mode. This should be India Time.
    mode = DISPMODE_IND
    
    #this should be removed.
    nobeldata = None
    
    def __init__(self):
        """
        Initialize the damn thing
        """
        
        #this does something about setting where you are. Leave as is for now.
        locale.setlocale(locale.LC_ALL, '')
        

        #initialise the epd2in7's package's function in epd method
        self.epd = epd2in7.EPD()
        self.epd.init()
        
        #read button input on the raspberry pi
        self.read_buttons()
    
    def start(self, start_mode = DISPMODE_IST):
        """
        This function initialises the clock which keeps updating
        """
        self.mode = start_mode

        while True:
            if DISPMODE_IST == self.mode:
                self.draw_ist_data()
            elif DISPMODE_EST == self.mode:
                self.draw_est_data()
            elif DISPMODE_UK == self.mode: 
                self.draw_uk_data()
            elif DISPMODE_PST == self.mode:
                self.draw_pst_data()                    
            else:
                self.mode = DISPMODE_IST
                self.draw_ist_data()                    
            self.sleep_until_next_min()

    def get_time():
        """
        Function to get times from 4 timezones at that second
        """

        #Create format to show time in.
        format = "%I %M %p %a"

        #Set timezones for all places
        tz_india = pytz.timezone("Asia/Kolkata")
        tz_pacific = pytz.timezone("US/Pacific")
        tz_eastern = pytz.timezone("US/Eastern")
        tz_uk = pytz.timezone("Europe/London")

        #Save timezones as their own variables
        time_india = datetime.now(tz= tz_india).strftime(format)
        time_india = "IST " + time_india
        time_pacific = datetime.now(tz= tz_pacific).strftime(format)
        time_pacific = "PST " + time_pacific
        time_eastern = datetime.now(tz= tz_eastern).strftime(format)
        time_eastern = "EST " + time_eastern
        time_uk = datetime.now(tz= tz_uk).strftime(format)
        time_uk = "UK " + time_uk

        return time_india,time_pacific, time_eastern, time_uk                

    def draw_ist_data(self):
        """
        This function graphs time in IST in real time. 
        Note use get_time every time this function is called so the time is 
        updated on every button press. 
        """
        #get ist time
        time = get_time()
        time_now = time[0]
        # Create a new image object (1 bit color and dimensions of the e ink screen. )
        ist_image = Image.new('1', (self.epd.height, self.epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(ist_image)
        draw.text((20, 70), time_now, font = timefont, fill = 0)
        self.epd.display(self.epd.getbuffer(ist_image))    

    def draw_est_data(self):
        """
        This function graphs time in EST in real time. 
        Note use get_time every time this function is called so the time is 
        updated on every button press. 
        """
        #get ist time
        time = get_time()
        time_now = time[2]
        # Create a new image object (1 bit color and dimensions of the e ink screen. )
        est_image = Image.new('1', (self.epd.height, self.epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(est_image)
        draw.text((20, 70), time_now, font = timefont, fill = 0)
        self.epd.display(self.epd.getbuffer(est_image))    

    def draw_uk_data(self):
        """
        This function graphs time in UK in real time. 
        Note use get_time every time this function is called so the time is 
        updated on every button press. 
        """
        #get ist time
        time = get_time()
        time_now = time[3]
        # Create a new image object (1 bit color and dimensions of the e ink screen. )
        uk_image = Image.new('1', (self.epd.height, self.epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(uk_image)
        draw.text((20, 70), time_now, font = timefont, fill = 0)
        self.epd.display(self.epd.getbuffer(uk_image))              
            
    def draw_pst_data(self):
        """
        This function graphs time in PST in real time. 
        Note use get_time every time this function is called so the time is 
        updated on every button press. 
        """
        #get ist time
        time = get_time()
        time_now = time[1]
        # Create a new image object (1 bit color and dimensions of the e ink screen. )
        pst_image = Image.new('1', (self.epd.height, self.epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(pst_image)
        draw.text((20, 70), time_now, font = timefont, fill = 0)
        self.epd.display(self.epd.getbuffer(pst_image))             

    def sleep_until_next_min(self):
        now = datetime.now()
        seconds_until_next_minute = 60 - now.time().second
        time.sleep(seconds_until_next_minute)

    def read_buttons(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_BTN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(PIN_BTN1, GPIO.FALLING, callback=self.button_pressed, bouncetime=BOUNCETIME)
        GPIO.setup(PIN_BTN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(PIN_BTN2, GPIO.FALLING, callback=self.button_pressed, bouncetime=BOUNCETIME)
        GPIO.setup(PIN_BTN3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(PIN_BTN3, GPIO.FALLING, callback=self.button_pressed, bouncetime=BOUNCETIME)
        GPIO.setup(PIN_BTN4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(PIN_BTN4, GPIO.FALLING, callback=self.button_pressed, bouncetime=BOUNCETIME)

    def button_pressed(self, pin):
        if PIN_BTN1 == pin:
            self.mode = DISPMODE_IST
            self.draw_ist_data()
        elif PIN_BTN2 == pin:
            self.mode = DISPMODE_EST            
            self.draw_est_data()
        elif PIN_BTN3 == pin:
            self.mode = DISPMODE_UK
            self.draw_uk_data()
        elif PIN_BTN4 == pin:
            self.mode = DISPMODE_PST            
            self.draw_pst_data()           

if __name__ == '__main__':
    display = Display()
     display.start(DISPMODE_IST)
