import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

settings = [
            
            ['port','udp','32719','1'],
            ['port','tcp','32719','1'],
            ['port','http','8080','1'],
            ['host','http','localhost','1'],
            ['host','udp','localhost','1'],
            ['host','tcp','localhost','1']
]

queries = ["""
     drop table if exists settings
""","""
    create table if not exists settings(
        type text,
        key text,
        value text,
        default_value int
    );"""
]

for x in settings:
    queries.append("""
         insert into settings values(
              '%s',
              '%s',
              '%s',
              '%s'
         );
    """ % (x[0], x[1], x[2], x[3]))

for x in queries:
    c.execute(x)
    
conn.commit()     
c.execute('select * from settings')
print c.fetchall()