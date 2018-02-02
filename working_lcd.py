#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#  lcd_16x2.py
#  16x2 LCD Test Script
#
# Author : Matt Hawkins
# Date   : 06/04/2015
#
# https://www.raspberrypi-spy.co.uk/
#
#--------------------------------------

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

# Define GPIO to LCD mapping
LCD_RS = 37
LCD_E  = 35
LCD_D4 = 40
LCD_D5 = 38
LCD_D6 = 36
LCD_D7 = 32    

# Define some device constants
#LCD_WIDTH = 16    # Maximum characters per line
#LCD_CHR = True
#LCD_CMD = False

# Timing constants
E_PULSE = 0.001
E_DELAY = 0.001

#import
import RPi.GPIO as GPIO
import time

class LCD():

    def __init__(self):
        
                       
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)       # Use BOARD GPIO numbers
        GPIO.setup(LCD_E, GPIO.OUT)  # E
        GPIO.setup(LCD_RS, GPIO.OUT) # RS
        GPIO.setup(LCD_D4 , GPIO.OUT) # DB4
        GPIO.setup(LCD_D5, GPIO.OUT) # DB5
        GPIO.setup(LCD_D6, GPIO.OUT) # DB6
        GPIO.setup(LCD_D7, GPIO.OUT) # DB7
        
        # Initialise display
        self.lcd_byte(0x33,False) # 110011 Initialise
        self.lcd_byte(0x32,False)# 110010 Initialise
        self.lcd_byte(0x06,False) # 000110 Cursor move direction
        self.lcd_byte(0x0C,False) # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28,False) # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01,False) # 000001 Clear display
        time.sleep(E_DELAY)
    

    def lcd_string(self,message,line):
        # Send string to display
    
        message = message.ljust(16," ")
    
        self.lcd_byte(line, False)
    
        for i in range(16):
            self.lcd_byte(ord(message[i]),True)
            
            
    
    def lcd_byte(self,bits, mode):
        # Send byte to data pins
        # bits = data
        # mode = True  for character
        #        False for command
    
        GPIO.output(LCD_RS, mode) # RS
    
        # High bits
        GPIO.output(LCD_D4 , False)
        GPIO.output(LCD_D5, False)
        GPIO.output(LCD_D6, False)
        GPIO.output(LCD_D7, False)
        if bits&0x10:
            GPIO.output(LCD_D4 , True)
        if bits&0x20:
            GPIO.output(LCD_D5, True)
        if bits&0x40:
            GPIO.output(LCD_D6, True)
        if bits&0x80:
            GPIO.output(LCD_D7, True)
    
        # Toggle 'Enable' pin
        self.lcd_toggle_enable()
    
        # Low bits
        GPIO.output(LCD_D4 , False)
        GPIO.output(LCD_D5, False)
        GPIO.output(LCD_D6, False)
        GPIO.output(LCD_D7, False)
        if bits&0x01:
            GPIO.output(LCD_D4 , True)
        if bits&0x02:
            GPIO.output(LCD_D5, True)
        if bits&0x04:
            GPIO.output(LCD_D6, True)
        if bits&0x08:
            GPIO.output(LCD_D7, True)
    
        # Toggle 'Enable' pin
        self.lcd_toggle_enable()
    
    def lcd_toggle_enable(self):
        # Toggle enable
        time.sleep(E_PULSE )
        GPIO.output(LCD_E, True)
        time.sleep(E_DELAY)
        GPIO.output(LCD_E, False)
        time.sleep(E_PULSE )        
     
