import psycopg2
import re
import rankCheck
#date here is a str in sql format - 1900-02-15
#both dates are included
def selectFighteInfo(dateFrom, dateTo):
    try:
        connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        select_str = "SELECT * FROM fights WHERE FightTime BETWEEN " + "to_date('"+dateFrom+"','YYYYMMDD')" + " AND " + "to_date('"+dateTo+"','YYYYMMDD')" + " ORDER BY FightTime ASC;" 
        cursor.execute(select_str)
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return rows
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
def retriveNumberFights(fighterName):
    try:
        connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        select_str = "SELECT COUNT(time) FROM " + fighterName + ";"
        cursor.execute(select_str)
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return rows
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
def retriveNumberFightsAtTime(fighterName, time):
    try:
        connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        time_f = "'" + str(time) +"'::date"
        #WHERE update_date >= '2013-05-03'::date
        select_str = "SELECT COUNT(time) FROM " + fighterName + " WHERE time < "+ time_f + ";" 
#"to_date('"+dateFrom+"','YYYYMMDD');"
        cursor.execute(select_str)
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return rows
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
def retriveCurrentRank(fighterName):
    try:
        connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        #SELECT * FROM table WHERE id = ? ORDER BY date DESC LIMIT 1;
        select_str = "SELECT * FROM " + fighterName + " ORDER BY time DESC LIMIT 1;"
        cursor.execute(select_str)
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        # rows [0] - rankwrestle, [1] - rankstrike, [2] - rank, [3] - WeightCategory, [4] - result, [5] - time
        return rows
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
def retriveRank(fighterName,time):
    print("time",str(time))
    try:
        connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        #SELECT * FROM table WHERE id = ? ORDER BY date DESC LIMIT 1;
        time_f = "'" + str(time) +"'::date"       
        select_str = "SELECT * FROM " + fighterName + " WHERE time < "+ time_f + " ORDER BY time DESC LIMIT 1;"
        cursor.execute(select_str)
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        # rows [0] - rankwrestle, [1] - rankstrike, [2] - rank, [3] - WeightCategory, [4] - result, [5] - time
        return rows
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
#add change weight
def Pelo(diffInRanking):
    return 1/(1+10**(-float(diffInRanking)/400))
def K_h(number):
    n = int(number) 
    if n == 1:
       return 150
    elif n == 2:
       return 125
    elif n == 3:
       return 100
    else:
       return 80
def K_l(number):
    l = [35,40, 60]
    return l[int(number) - 1]
def Kpair(number1, number2):
    nh1 = K_h(number1)
    nh2 = K_h(number2) 
    standart = 80
    if nh1 != standart and nh2 != standart:
        return (nh1, nh2)
    elif nh1 != standart and nh2 == standart:
        return (nh1, K_l(number1))
    elif nh1 == standart and nh2 !=standart:
        return (K_l(number2), nh2)
    else:
        return (nh1, nh2)

def calculateRankStrike(rank1, rank2, numberFights1, numberFights2, method, scoreDiff, StrikesFirstFighter, StrikesSecondFighter, KDFirstFighter, KDSecondFighter, GroundStrikesFirstFighter, GroundStrikesSecondFighter):
    KDfactor = 10 #KD = 20 sig strikes landed
    sigStrikesF = abs(int(StrikesFirstFighter)-int(GroundStrikesFirstFighter)) + KDfactor*KDFirstFighter
    if method == "KO/TKO":
        sigStrikesF = sigStrikesF + 20
    sigStrikesS = abs(int(StrikesSecondFighter)-int(GroundStrikesSecondFighter)) + KDfactor*KDSecondFighter
    totalStrikes = sigStrikesF + sigStrikesS
    rank1_new = rank1
    rank2_new = rank2
    if totalStrikes > 15:
        sigStrikesRatioF = sigStrikesF/totalStrikes
        sigStrikesRatioS = sigStrikesS/totalStrikes
        #At this step points are calculated here comes the magic formula:
        diffInRankin = int(rank1) - int(rank2)
        #determine K:
        K_1, K_2 = Kpair(numberFights1, numberFights2)
        rank1_new = int(rank1) + K_1*(sigStrikesRatioF - Pelo(diffInRankin))
        rank2_new = int(rank2) + K_2*(sigStrikesRatioS - Pelo(-diffInRankin))
    return (rank1_new, rank2_new)
