import RPi.GPIO as GPIO
import time
import logging

class Report_Button:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(33, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #starts false
        
        
        
        
        
        
    def button_push(self):     
        report_button = GPIO.input(33) 
        if (report_button==True):
            print("button pushed")
            return True