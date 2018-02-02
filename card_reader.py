import serial
import logging
import time
from button import Report_Button
from working_lcd import LCD
from datetime import datetime, timedelta
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line


class CardReader:

    def __init__(self,logger=logging.getLogger(__name__)):
        self.logger = logger
        #Open COM port
        port = "/dev/ttyACM0" #hardcoded for linux
        self.ser = serial.Serial(port,baudrate=9600,parity=serial.PARITY_ODD,stopbits=serial.STOPBITS_TWO,bytesize=serial.SEVENBITS)
        self.logger.info("{p} port established".format(p = port))		

    def get_tag_id_off(self):
        
        f = open('device_config.txt','r')
        previous_line = ''
        for line in f:   
            if ('_device' in previous_line):
                if (line == '\n'):
                    pass      
                else:
                    device_name = line
                    break
            else:    
                previous_line = line 
                
        previous_line = ''
        for line in f:   
            if (previous_line in device_name):
                if (line == '\n'):
                    pass      
                else:
                    device_id = line[3:4]
                    break
            else:    
                previous_line = line     
                
        tag_length = 14
        self.ser.read(self.ser.inWaiting()) #flushing the system.
        time.sleep(0.1)
        while(self.ser.inWaiting()>0):
            self.ser.read(self.ser.inWaiting()) #flushing the system.
            self.logger.debug("Data still coming in - Flushing Loop")
            time.sleep(0.1)
        self.logger.debug("Waiting for Data")
        report_button = Report_Button();
        lcd = LCD();
        
        while(self.ser.inWaiting()<tag_length):
            t = datetime.now().time()
            t = str(t)
            (h, m, s) = t.split(':')
            value = int(h) * 100 + int(m) * 10 +200              
            if (value == 500):
                list_dowload = listDownload();
                listDownload.download();            
            dt = datetime.now() + timedelta(hours = 2)
            
            button_push = report_button.button_push()
            
            lcd.lcd_string("Time: %s" %dt.strftime("%H:%M:%S"),LCD_LINE_1)   
            lcd.lcd_string("ID="+device_id,LCD_LINE_2)
            button_push = report_button.button_push()
            
            if (button_push == True):
                return 1    
            
            if(self.ser.inWaiting()>tag_length):
                break       
            
            
            time.sleep(1)
            
            if(self.ser.inWaiting()>tag_length):
                break
            
            button_push = report_button.button_push()   
            
            lcd.lcd_string("Swipe Card",LCD_LINE_1)  
            
            button_push = report_button.button_push()
            
            if(self.ser.inWaiting()>tag_length):
                break            
            
            time.sleep(1)
            if(self.ser.inWaiting()>tag_length):
                break
            
            button_push = report_button.button_push()
                            
        value = self.ser.read(tag_length)
        value = value.decode("utf-8")
        value = int(value[1:-3],16)
        self.logger.debug("Value: {v}".format(v = value))
        return value #returns tag value

    def get_tag_id(self):
        tag_length = 14
        self.ser.read(self.ser.inWaiting()) #flushing the system.
        time.sleep(0.1)
        while(self.ser.inWaiting()>0):
            self.ser.read(self.ser.inWaiting()) #flushing the system.
            self.logger.debug("Data still coming in - Flushing Loop")
            time.sleep(0.1)
        self.logger.debug("Waiting for Data")

        while(self.ser.inWaiting()<tag_length):
            pass                          
        value = self.ser.read(tag_length)
        value = value.decode("utf-8")
        value = int(value[1:-3],16)
        self.logger.debug("Value: {v}".format(v = value))
        return value #returns tag value

    def get_tag_id_on(self,info):
        f = open('device_config.txt','r')
        previous_line = ''
        for line in f:   
            if ('_device' in previous_line):
                if (line == '\n'):
                    pass      
                else:
                    device_name = line
                    break
            else:    
                previous_line = line 
                
        previous_line = ''
        for line in f:   
            if (previous_line in device_name):
                if (line == '\n'):
                    pass      
                else:
                    device_id = line[3:4]
                    break
            else:    
                previous_line = line     
                
        lcd = LCD();
        report_button = Report_Button();
        tag_length = 14
        self.ser.read(self.ser.inWaiting()) #flushing the system.
        time.sleep(0.1)
        while(self.ser.inWaiting()>0):
            self.ser.read(self.ser.inWaiting()) #flushing the system.
            self.logger.debug("Data still coming in - Flushing Loop")
            time.sleep(0.1)
        self.logger.debug("Waiting for Data")                
        while(self.ser.inWaiting()<tag_length):
            dt = datetime.now() + timedelta(hours = 2)
            
            button_push = report_button.button_push()
            
            lcd.lcd_string("Time: %s" %dt.strftime("%H:%M:%S"),LCD_LINE_1)  
            lcd.lcd_string(info + " ID="+device_id,LCD_LINE_2)
                        
            
            button_push = report_button.button_push()   
            
            if(self.ser.inWaiting()>tag_length):
                break
            
            time.sleep(1)
            if(self.ser.inWaiting()>tag_length):
                break
            
            button_push = report_button.button_push()
            
            if (button_push == True):
                return 1                         
            
            lcd.lcd_string("Swipe Card",LCD_LINE_1)  
            lcd.lcd_string("to log off",LCD_LINE_2)
            
            button_push = report_button.button_push()
            
            if(self.ser.inWaiting()>tag_length):
                break 
            
            time.sleep(1)
                
            if(self.ser.inWaiting()>tag_length):
                break
            
            button_push = report_button.button_push()   
            
        value = self.ser.read(tag_length)
        value = value.decode("utf-8")
        value = int(value[1:-3],16)
        self.logger.debug("Value: {v}".format(v = value))
        return value #returns tag value