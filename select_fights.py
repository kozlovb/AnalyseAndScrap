import psycopg2

try:
    connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # create a new table with a single column called "name"
    cursor.execute("SELECT * FROM fights WHERE FightTime BETWEEN " + "to_date('"+"20170801"+"','YYYYMMDD')" + " AND " + "to_date('"+"20171031"+"','YYYYMMDD')"+" ORDER BY FightTime ASC;")
    rows = cursor.fetchall()
    print(rows)
    conn.close()
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)
