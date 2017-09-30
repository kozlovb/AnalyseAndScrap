import psycopg2

try:
    connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS fights;""") 
    # create a new table with a single column called "name"
    cursor.execute("""CREATE TABLE fights(
FightTime date NOT NULL, 
FightPlace TEXT NOT NULL, 
Attendance INT NOT NULL,
result TEXT NOT NULL,
method TEXT NOT NULL, 
FirstFighterName TEXT NOT NULL, 
SecondFighterName TEXT NOT NULL, 
StrikesFirstFighter INT NOT NULL, 
StrikesSecondFighter INT NOT NULL,
TakedownsFirstFighter INT NOT NULL, 
TakedownsSecondFighter INT NOT NULL, 
SubAttFirstFighter INT NOT NULL, 
SubAttSecondFighter INT NOT NULL,
PassGuardFirstFighter INT NOT NULL, 
PassGuardSecondFighter INT NOT NULL, 
WeightCategory TEXT NOT NULL, 
RoundEnd INT NOT NULL, 
TimeEnd INT NOT NULL, 
KDFirstFighter INT NOT NULL, 
KDSecondFighter INT NOT NULL, 
ReverseFirstFighter INT NOT NULL, 
ReverseSecondFighter INT NOT NULL, 
GroundStrikesFirstFighter INT NOT NULL, 
GroundStrikesSecondFighter INT NOT NULL, 
ScoreDiff INT NOT NULL, 
CONSTRAINT PK_placefighters PRIMARY KEY (FightTime, FirstFighterName, SecondFighterName) 
);""")
    #cursor.execute("""CREATE INDEX title_idx ON fights (FightTime);""")
    # run a SELECT statement - no data in there, but we can try it
    #cursor.execute("""INSERT INTO fights VALUES ('1952-07-07', 'a', 1, 'res', 'a', 'a', 'a',1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);""")
    #cursor.execute("""INSERT INTO fights VALUES ('1951-07-07', 'a', 1, 1, 'a', 'a', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);""")
    #cursor.execute("""INSERT INTO fights VALUES ('1953-07-07', 'a', 1, 1, 'a', 'a', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);""")
    #cursor.execute("INSERT INTO fights VALUES ('2016-11-12','NewYorkCity,NewYork,USA',20427,'win','KO/TKO','ConorMcGregor','EddieAlvarez',32,9,0,0,0,0,0,0,'Lightweight',2,184,3,0,0,0,5,0,-1);")
    cursor.execute("""CREATE INDEX title_idx ON fights (FightTime);""") 
    cursor.execute("""SELECT * FROM fights ORDER BY FightTime ASC;""")
    rows = cursor.fetchall()
    print(rows)
    conn.commit()
    conn.close()
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)
