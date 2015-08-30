__author__ = 'ZZ_NIFE'

import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "test.db")

# Create table
#c.execute('''DROP TABLE components2''')

#c.execute('''CREATE TABLE components
 #            (compid INTEGER Primary KEY AUTOINCREMENT, type text, name text, address text, id text, status int)''')


def writeComponentToDB(type, name, address, id, status):
    conn = sqlite3.connect(db_path)

    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("INSERT INTO components VALUES (null,?, ?, ?,?,?)", (type,name, address, id, status))
    conn.commit()
    conn.close()

def setStatusForComponentInDB(uniqueId):
    conn = sqlite3.connect(db_path)

    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    rows = getComponentsFromDB()
    status = 0
    for row in rows:

        if str(row[0]) == uniqueId:
            if(row[5] is 1):
                status = 0
            else:
                status = 1
    print("Upadte: " + str(uniqueId) + " with value: " + str(status))
    c.execute("UPDATE components SET status=? WHERE compid=?", (status, uniqueId))
    conn.commit()
    conn.close()

def writeComponentsToJsonFile():
    conn = sqlite3.connect(db_path)

    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM components")
    recs = c.fetchall()
    rows = [dict(rec) for rec in recs]

    with open("../data/components.txt", "w") as outfile:
        json.dump(rows,outfile,indent=4)

    conn.close()

def getComponentsFromDB():
    conn = sqlite3.connect(db_path)

    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    rows = []
    for row in c.execute('SELECT * FROM components ORDER BY type'):
        rows.append(row)
    return rows

    conn.close

#writeComponentToDB("Light","SocketTV", "10001","1","0")
#writeComponentToDB("Light","Rnd", "10001","1","0")
#writeComponentToDB("Socket","SocketTV", "10001","1","0")

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.





