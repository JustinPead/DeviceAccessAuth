import RPi.GPIO as GPIO
import time
import logging

class LEDs:
    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger
        GPIO.setmode(GPIO.BOARD)
        #GPIO.setwarnings(False)
        #success LED
        GPIO.setup(13,GPIO.OUT)
        GPIO.output(13,0)
        #On LED
        GPIO.setup(8,GPIO.OUT)
        GPIO.output(8,0)
        #fail LED
        GPIO.setup(12,GPIO.OUT)
        GPIO.output(12,0)
        logging.debug("LEDS initialised")
        #switching on device(relay low active)
        GPIO.setup(7,GPIO.OUT)
        
        
        
    def __enter__(self):
        return self

    #On LED (the blinking led used in the card reader code)
    def orange(self):
        GPIO.output(8,1)
        time.sleep(0.5)
        GPIO.output(8,0)
        time.sleep(2)

    def green(self):
        for _ in range(6):
            GPIO.output(13,1)
            time.sleep(0.3)
            GPIO.output(13,0)
            time.sleep(0.3)
        self.logger.debug("Flashed success LED")

    def red(self):
        for _ in range(6):
            GPIO.output(12,1)
            time.sleep(0.3)
            GPIO.output(12,0)
            time.sleep(0.3)
        logging.info("Flashed failed LED")

    #the relay seems to be a low active so on is 0 and off is 1
    def switching_device_on(self):

        GPIO.output(7,1)
        
        
    def switching_device_off(self):

        GPIO.output(7,0)
        
        
    def __exit__(self, type, value, traceback):
        self.logger.debug("lights exited")
       