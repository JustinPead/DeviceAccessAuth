# the device needs to know its own name
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime, timedelta
class Log:
    def __init__(self):
        
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json.txt',scope)
        client = gspread.authorize(creds)
       
    
    def log_record(self,info):
        
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
                
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json.txt',scope)
        client = gspread.authorize(creds)        
        sheet = client.open('DeviceAccessSheet').worksheet('log')
        sheet.update_cell(1,1,'device name')
        sheet.update_cell(1,2,'student number')     
        sheet.update_cell(1,3,'time logged in') 
        sheet.update_cell(1,4,'device id')   
        #checks for and deletes empty rows
        count = 0
        rows = sheet.row_count+1
        
        for i in range(1,rows):
            a = sheet.row_values(i-count)
            if ('' in a):
                sheet.delete_row(i-count)
                count +=1
               
    
        dt = datetime.now() + timedelta(hours = 2)
        
        sheet.append_row([device_name,info,dt,device_id])

