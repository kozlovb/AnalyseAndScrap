import psycopg2
import fillRank

#results - 0 loss, 1 -win, 2 -draw
#getProbaWinLoseDraw()
#FaughtInLastYear1, Last3Results1 = retriveLastResults(name1,fightToCall[0])
#FaughtInLastYear1, LastResultsAverage1, NumOfUFCFights1
def retrieveNumberOfFights(fighterName, time):
    try:
        connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        time_f = "'" + str(time) +"'::date"
        select_str = "SELECT COUNT(*) FROM " + fighterName+" WHERE time < "+ time_f + ";"
        cursor.execute(select_str)
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return int(rows[0][0])-1      
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
def retriveLastResults(fighterName,time):
    try:
        connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        #SELECT * FROM table WHERE id = ? ORDER BY date DESC LIMIT 1;
        time_f = "'" + str(time) +"'::date"
        # The sign < less is chosen as we wanty to see if raiting prior to the fight predicted the result correctly
        select_str = "SELECT * FROM " + fighterName + " WHERE time < "+ time_f + " ORDER BY time DESC LIMIT 4;"
        cursor.execute(select_str)
        rows = cursor.fetchall()
        print ("fighterName", fighterName, "rows", rows)
        conn.commit()
        conn.close()
        # rows [0] - rankwrestle, [1] - rankstrike, [2] - rank, [3] - WeightCategory, [4] - result, [5] - time
        # treat data - first row is init
        #if less then 3 calculate average
        length  = len(rows)-1
        result = 0
        #if 0 return 0.5
        if length == 0:
            return (False, 500)
        print("time of rows [0]", rows[0][5])    
        for e in rows[:length]:
            result = result + e[4]
        faughtInLastYear = False
        timeFaught = int(str(rows[0][5])[0:4])*12 + int(str(rows[0][5])[5:7])
        InitialTime =int(str(time)[0:4])*12 + int(str(time)[5:7])
        if InitialTime < timeFaught + 12:
           faughtInLastYear = True 
        #change lenght to count req   
        return (faughtInLastYear, result/length)      
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
#  height1, reach1, stance1, age1 = retriveFighterInfos(name1)
#[
#weight cAtegories:
#man - 
#Heavyweight, LightHeavyweight, Middleweight, Welterweight, Lightweight, Featherweight, Bantamweight, Flyweight
#woman -
#WomensBantamweight, WomensStrawweight
#]
#AveragesWin rank w, rank s, rank r, height, reach, stance, age, last 3 results, last year fight (yes/no 1/0) 
#AvergaesLoss 
#height1, reach1, stance1, age1 = retriveFighterInfos(name1)
def retriveFighterInfos(name, time):
    try:
        connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        # create a new table with a single column called "name"
        cursor.execute("SELECT * FROM fighters WHERE fighterName = '"+name+"' ;")
        rows = cursor.fetchall()
      #print("fighter data",rows)
        conn.close()
        age = (int(str(time)[0:4])*12 + int(str(time)[5:7]) - (int(str(rows[0][4])[0:4])*12 + int(str(rows[0][4])[5:7])))/12
   ---\Loss_bayesian_data_for_weigh}     return [int(rows[0][1]),int(rows[0][2]),str(rows[0][3]),age]
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
#fightToCall - FightTime 0,FightPlace 1,Attendance 2,result 3,method 4,FirstFighterName 5, SecondFighterName 6, StrikesFirstFighter 7, StrikesSecondFighter 8,TakedownsFirstFighter 9, TakedownsSecondFighter 10, SubAttFirstFighter 11, SubAttSecondFighter 12,PassGuardFirstFighter 13, PassGuardSecondFighter 14, WeightCategory 15, RoundEnd 16, TimeEnd 17, KDFirstFighter 18, KDSecondFighter 19, ReverseFirstFighter 20, ReverseSecondFighter 21, GroundStrikesFirstFighter 22, GroundStrikesSecondFighter 23,ScoreDiff 24
#result - win,draw
#info out: (first_fighter, second_fghter)
#resutl 0, height1 1, reach1 2, stance1 3, age1 4, rank_wres 5, rank_strike 6, rank 7, 
#FaughtInLastYear1 8, LastResultsAverage1 9, NumOfUFCFights1 10, weightCAt 11
def fightInInfoOut(fightToCall):
    print("here is the fight to analyse", fightToCall)
    result = fightToCall[3]
    if result == "win":
        result1 = "win"
        result2 = "loss"
    else: #should be draw
        result1 = "draw"
        result2 = "draw"
    name1 , name2 = fillRank.formatName(fightToCall[5]), fillRank.formatName(fightToCall[6])
    #rank1_w,rank1_s,rank1_r 
    rank1 = fillRank.retriveRank(name1,fightToCall[0])[0]
    (FaughtInLastYear1, LastResultsAverage1) = retriveLastResults(name1,fightToCall[0])
    NumOfUFCFights1 = retrieveNumberOfFights(name1, fightToCall[0])
    (height1, reach1, stance1, age1) = retriveFighterInfos(name1,fightToCall[0])
    rank2 = fillRank.retriveRank(name2,fightToCall[0])[0]
    (FaughtInLastYear2, LastResultsAverage2) = retriveLastResults(name2,fightToCall[0])
    NumOfUFCFights2 = retrieveNumberOfFights(name2, fightToCall[0])
    (height2, reach2, stance2, age2) = retriveFighterInfos(name2,fightToCall[0])
    #"resutl, height1, reach1, stance1, age1, rank_wres, rank_strike, rank, FaughtInLastYear1, LastResultsAverage1, NumOfUFCFights1"
    print ("rank", rank1[0])    
    res1 = (result1,height1,reach1,stance1,age1,rank1[0],rank1[1],rank1[2],FaughtInLastYear1,LastResultsAverage1,NumOfUFCFights1,fightToCall[15])
    res2 = (result2,height2,reach2,stance2,age2,rank2[0],rank2[1],rank2[2],FaughtInLastYear2,LastResultsAverage2,NumOfUFCFights2,fightToCall[15])
    return (res1, res2)
