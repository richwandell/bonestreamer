import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

def fetchAllQuery(q):     
    c.execute(q)
    return c.fetchall()
     
def fetchQuery(q):
    c.execute(q)
    return c.fetchone()
     