def calculateRankWrestle(rank1, rank2, numberFights1, numberFights2, method, Takedown1Fighter, Takedown2Fighter, Reverse1Fighter, Reverse2Fighter, passGuard1, passGuard2, SubAtt1Fighter, SubAtt2Fighter, GrStr1Fighter, GrStr2Fighter):
    #takedown - 5
    #Reverse - 5
    #passGuard - 3
    #SubAtt - 2
    #GrStr -1
    diffInRankin = int(rank1) - int(rank2)
    #determine K:
    (K_1, K_2) = Kpair(numberFights1, numberFights2)
    fighter1Wscore = 5 * Takedown1Fighter + 5 * Reverse1Fighter + 3 * passGuard1 + 2 * SubAtt1Fighter + GrStr1Fighter
    fighter2Wscore = 5 * Takedown2Fighter + 5 * Reverse2Fighter + 3 * passGuard2 + 2 * SubAtt2Fighter + GrStr2Fighter
    if method == "SUB":
        fighter1Wscore = fighter1Wscore + 20
    totalWscore =  fighter1Wscore + fighter2Wscore    
    (rank1_new, rank2_new) = (rank1, rank2)
    if totalWscore > 10:
        wresRatioF1 = fighter1Wscore/totalWscore
        wresRatioF2 = fighter2Wscore/totalWscore
        rank1_new = int(rank1) + K_1*(wresRatioF1 - Pelo(diffInRankin))
        rank2_new = int(rank2) + K_2*(wresRatioF2 - Pelo(-diffInRankin))
    return (rank1_new, rank2_new)
def calculateRank(rank1, rank2, numberFights1, numberFights2, method, scoreDiff, RoundEnd, to_print):
#M-DEC might be a draw but still one judge migt give more points to the other fighter:w
    #add number of fights to the ranking table
    points = 0
    total = 9
    if method == "CNC":
        return [rank1, rank2]
    if method == "KO/TKO" or method == "SUB":
      # first fighter gets +9 second -9 res
      # retrive existing ranks
        points = 9 
    elif method == "M-DEC" or method == "U-DEC" or method == "S-DEC":
        if RoundEnd > 3:
            total = 15 
        points = abs(int(scoreDiff)) #chush i ne zabyt pro bolshuu summu
        if total < points:
           total = points       
    else:
       print ("Unkwnown win method " + method)
    #At this step points are calculated here comes the magic formula:
    diffInRankin = int(rank1) - int(rank2)
    #determine K:
    (relResult1, relResult2) =( float((total + points))/(2*total) , float((total - points))/(2*total) ) 
    (K_1, K_2) = Kpair(numberFights1, numberFights2)
    rank1_new = int(rank1) + K_1*(float((total + points))/(2*total) - Pelo(diffInRankin))
    rank2_new = int(rank2) + K_2*(float((total - points))/(2*total) - Pelo(-diffInRankin)) 
    if(to_print):
        print ("points ", points, " total ", total, " K1 ", K_1, " K2 ", K_2, "rank1", rank1, "rank2", rank2, " diffInR ", diffInRankin, "Pelo", Pelo(diffInRankin), "result1", relResult1,"res2",relResult2, "method", method, "RoundEnd", RoundEnd, "scoreDiff", scoreDiff, "true or notMdec", method == "M-DEC")
    return (rank1_new, rank2_new, relResult1, relResult2)
def formatName(name):
    name = re.sub(r'-','',name)
    name = re.sub(r'\.','',name)
    return name
