import psycopg2
import math
connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
        
def CreateAveragesTable(category):
    name = "Average" + str(category)
    try:
        #connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        names = (name + "WL", name + "Draw")  
        for name in names:
            drop_if = "DROP TABLE IF EXISTS "+ name  
            cursor.execute(drop_if) 
        for name in names:                           #datetime.date(2015, 12, 12), 'JoseAldo',              170,               177,               'Orthodox - 1',           29.25,                     2650,                  2599,                      2772,             False,                                866.6666666666666,                    7,               'Featherweight')
            create_table = "CREATE TABLE " + name + "(fightTime INT NOT NULL, fighterName TEXT NOT NULL,height INT NOT NULL, reach INT NOT NULL, stance INT NOT NULL, age REAL NOT NULL, rankwrestle INT NOT NULL, rankstrike INT NOT NULL, rank INT NOT NULL, faughtLastYear INT NOT NULL, lastResultAverage REAL NOT NULL, numOfUFCFights INT NOT NULL, fighterName2 TEXT NOT NULL, height2 INT NOT NULL, reach2 INT NOT NULL, stance2 INT NOT NULL, age2 REAL NOT NULL, rankwrestle2 INT NOT NULL, rankstrike2 INT NOT NULL, rank2 INT NOT NULL, faughtLastYear2 INT NOT NULL, lastResultAverage2 REAL NOT NULL, numOfUFCFights2 INT NOT NULL, CONSTRAINT PK_"+name+" PRIMARY KEY (fightTime, fighterName));"
            cursor.execute(create_table)
        conn.commit()
        conn.close()
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
#info result 0, datetime 1, name 2, height 3, reach 4,
# stance 5, age 6, rank_wre 7, rank-str 8, rank 9, faughtLYear 10, lustResAv 11, NumUFCFight 12 , 
# name2 13, height2 14, reach2 15,
# stance2 16, age2 17, rank_wre2 18, rank-str2 19, rank2 20, faughtLYear2 21, lustResAv2 22, NumUFCFight2 23 
# category 24.        
def stAndFl(st,fl):
    if st == "Orthodox":
        stance = 1
    else:
        stance = 0
    if fl == True:
        faughtInLastYear = 1
    else:
        faughtInLastYear = 0
    return stance, faughtInLastYear 
def writeInDB(info):
    table_name = "Average" + str(info[24])
    if info[0] == "win":
        table_name = table_name + "WL"   
    else:
        table_name = table_name + "Draw"
                #time   name      height   reach   stance    age      rankw   rankstr   rank    faughtLastY  lustResAver NumUFCFights
    date_str = str(info[1])
    time_int = str(int(date_str[0:4])*10000 + int(date_str[5:7])*100 + int(date_str[8:10]))
    stance, faughtInLastYear = stAndFl(info[5], info[10])  
    stance2, faughtInLastYear2 = stAndFl(info[16], info[21])
    c = ","    
                                 #time                                    name             height               reach       stance        age            rankw        rankstr        rank           faughtLastY         lustResAver        NumUFCFights,               name                height               reach       stance             age            rankw                rankstr        rank           faughtLastY     lustResAver      NumUFCFights
    date_str = str(info[1])
    insert_str = "INSERT INTO " + table_name + " VALUES ("+time_int+",'"+str(info[2])+"',"+str(info[3])+c+str(info[4])+c+str(stance)+c+str(info[6])+c+str(info[7])+c+str(info[8])+c+str(info[9])+c+str(faughtInLastYear)+c+str(info[11])+c+str(info[12])+",'"+str(info[13])+"',"+ str(info[14]) + c + str(info[15]) +c +str(stance2)+ c+  str(info[17]) +c+str(info[18])+c+str(info[19])+c+str(info[20])+c+str(faughtInLastYear2)+c+str(info[22])+c+str(info[23])+");"
                            #('win', datetime.date(2015, 12, 12),        'ConorMcGregor',          175,             187,         'Orthodox', 27.416666666,     2568,           2647,        2791,            True,        1000.0,             6,          '')
    try:
        connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"  
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        cursor.execute(insert_str)
        conn.commit()
        conn.close()
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
def selecttest():
    try:
        connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM AverageFeatherweightWL;")
        rows = cursor.fetchall()
        print(rows)
        conn.commit()
        conn.close
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
#def calculateVarHeiReachAgeLastResAvNumUFCFight(table_name):
#          #h  r  age lastResAv   numUFCF
#    res = [0, 0, 0,    0,        0]
#    av = selectAverages(table_name)
#    if av[0] == 0:
#        return res
        
#    try:
#        conn = psycopg2.connect(connect_str)
#        cursor = conn.cursor()
#        cursor.execute("SELECT * FROM " + str(table_name)+";")
#        rows = cursor.fetchall()
#        for e in rows:
#            res[0] = (e[2]
def getCountsCat(category):
    table_names = ("Average"+category+"WL","Average"+category+"Draw")
    return (getCounts(table_names[0]), getCounts(table_names[1]))
