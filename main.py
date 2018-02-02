import time
from datetime import datetime, timedelta
import logging
from card_reader import CardReader
from access_list import AccessList
from timeout import Timeout
from leds import LEDs
from gspread_export import Export
import uct_info
import RPi.GPIO as GPIO
on = False
from working_lcd import LCD
from button import Report_Button
from listDownload import listDownload
from log import Log
#from LCD import LCD
student_name = ''
previous_user = ''
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line


if __name__ == "__main__":
    # create a folder called log using the command mkdir log if you havent done so 
    # already, this code creates a log of people who used the device and cannot do so
    # without a log folder to put it in.
    logging.basicConfig(filename = "./log/file_{t}.log".format(t = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())),
                        level=logging.DEBUG, 
                        format="%(asctime)s:" + logging.BASIC_FORMAT)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter("%(asctime)s:" + logging.BASIC_FORMAT))
    logging.getLogger().addHandler(console)
    logger = logging.getLogger(__name__)
    logger.info("Student Logger has started")
    
    
    
    while(True):# Loop created for retry purposes
      
        lcd = LCD();

        with LEDs() as leds:
            try:
                card_reader = CardReader();              
                export = Export(); 
                export.ID();
                log = Log();
                
                while(True):
                    access_list = AccessList("accesslist.txt",logger.getChild("access_list"));
                    
                    if (on):
                        button = card_reader.get_tag_id_on(info['uct_id']); 
                        lcd.lcd_string("Authenticating",LCD_LINE_1)
                        lcd.lcd_string("",LCD_LINE_2)
                    
                    else:
                        button = card_reader.get_tag_id_off(); #will return 1 if report button is pushed 
                        lcd.lcd_string("Authenticating",LCD_LINE_1)
                        lcd.lcd_string("",LCD_LINE_2)                        
                    
                    
                    if(button == 1):   
                        time.sleep(0.5)
                        report_button = Report_Button()
                        
                        lcd.lcd_string("push again to",LCD_LINE_1)
                        
                        lcd.lcd_string("report",LCD_LINE_2)                      
                        time.sleep(2)  
                        
                        #report button code
                        with Timeout(seconds=50) as t:
                            while(1):
                                
                            
                                    button_push = report_button.button_push();
                                    if (button_push):  
                                        
                                        lcd.lcd_string("button pushed",LCD_LINE_1)
                                        lcd.lcd_string("",LCD_LINE_2)
                                        time.sleep(1)
                                        lcd.lcd_string("Swipe Card",LCD_LINE_1)
                                        lcd.lcd_string("to report",LCD_LINE_2)
                                        reported = access_list.report(previous_user)
                                        tag_id = card_reader.get_tag_id();    
                                            
                                        tag_id = hex(tag_id)
                                        info = uct_info.get_info_from_tag(tag_id)
                                        reported_by = access_list.report(info['uct_id'])                                                                           
                                        reported1 = str(reported)
                                        reported_by1 = str(reported_by)                                                                     
                                        lcd.lcd_string("reporting",LCD_LINE_1)
                                        lcd.lcd_string(reported1,LCD_LINE_2)                                
                                        time.sleep(2)                            
                                        lcd.lcd_string("by"+reported_by1  ,LCD_LINE_1)   
                                        lcd.lcd_string("Reporting",LCD_LINE_1)
                                        dt = datetime.now() + timedelta(hours = 2)
                                        lcd.lcd_string("Time: %s" %dt.strftime("%H:%M:%S"),LCD_LINE_2)
                                        if (reported1 == reported_by1):
                                            reported = access_list.report(double_previous_user)
                                            export.export_info_same(reported, reported_by)
                                        else:
                                            export.export_info(reported, reported_by)
                                        lcd.lcd_string("Reported",LCD_LINE_1)
                                        break
                                        #if reported and reported_by are the same, export the other kind of reported                                    break
                            
                    else:
                        tag_id = button
                    
                    with Timeout(seconds=30) as t:
                        
                        tag_id = hex(tag_id)
                        info = uct_info.get_info_from_tag(tag_id)#as defined above  
                        access_status = access_list.check_allowed(info['uct_id'])
                        admin_status = access_list.admin_access(info['uct_id'])
                        
                        
                        #check workday
                        if (admin_status!=True and access_status == True and on == False):
                            access_status = access_list.check_workday_access(info['uct_id'])
                            if (access_status != True):
                                lcd.lcd_string("You do not have",LCD_LINE_1) 
                                lcd.lcd_string("weekend access",LCD_LINE_1) 
                                time.sleep(2)                            
                        
                        #check ban
                        if (admin_status!=True and access_status == True and on == False):
                            access_status = access_list.check_ban(info['uct_id'])
                            
                            if (access_status != True):
                                lcd.lcd_string("You are banned",LCD_LINE_1) 
                                time.sleep(2)
                                
                        #check time acess
                        if (admin_status!=True and access_status == True and on == False):
                            access_status = access_list.check_time(info['uct_id'])  
                            if (access_status != True):
                                lcd.lcd_string("No access during",LCD_LINE_1) 
                                lcd.lcd_string("this time",LCD_LINE_2) 
                                time.sleep(2)   
                                                       
                                                                        
                                                    
                        #check if on    
                        if (on == True):
                            #switch device off
                            if (admin_status == True or previous_user == info['uct_id']):
                                lcd.lcd_string("Device off",LCD_LINE_1) 
                                lcd.lcd_string("logging exit",LCD_LINE_2)                            
                                leds.switching_device_off();
                                log.log_record_exit(info['uct_id']) 
                                on = False
                            else:
                                lcd.lcd_string("Access Denied",LCD_LINE_1)
                                lcd.lcd_string("",LCD_LINE_2) 
                                leds.red();
                        else:
                            logger.info("Student Number: {name} Access Given: {status}".format(
                                name = info['uct_id'],
                                status = access_status))
                            double_previous_user = previous_user
                            student_name = info['name']
                            previous_user = info['uct_id']
                            
                            #switch device on
                            if(True==access_status or True == admin_status):  
                                lcd.lcd_string("Access Granted",LCD_LINE_1) 
                                lcd.lcd_string("Device on",LCD_LINE_2)                                   
                                leds.switching_device_on();
                                on = True
                                leds.green();
                                lcd.lcd_string("logging entry" ,LCD_LINE_1) 
                                lcd.lcd_string("" ,LCD_LINE_2)
                                log.log_record_entry(info['uct_id'])                                
                                lcd.lcd_string("Welcome" ,LCD_LINE_1)                              
                                lcd.lcd_string(student_name ,LCD_LINE_2)    
                                
                            else:
                                leds.red();
                                lcd.lcd_string("Access Denied",LCD_LINE_1)
                                lcd.lcd_string("",LCD_LINE_2) 
                        time.sleep(4)
                        
                        #admin list download
                                                  
                        if (admin_status == True and on == True):
                            lcd.lcd_string("Downloading list" ,LCD_LINE_1) 
                            lcd.lcd_string("" ,LCD_LINE_2) 
                            list_dowload = listDownload();
                            listDownload.download();                                   
                     
                    
            except Exception as e:
                logger.exception(e)