# 0 - both less then 3 fights, 1- one less then 3 fights, 2- both more or eq to 3 fights
def getCategory(num1,num2):
    limit  = 3    
    if num1 < limit and num2 < limit:
        return 0
    if num1 < limit or num2 < limit:
        return 1
    return 2
# str1 = 20141004 - 04 10(Oct) 2014, both dates are inclusive i.e. - []
def predictCorr(str1,str2):
    # 0 - both less then 3 fights, 1- one less then 3 fights, 2- both more or eq to 3 fights
    predcorrect_w_s_r_total = []
    for i in range (0,3):
        predcorrect_w_s_r_total.append([0,0,0,0])
    f_info = selectFighteInfo(str1, str2)
    for fightToCall in f_info:
        name1 , name2 = formatName(fightToCall[5]), formatName(fightToCall[6])
        rank1 = retriveRank(name1,fightToCall[0])
        rank2 = retriveRank(name2,fightToCall[0])
        fights1 = retriveNumberFightsAtTime(name1,fightToCall[0])[0][0] - 1
        fights2 = retriveNumberFightsAtTime(name2,fightToCall[0])[0][0] - 1
        category = getCategory(fights1,fights2)
        print("nameW ",name1," nameL ",name2,"rank1",rank1,"rank2",rank2,"f time",fightToCall[0],"f number1",fights1,"f number2",fights2) 
        for i in range(0,3):
            predcorrect_w_s_r_total[category][i] = predcorrect_w_s_r_total[category][i] + int(rank1[0][i]>rank2[0][i]) + 0.5 * int(rank1[0][i]==rank2[0][i])
        predcorrect_w_s_r_total[category][3] = predcorrect_w_s_r_total[category][3] + 1
    return predcorrect_w_s_r_total    
def calculateRanksForDates(str1,str2):
    f_info = selectFighteInfo(str1, str2)
    result = [] 
    for fightToCall in f_info:
        name1 , name2 = formatName(fightToCall[5]), formatName(fightToCall[6])
        rankCheck.createIfEmpty(name1)
        rankCheck.createIfEmpty(name2) 
        rank1 = retriveCurrentRank(name1)
        rank2 = retriveCurrentRank(name2)
        to_print = False
        if (name1, name2 ) == ("TyronWoodley","StephenThompson") or (name2, name1) == ("StephenThompson","TyronWoodley"): 
            to_print = True       
        tuple_wr_str_ran = (fightToCall[0],fightToCall[15],(name1,name2),calculateRankWrestle(rank1[0][0], rank2[0][0], retriveNumberFights(name1)[0][0], retriveNumberFights(name2)[0][0], fightToCall[4], fightToCall[9],fightToCall[10],fightToCall[20], fightToCall[21], fightToCall[13], fightToCall[14], fightToCall[11], fightToCall[12], fightToCall[22], fightToCall[23]),calculateRankStrike(rank1[0][1], rank2[0][1], retriveNumberFights(name1)[0][0], retriveNumberFights(name2)[0][0], fightToCall[4], fightToCall[24], fightToCall[7], fightToCall[8], fightToCall[18], fightToCall[19], fightToCall[22], fightToCall[23]),calculateRank(rank1[0][2], rank2[0][2], retriveNumberFights(name1)[0][0], retriveNumberFights(name2)[0][0], fightToCall[4], fightToCall[24], fightToCall[16], to_print))
        writeRank(tuple_wr_str_ran)   
    return result
