import logging
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class AccessList:
    def __init__(self,file_name,logger = logging.getLogger(__name__)):
        self.logger = logger;
        with open(file_name) as f:
            self.students = f.readlines()
        self.students = [student.strip() for student in self.students] #allows the usage of system to be recorded in the log
        self.students = [student.upper() for student in self.students]	
        self.logger.info("Read {l} students".format(l = len(self.students)))
        
    def check_allowed(self, student_number): #grants or denies access
        student_number = student_number.upper()
        student_number = student_number.strip()
        for i in self.students:
            students=i.split(',')   
            if(student_number in students):
                    a = True    
                    break
            else:
                    a = False
        return a 

    def check_workday_access(self, student_number):
        
        date = datetime.date.today();        
        day = date.weekday();   
        if (day== 5 or day== 6):
            workday = 0            
        else:
            workday = 1        
        string_date = str(date)
        string_date = string_date[5:]        
        file = open ("public holidays.txt", 'r')
        lines = file.read();        
        if (string_date in lines):
            workday = 0        
            
        student_number = student_number.upper()
        student_number = student_number.strip()
        if (workday == 0):
            
            for i in self.students:
                students=i.split(',')
                if(student_number in students):
                    if ('1' in students):
                        a = True  
                        break
                    else:
                        a=False
            return a
        
        else:
            for i in self.students:
                students=i.split(',')   
                if(student_number in students):
                        a = True    
                        break
                else:
                        a =  False            
            return a
        
    def admin_access(self, student_number):
        
        student_number = student_number.upper()
        student_number = student_number.strip()  
        
        for i in self.students:
            students=i.split(',') 
            if(student_number in students and 'ADMIN' in students):             
                a = True     
                break
            else:
                a = False            
        return a    
    
    def report(self, student_number):
        for i in self.students:
            students=i.split(',') 
            if(student_number in students):             
                a = students    
                break
            else:
                a = ''          
        return a            
    

    def check_ban(self, student_number):
                        
        student_number = student_number.upper()
        student_number = student_number.strip()

         
        for i in self.students:
           
            students=i.split(',')
            if(student_number in students):              
                if ('BANNED' in students):
                    a = False                     
                    break
                else:
                    a = True
        return a
    
    def check_time(self, student_number):

        student_number = student_number.upper()
        student_number = student_number.strip()

          
        for i in self.students:
            students=i.split(',')
            if(student_number in students):              
                t = datetime.datetime.now().time()
                t = str(t)
                (h, m, s) = t.split(':')
                value = float(h) * 100 + float(m) +200
                print(t)
                print(value)
                if (value >= int(students[3]) and value <= int(students[4])):
                    a = True
                else:
                    a= False
        return a
        