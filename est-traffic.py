import time
import MySQLdb

# start the clock and get the month
start = time.time()

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
cur.execute("SELECT Keywords.search_volume, Rankings.ranking_id, Rankings.position FROM Keywords JOIN Rankings ON Keywords.key_id = Rankings.key_id")


# THIS FETCH ALL MIGHT BREAK IF THE DATABASE GETS TOO BIG
rows = cur.fetchall()

# Click through rates for forecast
ctr = [0.18000, 0.09000, 0.07600, 0.06000, 0.05500, 0.05000, 0.03000, 0.02250, 0.01500, 0.01000, 0.00850, 0.00800, 0.00750, 0.00700, 0.00650, 0.00600, 0.00550, 0.00500, 0.0050, 0.00450, 0.00385, 0.00370, 0.00355, 0.0030, 0.00325, 0.00310, 0.00295, 0.00280, 0.00265, 0.00200, 0.00190, 0.00180, 0.00170, 0.00160, 0.00150, 0.0010, 0.00130, 0.00120, 0.00110, 0.00100, 0.00090, 0.00080, 0.00070, 0.00060, 0.00050, 0.0000, 0.00030, 0.00020, 0.00010, 0.00000]

# list to test
lst = []

# iterate through all the Rankings in the database
for iteration in rows:
    sv = int(iteration[0])
    ranking_id = iteration[1]
    position = int(iteration[2])
    print (iteration)
    try:
        if position >= 50:
            test = int(sv) * ctr[49]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 49:
            test = int(sv) * ctr[48]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 48:
            test = int(sv) * ctr[47]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 47:
            test = int(sv) * ctr[46]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 46:
            test = int(sv) * ctr[45]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 45:
            test = int(sv) * ctr[44]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 44:
            test = int(sv) * ctr[43]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 43:
            test = int(sv) * ctr[42]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 42:
            test = int(sv) * ctr[41]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 41:
            test = int(sv) * ctr[40]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 40:
            test = int(sv) * ctr[39]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 39:
            test = int(sv) * ctr[38]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 38:
            test = int(sv) * ctr[37]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 37:
            test = int(sv) * ctr[36]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 36:
            test = int(sv) * ctr[35]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 35:
            test = int(sv) * ctr[34]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 34:
            test = int(sv) * ctr[33]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 33:
            test = int(sv) * ctr[32]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 32:
            test = int(sv) * ctr[31]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 31:
            test = int(sv) * ctr[30]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 30:
            test = int(sv) * ctr[29]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 29:
            test = int(sv) * ctr[28]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 28:
            test = int(sv) * ctr[27]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 27:
            test = int(sv) * ctr[26]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 26:
            test = int(sv) * ctr[25]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 25:
            test = int(sv) * ctr[24]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 24:
            test = int(sv) * ctr[23]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 23:
            test = int(sv) * ctr[22]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 22:
            test = int(sv) * ctr[21]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 21:
            test = int(sv) * ctr[20]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 20:
            test = int(sv) * ctr[19]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 19:
            test = int(sv) * ctr[18]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 18:
            test = int(sv) * ctr[17]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 17:
            test = int(sv) * ctr[16]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 16:
            test = int(sv) * ctr[15]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 15:
            test = int(sv) * ctr[14]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 14:
            test = int(sv) * ctr[13]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 13:
            test = int(sv) * ctr[12]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 12:
            test = int(sv) * ctr[11]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 11:
            test = int(sv) * ctr[10]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 10:
            test = int(sv) * ctr[9]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 9:
            test = int(sv) * ctr[8]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 8:
            test = int(sv) * ctr[7]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 7:
            test = int(sv) * ctr[6]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 6:
            test = int(sv) * ctr[5]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 5:
            test = int(sv) * ctr[4]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 4:
            test = int(sv) * ctr[3]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 3:
            test = int(sv) * ctr[2]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 2:
            test = int(sv) * ctr[1]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position >= 1:
            test = int(sv) * ctr[0]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
        elif position < 1:
            test = int(sv) * ctr[0]
            cur.execute("UPDATE Rankings SET est_traffic = %s WHERE ranking_id = %s",(test,ranking_id,))
            continue
    except:
        print ("something broke")
        lst.append('BREAK')


# print how long it took
print("Time taken : ", time.time()- start)

# commit to database and close db
myConnection.commit()
myConnection.close()
print ("close connection to database")