#calculate ranks for dates returns FightTime 0,WeightCategory 1,(name1,name2) 2,(rankWrestle1,rankW2) 3, (rankStrike1,rankStrik2) 4,(Rankrank1,Rankrank2,result1,result2) 5
def writeRank(e):
    if len(e[5]) == 4: # otherwise it s nc 
        result1 = int(e[5][2] * 1000)
        result2 = int(e[5][3] * 1000)
        try:
            connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
            # use our connection values to establish a connection
            conn = psycopg2.connect(connect_str)
            # create a psycopg2 cursor that can execute queries
            cursor = conn.cursor()
            #WeightCategory , result
            #print("time", str(e[0]))       #name                     #rankW              #rankS                 #rankRank              #Weight       #Score              #time
            insert_str1 = "INSERT INTO " + e[2][0] + " VALUES ("+str(int(e[3][0]))+"," + str(int(e[4][0]))+","+ str(int(e[5][0]))+",'"+str(e[1])+"',"+str(result1) +",'"+str(e[0])+"');"
            #print("insert str1", insert_str1)
            insert_str2 = "INSERT INTO " + e[2][1] + " VALUES ("+str(int(e[3][1]))+"," + str(int(e[4][1]))+","+ str(int(e[5][1]))+",'"+str(e[1])+"',"+str(result2) +",'"+str(e[0])+"');"
            #print("insert str2", insert_str2)
            cursor.execute(insert_str1)
            cursor.execute(insert_str2)
            conn.commit()
            conn.close()
        except Exception as e:
            print("Uh oh, can't connect. Invalid dbname, user or password?")
            print(e)
def getAndWriteDataByTimeSlice(timeSlice):
    calculateRanksForDates(timeSlice[0], timeSlice[1])
def howManyCorrectPredict():
    predcorrect_w_s_r_total = []
    for i in range (0,3):
         predcorrect_w_s_r_total.append([0,0,0,0])
    for count in range(2012,2017):
         my_slice = (str(count) + "0101", str(count) + "1231")
         res = predictCorr(my_slice[0],my_slice[1])
         for i in range(0,3):
             for j in range(0,4):
                 predcorrect_w_s_r_total[i][j] = predcorrect_w_s_r_total[i][j] + res[i][j]
    # 0 - both less then 3 fights, 1- one less then 3 fights, 2- both more or eq to 3 fights
    for i in range(0,3):
        print ("For category -", i)
        print("num correct pred wrestle, strike, rank, total", predcorrect_w_s_r_total[i][0], predcorrect_w_s_r_total[i][1], predcorrect_w_s_r_total[i][2], predcorrect_w_s_r_total[i][3])
        print("num correct pred wrestle, strike, rank, total", predcorrect_w_s_r_total[i][0]/predcorrect_w_s_r_total[i][3], predcorrect_w_s_r_total[i][1]/predcorrect_w_s_r_total[i][3], predcorrect_w_s_r_total[i][2]/predcorrect_w_s_r_total[i][3], predcorrect_w_s_r_total[i][3])

#start from 01 01 1997 (otherwise there were crazy events with open weight)
def fillRankRangeYears(start_y,end_y):
    for count in range(2017,2018):
        my_slice = (str(count) + "0101", str(count) + "1231")
        getAndWriteDataByTimeSlice(my_slice)

#start from 01 01 1997 (otherwise there were crazy events with open weight)
if __name__ == "__main__":
    howManyCorrectPredict()
    #print ("f select example", fightInfo[0])
#calculate ranks for dates returns FightTime,WeightCategory,result,name1,name2,rankWrestle, rankStrike, Rankrank
    #print ("rankings", calculateRanksForDates("20160305", "20160319")) 
    #writeRanks(calculateRanksForDates("20160305", "20160319"))
#FightTime 0,FightPlace 1,Attendance 2,result 3,method 4,FirstFighterName 5, SecondFighterName 6, StrikesFirstFighter 7, StrikesSecondFighter 8,TakedownsFirstFighter 9, TakedownsSecondFighter
#10, SubAttFirstFighter 11, SubAttSecondFighter 12,PassGuardFirstFighter 13, PassGuardSecondFighter 14, WeightCategory 15, RoundEnd 16, TimeEnd 17, KDFirstFighter 18, KDSecondFighter 19, 
#ReverseFirstFighter 20, ReverseSecondFighter 21, GroundStrikesFirstFighter 22, GroundStrikesSecondFighter 23,ScoreDiff 24,
   
   

