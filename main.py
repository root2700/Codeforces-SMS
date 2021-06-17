# -*- coding: utf-8 -*-
"""

@author: Aadityan and  Sharan 
"""

import twilio;

from twilio.rest import Client
import pandas as pd
import urllib.request as u
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pytz import timezone
import http.client
import os
from twilio.http.http_client import TwilioHttpClient
import time


System_time = time.localtime(time.time())

def sendmessage(name):
    
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    account_sid = 'ACc9f7d18a8d82bac668293c2df91c03d0'
    auth_token = '7802718dd3e07b08e9e29c3e01bffb91'

    client = Client(account_sid, auth_token, http_client=proxy_client)

    # twilio api calls will now work from behind the proxy:
    message = client.messages \
        .create(
            body=f'Remainder! {name}Starts in 15 minutes',
            from_='+12142389916',
            to='+918220301091'
            )
    print(message.sid)


def sleep(n):
    for i in range(n):
        time.sleep(1)

# using web scraping to scrape the contest details from codeforces' site
def solve():
    
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


    now_time = datetime.now()
    x = now_time.strftime("%Y/%m/%d-%H:%M:%S")
    x = datetime.strptime(x, "%Y/%m/%d-%H:%M:%S")

    rem = []
    for i in R:
        date_str = i
        datetime_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        difference = datetime_obj - x
        seconds = difference.days*3600*24 + difference.seconds;
        rem.append(seconds);
    
    
    prev =0;
    idx = 0;
    hour3 = 3600*3; #update frequency 
    for i in rem: 
        i = i-prev;
        prev = i;
        print(i)
        if(i < hour3):
            sleep(i);
            sendmessage(A[idx]);
            idx+=1;
        else:
            sleep(hour3);


while(1):
    solve();







    




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