def appendTolistIndict(key ,d, el):
    if key in d.keys():
        l_current = d.get(key)
        l_current.append(el)
    else:
        l_current = []
        l_current.append(el)
    d[key] = l_current
    return d
    
def checkWeightCategory(to_check):
    weights = ["Heavyweight", "LightHeavyweight", "Middleweight", "Welterweight", "Lightweight", "Featherweight", "Bantamweight", "Flyweight", "WomensBantamweight", "WomensStrawweight"]
    return to_check in weights 
class CAveragres:
    def __init__(self):
        weights = ["Heavyweight", "LightHeavyweight", "Middleweight", "Welterweight", "Lightweight", "Featherweight", "Bantamweight", "Flyweight", "WomensBantamweight", "WomensStrawweight"]
        self.Win_av = {}
        self.Draw_av = {}
        self.Loss_av = {}
                      #h  r  a  r_w r_s r_r lastresAv num fights  count
        init_list  = [ 0, 0, 0, 0,  0,  0,   0,      0, 0]
        for w in weights:     
            self.Win_av[w] =  init_list
            self.Draw_av[w] = init_list
            self.Loss_av[w] = init_list
        self.len = len(init_list) 
    def add(self, cont, info):
        cont[0] += info[1] #heights
        cont[1] += info[2] #reach 
        cont[2] += info[4] #age
        cont[3] += info[5] #r_w 
        cont[4] += info[6] #r_s
        cont[5] += info[7] #r_r
        cont[6] += info[9] #last res av
        cont[7] += info[10] # num fights
        cont[8] += 1 # count
        return cont       
    def addData(self,info):
        if checkWeightCategory(info[11]):
            if info[0] == "win":
                self.add(self.win_av, info) 
            elif info[0] == "draw":
                self.add(self.draw_av, info) 
            elif info[0] == "loss":
                self.add(self.loss_av, info) 
            else:
                raise Exception('forgot to test for draw loss win')          
   def getAverages(self):
       res = [self.Win_av, self.Draw_av, self.Loss_av]
       data = [self.Win_av, self.Draw_av, self.Loss_av]
       for i in [0,1,2]:
           for key in data[i].keys():
               for j in range(0:self.len-1)
                   res[i](key)[j] = data[i](key)[j]/data[i](key)[j][self.len-1] 
       return res
if __name__ == "__main__":
    #for count in range(2000,2001):
        #my_slice = (str(count) + "0101", str(count) + "1231")
        #f_info = fillRank.selectFighteInfo(my_slice[0], my_slice[1])
        #for fightToCall in f_info:
        #    if fightToCall[3] == "win" or fightToCall[3] == "draw":
        #        fightInInfoOut(fightToCall)
    my_slice = (str(2015) + "1212", str(2015) + "1213")
    f_info = fillRank.selectFighteInfo(my_slice[0], my_slice[1])
    fightToCall = f_info[11]
    
    print(fightToCall)
    Win_bayesian_data_for_weight = {}
    Draw_bayesian_data_for_weight = {}
    Loss_bayesian_data_for_weight = {}
    for info in fightInInfoOut(fightToCall):
    CAveragres win_av
    CAveragres draw_av
    CAveragres loss_av
    for info in fightInInfoOut(fightToCall):
        if checkWeightCategory(info[11]):
            if info[0] == "win":
                Win_bayesian_data_for_weight = appendTolistIndict(info[11], Win_bayesian_data_for_weight,info) 
            elif info[0] == "draw":
                Draw_bayesian_data_for_weight = appendTolistIndict(info[11], Draw_bayesian_data_for_weight,info) 
            elif info[0] == "loss":
                Loss_bayesian_data_for_weight = appendTolistIndict(info[11], Loss_bayesian_data_for_weight,info) 
            else:
                raise Exception('forgot to test for draw loss win')            
    print ("res", Win_bayesian_data_for_weight, Loss_bayesian_data_for_weight)

# data
#resutl 0, height1 1, reach1 2, stance1 3, age1 4, rank_wres 5, rank_strike 6, rank 7, 
#FaughtInLastYear1 8, LastResultsAverage1 9, NumOfUFCFights1 10, weightCAt 11

       
       
#'ConorMcGregor', 175, 187, 'Orthodox', datetime.date(1988, 7, 14)),    
#(2568, 2647, 2791, 'Featherweight', 1000, datetime.date(2015, 7, 11))
#Lets prepare data for 2 bayesians - 1) by weight category, 2) all weight, for all weights take the diffs


