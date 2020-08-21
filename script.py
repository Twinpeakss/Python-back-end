from peewee import *
import json
import sqlite3
from datetime import datetime
import re
import click
import re



#Actions before  create database
#########################################################################################################################################
class FirstPart:

    def __init__(self):
        self



#Opens the persons.json  file for edit/get some data
    with open('persons.json','r+',encoding='utf-8') as access_json:
        read_content = json.load(access_json) #dic
        
            
    def get_persons_dates():
        saved_date = []
        content = read_content['results'] #content is the list 
        for person in content: #person is the dict
            dob_access = person['dob']['date']
            saved_date.append(dob_access)

        return saved_date


    def convert_dates_to_the_date_time(dates):
        date_time_list = []
        for date in dates:
            date = date[:10]
            date = date.replace('-','/')
            date_time_list.append(datetime.strptime(date,'%Y/%m/%d'))
        return date_time_list


   
    def get_days_until_birtday(original_date, datetime.now()):
        days_until = []
        for date in original_date:
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
        return days_until


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
    

    def put_numbs_toJson(numbs):
        with open('persons.json','r+',encoding='utf-8') as access_json:
            read_content = json.load(access_json)
            content = read_content['results']  
            for person,numb in  zip(content,numbs): 
                person['phone'] =  numb

            access_json.seek(0)    
            json.dump(read_content,access_json)
            access_json.truncate()


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



    if __name__ == '__main__': 
        fp = FirstPart()
        fp.create_field_and_put_days(get_days_until_birtday(convert_dates_to_the_date_time(get_persons_dates()),now))
        fp.put_numbs_toJson(get_phone_numbers_and_clear())
        fp.remove_picture_field()

##################################Models#######################################################################################################
db = SqliteDatabase('people.db')

class BaseModel(Model):    
    class Meta:
        database = db 


class Person(BaseModel):
    person_id = AutoField()
    gender = TextField()       
    email = CharField()
    phone = IntegerField()
    cell = CharField()
    nat = CharField()

class Name(BaseModel):
    name_id = ForeignKeyField(Person, column_name='person_id')
    title = CharField()
    first = CharField()
    last = CharField()
    

class Location(BaseModel):
    location_id = ForeignKeyField(Person, column_name='person_id')    
    city = CharField()
    state = CharField()
    country = CharField()
    postcode = CharField()  
    


class Street(BaseModel):
    street_id = ForeignKeyField(Location, column_name='location')
    number = IntegerField()
    name = CharField()
    
    
class Coordinates(BaseModel):
    coordinates_id = ForeignKeyField(Person, column_name='person_id')
    latitude = FloatField()
    longitude = FloatField()
    
    
class TimeZone(BaseModel):
    timezone_id = ForeignKeyField(Person, column_name='person_id')
    offset = CharField()
    description = CharField()
    

class Login(BaseModel):
    login_id = ForeignKeyField(Person, column_name='person_id')
    uuid = CharField()
    username = CharField()
    password = CharField()
    salt = CharField()
    md5 = CharField()
    sha1 = CharField()
    sha256 = CharField()
    

class Dob(BaseModel):
    dob_id = ForeignKeyField(Person, column_name='person_id', backref='dates')
    date = DateTimeField()
    age = IntegerField()
    dub = IntegerField()
    

class Registered(BaseModel):
    registered_id = ForeignKeyField(Person, column_name='person_id')
    date = DateTimeField()
    age = IntegerField()
    

class Id_user(BaseModel):
    user_id = ForeignKeyField(Person, column_name='person_id')
    name = CharField() #""
    value = CharField(null = True)# null
    



def conn_and_create_db():
    db.connect()
    db.create_tables([Person, Name, Location, Street, Coordinates,
                 TimeZone,  Login, Dob, Registered, Id_user])



#Will insert values in the databse if the not already exists
def insert_values_to_db():
    with open('persons.json','r+',encoding='utf-8') as access_json:
        data = json.load(access_json)
        persons = data['results']
        with db.atomic():
            i = 1
            for person in persons:               
                Person.create(gender = person['gender'], email = person['email'],
                phone = person['phone'], cell = person['cell'], nat = person['nat'])

                Name.create(name_id = i,title = person['name']['title'], 
                first = person['name']['first'],last =  person['name']['last'])               

                Location.create(location_id = i, city = person['location']['city'],
                                state = person['location']['state'], country = person['location']['country'],
                                postcode = person['location']['postcode'])

                Street.create(street_id = i, number = person['location']['street']['number'],
                            name = person['location']['street']['name'])

                Coordinates.create(coordinates_id = i, latitude = person['location']['coordinates']['latitude'],
                            longitude = person['location']['coordinates']['longitude'])
    
                TimeZone.create(timezone_id = i, offset = person['location']['timezone']['offset'],
                                description = person['location']['timezone']['description'])

                Login.create(login_id = i, uuid = person['login']['uuid'], username = person['login']['username'],
                 password = person['login']['password'], salt = person['login']['salt'], md5 = person['login']['md5'],
                 sha1 = person['login']['sha1'], sha256 = person['login']['sha256'])

                Dob.create(dob_id = i, date = person['dob']['date'], age = person['dob']['age'],
                            dub = person['dob']['dub'])

                Registered.create(registered_id = i, date = person['registered']['date'],
                                age = person['registered']['age'])

                Id_user.create(user_id = i, name = person['id']['name'], value = person['id']['value'])

                i += 1
               
            
