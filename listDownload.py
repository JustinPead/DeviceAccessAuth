from oauth2client.service_account import ServiceAccountCredentials
import gspread


class listDownload:
    
    def __init__(self):
        filename = 'accesslist'
        
        

    def download():
        filename = 'accesslist'

        f = open('device_config.txt','r')
        groups = ['group_global']
        deviceName = ''
        config = []
        instructionNumber = 0
        for line in f:
            line = line.rstrip()
            if(line[0] == '_'):
                instructionNumber = instructionNumber+1
            else:
                if(1 == instructionNumber): #group information
                    line = 'group_'+line
                    groups.append(line)
                elif(2 == instructionNumber): #device information
                    if ('ID' not in line):
                        deviceName = line
                elif(3 == instructionNumber): #general config Information
                    config.append(line)
                else:
                    print("I should never have gotten here - Case after _config!!?!")
        
        times = config[0].split(',')
        accessStartTime = int(times[0])
        accessStopTime = int(times[1])
        config_nonWorkDay = int(config[1].split('=')[1])
        
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json.txt',scope)
        client = gspread.authorize(creds)
        groupNames = []
        #for num, sheetName in enumerate(groups, start=0):
        for sheetName in groups:
            sheet = client.open('DeviceAccessSheet').worksheet(sheetName)
            sheetRecords = sheet.get_all_records()
            if(sheetRecords[0]["Role"] == "setting"):
                groupSettings = sheetRecords[0]
                groupStartTime = groupSettings["AllowStartTime"]
                groupStopTime = groupSettings["AllowStopTime"]
                group_nonWorkDay = groupSettings["NonWorkDay"]
            else:
                groupStartTime = accessStartTime
                groupStopTime = accessStopTime
                group_nonWorkDay = config_nonWorkDay
            for record in sheetRecords:
                if(record["Role"] == 'user'):
                    record["AllowStartTime"] = groupStartTime
                    record["AllowStopTime"] = groupStopTime
                    record["NonWorkDay"] = group_nonWorkDay
                if(record["Role"] == 'e_user'):
                    if(record["AllowStartTime"] == ''):
                        record["AllowStartTime"] = groupStartTime
                    if(record["AllowStopTime"] == ''):
                        record["AllowStopTime"] = groupStopTime
                    if(record["NonWorkDay"] == ''):
                        record["NonWorkDay"] = group_nonWorkDay
            groupNames.extend(sheetRecords)
        
        sheet = client.open('DeviceAccessSheet').worksheet(deviceName)
        sheetRecords = sheet.get_all_records()
        if(sheetRecords[0]["Role"] == "setting"):
            deviceSettings = sheetRecords[0]
            deviceStartTime = deviceSettings["AllowStartTime"]
            deviceStopTime = deviceSettings["AllowStopTime"]
            device_nonWorkDay = deviceSettings["NonWorkDay"]
        else:
            deviceStartTime = accessStartTime
            deviceStopTime = accessStopTime
            device_nonWorkDay = config_nonWorkDay
        for record in sheetRecords:
            if(record["Role"] == 'user'):
                record["AllowStartTime"] = deviceStartTime
                record["AllowStopTime"] = deviceStopTime
                record["NonWorkDay"] = device_nonWorkDay
            if(record["Role"] == 'e_user'):
                if(record["AllowStartTime"] == ''):
                    record["AllowStartTime"] = deviceStartTime
                if(record["AllowStopTime"] == ''):
                    record["AllowStopTime"] = deviceStopTime
                if(record["NonWorkDay"] == ''):
                    record["NonWorkDay"] = device_nonWorkDay
        
        
        f = open(filename+".txt",'w')
        f.write('group\r\n')
        for i in groupNames:
            if(i["Role"] != "Setting"):
                if(str.isdigit(str(i['UCTNumber']))):
                    f.write(str(i['Name'])+','+'0'+str(i['UCTNumber'])+','+str(i['Role'])+','+str(i["AllowStartTime"])+','+str(i["AllowStopTime"])+','+str(i["NonWorkDay"])+'\r\n')
                else:                
                    f.write(str(i['Name'])+','+str(i['UCTNumber'])+','+str(i['Role'])+','+str(i["AllowStartTime"])+','+str(i["AllowStopTime"])+','+str(i["NonWorkDay"])+'\r\n')
                
        f.write('deviceSpecific\r\n')
        for i in sheetRecords:
            if(i["Role"] != "Setting"):
                if(str.isdigit(str(i['UCTNumber']))):
                    f.write(str(i['Name'])+','+'0'+str(i['UCTNumber'])+','+str(i['Role'])+','+str(i["AllowStartTime"])+','+str(i["AllowStopTime"])+','+str(i["NonWorkDay"])+'\r\n')        
                else:
                    f.write(str(i['Name'])+','+str(i['UCTNumber'])+','+str(i['Role'])+','+str(i["AllowStartTime"])+','+str(i["AllowStopTime"])+','+str(i["NonWorkDay"])+'\r\n')
        
               
               
