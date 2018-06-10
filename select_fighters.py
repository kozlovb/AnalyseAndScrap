import psycopg2
import sys
try:
    connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # create a new table with a single column called "name"
    cursor.execute("""SELECT * FROM fighters ORDER BY fighterName ASC;""")
    rows = cursor.fetchall()
    conn.close()
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)
print(rows)