####################CLICK######################

@click.group()
def cli():
    pass

@click.command(name='get-percents')
def get_percents():
    """Returns the percents of males and females""" 
    query_m = Person.select().where(Person.gender == 'male')
    quantity = Person.select()

    persons = 0
    for p in quantity:
        persons += 1

    mens = 0
    for gender in query_m:
        mens +=1

    males =  (mens/persons) * 100
    females = 100 - males  ##I assume that it is only mens and womans in the database xD
    click.echo(str(males) +'% of mens in the database')
    click.echo(str(females) +'% of womans in the database')


#Average % of age of the male and female
@click.command(name='get-average-age')
def get_average_age():
    """Returns the average age of people in database"""
    i = 0
    sum = 0
    query = Dob.select(Dob.age).join(Person, on=(Dob.person_id == Person.person_id))   
    for row in query:
        sum += row.age
        i +=1
    return click.echo(sum/i) 


@click.command(name='get-average-male-age')
def get_average_male_age():
    """Returns the mens average age"""
    sum = 0
    query = Dob.select(Dob.age).join(Person,
    on=(Dob.person_id == Person.person_id)).where(Person.gender == 'male')
    i = 0
    for row in query:
        sum += row.age
        i+=1 
    return click.echo(str(round(sum/i,2)) + ' average male age') 


@click.command(name='get-average-female-age')
def get_average_female_age():
    """Returns the femaels average age"""
    sum = 0
    query = Dob.select(Dob.age).join(Person,
    on=(Dob.person_id == Person.person_id)).where(Person.gender == 'female')
    i = 0
    for row in query:
        sum += row.age
        i+=1 
    return click.echo(str(round(sum/i,2)) + ' average female age') 


@click.command(name='get-most-common-cities')
@click.argument('n', required=True, type=int)
def get_most_common_cities(n):
    """Returns most commons cities in the databse"""
    query = (Location.select((Location.city), fn.COUNT(Location.city).alias('count'))
            .group_by(Location.city).order_by(fn.COUNT(Location.city)
            .desc()).limit(n))

    for row in query:
       print(row.city, row.count)


@click.command(name='get-most-common-passwords')
@click.argument('n', required=True, type=int)
def get_most_common_passwords(n):
    """Returns most common passwords in the database"""
    query = (Login.select((Login.password), fn.COUNT(Login.password).alias('count'))
            .group_by(Login.password).order_by(fn.COUNT(Login.password)
            .desc()).limit(n))

    for row in query:
        print(row.password, row.count)


@click.command(name='get-dates-between')
@click.option('--from','-f','from_', required=True, default='2000-05-01', help='From Wich date')
@click.option('--to', '-t', required=True, default='2000-05-01', help='To Wich date')
def get_users_in_range_dates(from_,to):
    """Get the all users between given dates"""
    M = datetime_validation(from_)
    N = datetime_validation(to)
    query = Person.select(Person).join(Dob,
    on=((Person.person_id == Dob.person_id))).where(Dob.date.between(M,N)).order_by(Dob.date)

    for row in query:
       print(row.email, row.phone, row.nat)


#regex validation of the date
def datetime_validation(some_date):
    pattern1 = "\d{4}.\d{2}.\d{2}"  #YYYY-MM-DD 
    pattern2 = "^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$"  #DD-MM-YYYY
    pattern3 = "^(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d$"  #american MM-DD-YYYY format
    validated = ''   
    result1 = re.fullmatch(pattern1,some_date)
    result2 = re.fullmatch(pattern2,some_date)
    result3 = re.match(pattern3,some_date)
    try:
        if(result1):
            validated = datetime.strptime(some_date, '%Y-%m-%d')

        if(result2):
            validated = datetime.strptime(some_date, '%d-%m-%Y')    

        if(result3):
            validated = datetime.strptime(some_date, '%m-%d-%Y')

    except ValueError as error:
        raise(error)


    return validated


@click.command(name='most-safe-password')
def most_secure_password():
    """Returns the most secure-safe password in the database"""
    passwords = []
    secure = {}
    query = Login.select(Login)
    for row in query:
        passwords.append(row.password)

    one_small_char_pattern = "[a-z]+" #1
    one_big_char_pattern = "[A-Z]+"  #2
    one_digit_pattern = "\d+"  #1 
    eights_digits_pattern = "\w{8}" #5
    special_charachter_pattern = "[|\^&+\-%*/=!>]{1}" #3

    points = 0
    for i in passwords:
        points = 0
        if(re.search(one_small_char_pattern,i)):
            points += 1

        if(re.search(one_big_char_pattern,i)):
            points += 2

        if(re.search(one_digit_pattern,i)):
            points += 1

        if(re.search(eights_digits_pattern,i)):
            points += 5

        if(re.search(special_charachter_pattern,i)):
            points += 3

        secure.update({i:points})

    max_val = max(secure.values())
    max_key = [i for i,j in secure.items() if j == max_val]
    click.echo(str(max_key) + " most secure password, get's the max point " + str(max_val))




cli.add_command(get_percents)
cli.add_command(get_average_age)
cli.add_command(get_average_male_age)
cli.add_command(get_average_female_age)
cli.add_command(get_most_common_cities)
cli.add_command(get_most_common_passwords)
cli.add_command(get_users_in_range_dates)
cli.add_command(get_average_female_age)
cli.add_command(most_secure_password)


if __name__ == '__main__':
    conn_and_create_db()
    insert_values_to_db()
    cli()