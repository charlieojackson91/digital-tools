
# imports required
import time
import urllib
#import urllib.parse
import re
import ssl
import MySQLdb
import datetime
import random
from crawler import Get_rankings

# start the clock and get the month
start = time.time()
now = datetime.datetime.now()
date = str(now)[:10]
print(date)
month = now.month

#TODO: add a break clause if Google block us. Save the count so we can re strart the crawl.

# get around SSL
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# inputs to make connection to database
hostname = 'localhost'
username = 'root'
password = 'chronic1'
database = 'Application'

# Connect to database
myConnection = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database )
print ("Connected to database")
cur = myConnection.cursor()

# query database
cur.execute("SELECT keyword, key_id FROM Keywords")

# THIS FETCH ALL MIGHT BREAK IF THE DATABASE GETS TOO BIG
row = cur.fetchall()

# list to append serps to
lst = list()

output = open('output.txt','w')

# iteration through keywords in database
count = 0
ticker = -1

for iteration in row:
    try:
        count = count + 1
        time.sleep(4)
        if ticker == 10:
            # commit to database every 10 keywords
            myConnection.commit()
            ticker = 0
        ticker = ticker + 1
        orig = iteration[0]
        query = iteration[0].replace(" ","-")
        key_id = iteration[1]
        links = Get_rankings(query)
        print(links)
        counter = 0
        for link in links:
            counter = counter + 1
            # see if the url is already in the database
            try:
                cur.execute("SELECT url_id FROM urls WHERE url_text LIKE %s;", (link,))
                row = cur.fetchone()
                #print ("URL id -",row, link)
                # if its none, the url is not in the database so we need to add it to the database
                if row is None:
                    # insert the url into urls table if its not already there
                    cur.execute("INSERT INTO urls (url_text) VALUES (%s);",(link,))
                    # find the id for the url just inserted
                    cur.execute("SELECT url_id FROM urls WHERE url_text LIKE %s;", (link,))
                    id = cur.fetchone()
                    # insert into the m2m table
                    cur.execute("INSERT INTO Rankings (key_id,url_id,position,timestmp) VALUES (%s,%s,%s,%s);",(key_id,id[0],counter,date))
                # if a url_id was found, check if we are in a new month and add to database if we are
                elif row != None:
                    print ("URL found in urls table")
                    cur.execute("INSERT INTO Rankings (key_id,url_id,position,timestmp) VALUES (%s,%s,%s,%s);",(key_id,row[0],counter,date))
            except Exception as e:
                print(e)
                continue
    except Exception as e:
        print(e)
        continue

# print how long it took
print("Time taken : ", time.time()- start)

# commit to database and close db
myConnection.commit()
myConnection.close()
print ("close connection to database")
