import psycopg2
import re
def selectFighterNames():
    try:
        connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        cursor.execute("""SELECT fighterName FROM fighters;""")
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return rows
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)

class FightRankingTable(object):
    def __init__(self, fighter_name):
        self.fighter_name = fighter_name
     
        try:
            connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
            # use our connection values to establish a connection
            conn = psycopg2.connect(connect_str)
            # create a psycopg2 cursor that can execute queries
            cursor = conn.cursor()
            drop_if = "DROP TABLE IF EXISTS "+ self.fighter_name  
            cursor.execute(drop_if) 
            # create a new table with a single column called "name"
            #result - win, nc, draw
            create_table = "CREATE TABLE " + self.fighter_name + " ( rankwrestle INT NOT NULL, rankstrike INT NOT NULL, rank INT NOT NULL, WeightCategory TEXT, result INT, time date NOT NULL, CONSTRAINT PK_"+self.fighter_name+" PRIMARY KEY (time));"
            cursor.execute(create_table)
    #cursor.execute("""CREATE INDEX title_idx ON fights (FightTime);""")
    # run a SELECT statement - no data in there, but we can try it
            insert_str = "INSERT INTO " + self.fighter_name + " VALUES (2500, 2500, 2500, null, null, '1900-01-01');"
            cursor.execute(insert_str)
            select_str = "SELECT * FROM " + self.fighter_name + ";"             
    #cursor.execute("""INSERT INTO fights VALUES ('1951-07-07', 'a', 1, 1, 'a', 'a', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);""")
    #cursor.execute("""INSERT INTO fights VALUES ('1953-07-07', 'a', 1, 1, 'a', 'a', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);""")
    #cursor.execute("INSERT INTO fights VALUES ('2016-11-12','NewYorkCity,NewYork,USA',20427,'win','KO/TKO','ConorMcGregor','EddieAlvarez',32,9,0,0,0,0,0,0,'Lightweight',2,184,3,0,0,0,5,0,-1);")
    #cursor.execute("""CREATE INDEX title_idx ON fights (FightTime);""") 
            cursor.execute(select_str)
            rows = cursor.fetchall()
            print(rows)
            conn.commit()
            conn.close()
        except Exception as e:
            print("Uh oh, can't connect. Invalid dbname, user or password?")
            print(e)
if __name__ == "__main__":
        #f = FightRankingTable("L")
        f_names = selectFighterNames()
        for name in f_names:
            ima = re.sub(r'-','',str(name[0]))
            ima = re.sub(r'\.','',ima)  
            FightRankingTable(str(ima)) 
#todo select fighters and then feed names to fightrank 
