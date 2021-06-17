import pandas as pd
import urllib.request as u
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pytz import timezone
import http.client
from string import Template 
import http.client
import pywhatkit as kit 
import time

System_time = time.localtime(time.time())

# using web scraping to scrape the contest details from codeforces' site
contest = "https://codeforces.com/contests"
page = u.urlopen(contest)
soup = BeautifulSoup(page, features='html.parser')

all_tables = soup.find_all('table')  # all table
right_table = soup.find('table', class_='')  # first table

# the 6 cols
A = []  # name
B = []  # start
C = []
D = []  # length
E = []  # before start
F = []  # reg deadline

for row in right_table.findAll("tr"):
    cells = row.findAll('td')
    if len(cells) == 6:
        A.append(cells[0].find(text=True))  # name
        B.append(cells[2].find(text=True))  # start
        D.append(cells[3].find(text=True))  # length
        E.append(cells[4].find(text=True))  # before start
        F.append(cells[5].find(text=True))  # reg


for row in right_table.findAll("a"):
    cells = row.findAll('span')
    if len(cells) == 1:
        C.append(cells[0].find(text=True))

# triming the spaces and newline characters in string
d = []
for i in D:
    j = i.replace(' ', '')
    k = j.replace('\n', '')
    l = k.replace('\r', '')
    d.append(l)
a = []
for i in A:
    j = i.replace(' ', '')
    k = j.replace('\n', '')
    l = k.replace('\r', '')
    a.append(l)

e = []
for i in E:
    j = i.replace(' ', '')
    k = j.replace('\n', '')
    l = k.replace('\r', '')
    e.append(l)

# changing the timezone to Asia/Kolkata
T = []  # --> indian time
for i in C:
    date_str = i
    datetime_obj = datetime.strptime(
        date_str, "%b/%d/%Y %H:%M")  # creating obj from string
    # giving an time zone to our object
    datetime_ob = timezone('Europe/Moscow').localize(datetime_obj)
    datetime_obj_ind = datetime_ob.astimezone(
        timezone('Asia/Kolkata'))  # converting time zone
    # converting the obj back to string
    T.append(datetime_obj_ind.strftime("%Y-%m-%d %H:%M:%S"))

# Tabulariation of data
print("\n\n**********UPCOMING CONTEST DETAILS**********\n\n")
df = pd.DataFrame()
df['Name'] = a
df['Start'] = T
df['Length'] = d
df['Phase'] = e
print(df)

R = []  # --> reminder time
# storing the time at which the reminder is to be sent(15 minutes before the contest starts)
for i in T:
    a = datetime.strptime(i, "%Y-%m-%d %H:%M:%S")  # string process time
    b = str(a-timedelta(minutes=15))
    R.append(b)  # obj

rem = ["2021/06/17 11:1:05"]
for i in R:
    date_str = i
    datetime_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    rem.append(datetime_obj.strftime("%Y/%m/%d %H:%M:%S"))



for i  in rem :
    conn = http.client.HTTPSConnection("api.msg91.com")
    kit.sendwhatmsg("+919486443050", "A remainder is sent for you codeforces contest on "+i, System_time.tm_hour, System_time.tm_min+3)
    payload = "{\n  \"flow_id\": \"60ca0d466c58d07d2249faa2\",\n  \"sender\": \"CForce\",\n  \"mobiles\": \"918220301091\",\n  \"schtime\":\""+i+"\",\n  \"VAR1\": \"VALUE 1\",\n  \"VAR2\": \"VALUE 2\"\n}"
    
    print(payload)

    headers = {
        'authkey': "362641AaN0He0TO60c9f08aP1",
        'content-type': "application/JSON"
    }

    conn.request("POST", "/api/v5/flow/", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"));
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    