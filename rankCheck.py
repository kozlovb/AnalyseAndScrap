import psycopg2
def createIfEmpty(name):
    #
    if not tableExist(name):
        try:
            name = str(name)
            connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
            # use our connection values to establish a connection
            conn = psycopg2.connect(connect_str)
            # create a psycopg2 cursor that can execute queries
            cursor = conn.cursor()
# create a new table with a single column called "name"
            #result - win, nc, draw
            create_table = "CREATE TABLE " + name + " ( rankwrestle INT NOT NULL, rankstrike INT NOT NULL, rank INT NOT NULL, WeightCategory TEXT, result INT, time date NOT NULL, CONSTRAINT PK_" + name + " PRIMARY KEY (time));"
            cursor.execute(create_table)
            insert_str = "INSERT INTO " + name + " VALUES (2500, 2500, 2500, null, null, '1900-01-01');"
            cursor.execute(insert_str)
            conn.commit()
            conn.close()
        except Exception as e:
            print("Uh oh, can't connect. Invalid dbname, user or password?")
            print(e)


def tableExist(ima):
    try:
        connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM " + str(ima) + ";")
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

