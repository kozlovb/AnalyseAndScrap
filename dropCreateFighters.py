import psycopg2

try:
    connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS fighters;""") 
    # create a new table with a single column called "name"
    cursor.execute("""CREATE TABLE fighters(
fighterName TEXT NOT NULL, 
height INT NOT NULL, 
reach INT NOT NULL, 
stance TEXT NOT NULL,
age date NOT NULL, 
CONSTRAINT PK_fighterName PRIMARY KEY (fighterName));""")
    #cursor.execute("""CREATE INDEX title_idx ON fights (FightTime);""")
    # run a SELECT statement - no data in there, but we can try it
    #cursor.execute("""INSERT INTO fights VALUES ('1952-07-07', 'a', 1, 'res', 'a', 'a', 'a',1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);""")
    #cursor.execute("""INSERT INTO fights VALUES ('1951-07-07', 'a', 1, 1, 'a', 'a', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);""")
    #cursor.execute("""INSERT INTO fights VALUES ('1953-07-07', 'a', 1, 1, 'a', 'a', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);""")
    #cursor.execute("INSERT INTO fights VALUES ('2016-11-12','NewYorkCity,NewYork,USA',20427,'win','KO/TKO','ConorMcGregor','EddieAlvarez',32,9,0,0,0,0,0,0,'Lightweight',2,184,3,0,0,0,5,0,-1);")
    #cursor.execute("""CREATE INDEX title_idx ON fights (FightTime);""") 
    #cursor.execute("""SELECT * FROM fights ORDER BY FightTime ASC;""")
    #rows = cursor.fetchall()
    #print(rows)
    conn.commit()
    conn.close()
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)
