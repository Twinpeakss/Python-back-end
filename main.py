import json
from datetime import datetime
import re



#Opens the persons.json  file for edit/get some data
with open('persons.json','r+',encoding='utf-8') as access_json:
    read_content = json.load(access_json) #dic
      
       
#Gets the users dates of birth        
def get_persons_dates():
    saved_date = []
    content = read_content['results'] #content is the list 
    for person in content: #person is the dict
        dob_access = person['dob']['date']
        saved_date.append(dob_access)

    return saved_date

dates = get_persons_dates()


def convert_dates_to_the_date_time(dates):
    date_time_list = []
    for date in dates:
        date = date[:10]
        date = date.replace('-','/')
        date_time_list.append(datetime.strptime(date,'%Y/%m/%d'))
    return date_time_list

converted_date_time = convert_dates_to_the_date_time(dates)


now = datetime.now()
def get_days_until_birtday(original_date, now):
    days_until = []
    for date in original_date:
        #delta_1 = datetime(now.year, date.month, date.day)
        #delta_2 = datetime(now.year + 1, date.month, date.day)
        #days = (max(delta_1,delta_2) - now).days
        if datetime(now.year,date.month,date.day) < now:
            try:                                                                #condition for leap year and unexisting days(2021.02.29v28)
                days = (datetime(now.year+1,date.month,date.day) - now).days
                days_until.append(days)
            except ValueError:
                days = (datetime(now.year+1,date.month,date.day-1) - now).days
                days_until.append(days)
        else:
            days = (datetime(now.year,date.month,date.day) - now).days
            days_until.append(days)
        #days_until.append(days) 
    return days_until

days = get_days_until_birtday(converted_date_time,now)


def create_field_and_put_days():
    with open('persons.json','r+',encoding='utf-8') as access_json:
        read_content = json.load(access_json)
        content = read_content['results']  
        for person, i in  zip(content,days): 
            dob_access = person['dob']            
            temp_field = {"dub": i }
            dob_access.update(temp_field)

        access_json.seek(0)    
        json.dump(read_content,access_json)
        access_json.truncate()
     
create_field_and_put_days()


def get_phone_numbers_and_clear():
    phone_numbs = []
    cleared_numbs = []
    special_chars = ["-",  "(",   ")"   ," "]
    with open('persons.json','r+', encoding='utf-8') as access_json:
        read_content = json.load(access_json)
        persons = read_content['results']
        for person in persons:
            phone_numbs.append(person['phone'])

        for i in phone_numbs:
            i = re.sub('[-)(]', '', i)
            i = i.replace(' ', '')
            cleared_numbs.append(i)
        return cleared_numbs
   


numbers = get_phone_numbers_and_clear()

def put_numbs_toJson(numbs):
    with open('persons.json','r+',encoding='utf-8') as access_json:
        read_content = json.load(access_json)
        content = read_content['results']  
        for person,numb in  zip(content,numbs): 
            person['phone'] =  numb

        access_json.seek(0)    
        json.dump(read_content,access_json)
        access_json.truncate()

put_numbs_toJson(numbers)



def remove_picture_field():
    with open('persons.json',"r+",encoding='utf-8') as data_file:
        data = json.load(data_file)
        persons = data['results']
        for i in persons:
            if 'picture' in i:
                del i['picture']

        data_file.seek(0)    
        json.dump(data,data_file)
        data_file.truncate()

#remove_picture_field()

