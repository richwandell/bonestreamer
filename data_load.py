import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

queries = ["""
     drop table if exists ports
""","""
     create table if not exists ports(
          port_type text,
          port_number int
     );
""","""
     insert into ports values(
          'udp',
          '32719'
     );
""","""
     insert into ports values(
          'tcp',
          '32719'
     );
""","""
     insert into ports values(
          'http',
          '8080'
     );
"""]

for x in queries:
    c.execute(x)
conn.commit()     
c.execute('select * from ports')
print c.fetchall()