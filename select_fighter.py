import psycopg2
import sys

if len(sys.argv) != 2:
    print ("wrong arg number")
fighterName = sys.argv[1]
try:
    connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # create a new table with a single column called "name"
    name = sys.argv[1:][0]
    cursor.execute("SELECT * FROM fighters WHERE fighterName LIKE " + name + ";")
    rows = cursor.fetchall()
    #print(rows)
    conn.close()
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)