def getCounts(table_name):
    try:
        connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+str(table_name)+";")
        rows = cursor.fetchall()
        conn.commit()
        conn.close
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e) 
    return len(rows)
def selectDiffAveragesCat(category):
    table_names = ("Average"+category+"WL","Average"+category+"Draw")
    result = []
    for table in table_names:
        result.append(selectDiffAverages(table))
    return result
def selectAveragesCat(category):
    table_names = ("Average"+category+"WL","Average"+category+"Draw")
    result = []
    for table in table_names:
        result.append(selectAverages(table))
    return result
def selectAverages(table_name):
    try:
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM " + str(table_name)+";")    
        rows = cursor.fetchall()
                 # h1  r1  a1  lrAv1 numUFCF1  h2  r2  a2  lrAv2 numUFCF2
        result = [0,   0,  0,   0,    0,       0,   0,  0,   0,     0]   
        if(len(rows) != 0):
            for e in rows:
                print("hei", e[2], " vt ", e[13])
                result[0] = result[0] + (e[2])        
                result[1] = result[1] + (e[3])
                result[2] = result[2] + (e[5])
                result[3] = result[3] + (e[10])
                result[4] = result[4] + (e[11])
                #second averages
                result[5] = result[5] + (e[13])        
                result[6] = result[6] + (e[14])
                result[7] = result[7] + (e[16])
                result[8] = result[8] + (e[21])
                result[9] = result[9] + (e[22])
        else:
            return (len(rows), result)
        conn.commit()
        conn.close
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
    for i in range(0, len(result)):
        result[i] = result[i] / len(rows)
    return (len(rows), result)
def selectDiffAverages(table_name):
    try:
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM " + str(table_name)+";")    
        rows = cursor.fetchall()
                 # h  r  a  lrAv numUFCF
        result = [0, 0, 0, 0,   0]   
        if(len(rows) != 0 ):
            for e in rows:
                result[0] = result[0] + (e[2] - e[13])        
                result[1] = result[1] + (e[3] - e[14])
                result[2] = result[2] + (e[5] - e[16])
                result[3] = result[3] + (e[10] - e[21])
                result[4] = result[4] + (e[11] - e[22])
        else:
            return (len(rows), result)
        conn.commit()
        conn.close
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
    for i in range(0, len(result)):
        result[i] = result[i] / len(rows)
    return (len(rows), result)
def selectDiffVarCat(category, AverRes):
    table_names = ("Average"+category+"WL","Average"+category+"Draw")
    result = []
    print('avres', AverRes)
    result.append(selectDiffVar(table_names[0], AverRes[0][1]))
    result.append(selectDiffVar(table_names[1], AverRes[1][1]))
    print('var', result)
    return result
def selectVarCat(category, AverRes):
    table_names = ("Average"+category+"WL","Average"+category+"Draw")
    result = []
    print('avres', AverRes)
    result.append(selectVar(table_names[0], AverRes[0][1]))
    result.append(selectVar(table_names[1], AverRes[1][1]))
    print('var', result)
    return result
def selectVar(table_name, aver):
    try:
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM " + str(table_name)+";")    
        rows = cursor.fetchall()
                 # h  r  a  lrAv numUFCF
        result = [0, 0, 0, 0,   0,   0, 0, 0, 0,   0] 
        index = [2, 3, 5, 10,11,13,14,16,21,22]
        #3.5 + 0.5 + 7.5 + 4.5+ 7.5+0.5 9.5 
        if(len(rows) != 0 ):
            for e in rows:
                for i in range(0,len(result)):
                    result[i] = result[i] + math.pow((aver[i] -e[index[i]]),2)
        else:
            return (len(rows), result)
        conn.commit()
        conn.close
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
    for i in range(0, len(result)):
        result[i] = result[i] / len(rows)
    return (len(rows), result)
def selectDiffVar(table_name, aver):
    try:
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM " + str(table_name)+";")    
        rows = cursor.fetchall()
                 # h  r  a  lrAv numUFCF
        result = [0, 0, 0, 0,   0]  
        #3.5 + 0.5 + 7.5 + 4.5+ 7.5+0.5 9.5 
        if(len(rows) != 0 ):
            for e in rows:
                result[0] = result[0] + math.pow((aver[0] -(e[2] -  e[13])),2)        
                result[1] = result[1] + math.pow((aver[1] -(e[3] -  e[14])),2)
                result[2] = result[2] + math.pow((aver[2] -(e[5] -  e[16])),2)
                result[3] = result[3] + math.pow((aver[3] -(e[10] - e[21])),2)
                result[4] = result[4] + math.pow((aver[4] -(e[11] - e[22])),2)
        else:
            return (len(rows), result)
        conn.commit()
        conn.close
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
    for i in range(0, len(result)):
        result[i] = result[i] / len(rows)
    return (len(rows), result)
        
