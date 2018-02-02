from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime, timedelta
import os

class Export:
    def __init__(self):
        
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json.txt',scope)
        client = gspread.authorize(creds)
       
    
    def export_info(self,info,other_info):
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json.txt',scope)
        client = gspread.authorize(creds)        
        sheet = client.open('DeviceAccessSheet').worksheet('reported')
        sheet.update_cell(1,1,'info')
        sheet.update_cell(1,2,'date and time')     
        sheet.update_cell(1,3,'State')   
        sheet.update_cell(1,4,'Reported by')
        sheet.update_cell(1,5,'logged in')
        sheet.update_cell(1,6,'device name')
        sheet.update_cell(1,7,'device id')
        #checks for and deletes empty rows
        count = 0
        rows = sheet.row_count+1
        
        for i in range(1,rows):
            a = sheet.row_values(i-count)
            if ('' in a):
                sheet.delete_row(i-count)
                count +=1
               
    
        dt = datetime.now() + timedelta(hours = 2)
        
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
            
        
        
        sheet.append_row([info,dt,0,other_info,'No',device_name,device_id])
        
        
    def export_info_same(self,info,other_info):
        
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
        sheet = client.open('DeviceAccessSheet').worksheet('reported')
        sheet.update_cell(1,1,'info')
        sheet.update_cell(1,2,'date and time')     
        sheet.update_cell(1,3,'State')   
        sheet.update_cell(1,4,'Reported by')
        sheet.update_cell(1,5,'logged in')
        sheet.update_cell(1,6,'device name')
        sheet.update_cell(1,7,'device id')        
        #checks for and deletes empty rows
        count = 0
        rows = sheet.row_count+1
        
        for i in range(1,rows):
            a = sheet.row_values(i-count)
            if ('' in a):
                sheet.delete_row(i-count)
                count +=1
               
    
        dt = datetime.now() + timedelta(hours = 2)
        
                          
        
        sheet.append_row([info,dt,0,other_info,'Yes',device_name,device_id])        
        
    def ID(self):
        t = 0
        r = 1
        f = open('device_config.txt','r')
        previous_line = ''
        
        with open('device_config.txt','r') as rf:
            for line in rf:
                if ('ID' in line and '?' in line):                    
                    t=1
        if (t ==1):
                        
            for line in f:   
                if ('_device' in previous_line):
                    if (line == '\r\n'):
                        pass      
                    else:
                        device_name = line
    
                        break
                else:    
                    previous_line = line         
             
             
            scope = ['https://spreadsheets.google.com/feeds']
            creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json.txt',scope)
            client = gspread.authorize(creds)        
            sheet = client.open('DeviceAccessSheet').worksheet('Devices')
            
            result = sheet.col_values(1)
            
            for word in result:  
                if (word in device_name): 
                    ID = sheet.cell(r,2).value 
                    sheet.update_cell(r,2,str(int(ID)+1))
                    break
                    
                else:
                    r+=1   
            
                                                    
            with open('device_config.txt','r') as rf:
                with open('device_config2.txt','w') as wf:
                    for line in rf:
                        if ('ID' in line and '?' in line): 
                            wf.write('ID=' + str(ID)+'\r\n')
                            t=1
                        else:
                            wf.write(line)
                            
                          
                with open('device_config2.txt','r') as rf:
                    with open('device_config.txt','w') as wf:
                        for line in rf:
                            wf.write(line+'\r\n')
                                
                os.remove("device_config2.txt")
            
        else:
            pass