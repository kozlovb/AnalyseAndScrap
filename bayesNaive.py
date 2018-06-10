import psycopg2
import fillRank
import dropCreateAverages
import math
#results - 0 loss, 1 -win, 2 -draw
#getProbaWinLoseDraw()
#FaughtInLastYear1, Last3Results1 = retriveLastResults(name1,fightToCall[0])
#FaughtInLastYear1, LastResultsAverage1, NumOfUFCFights1
def getWeights():
    return ["Heavyweight", "LightHeavyweight", "Middleweight", "Welterweight", "Lightweight", "Featherweight", "Bantamweight", "Flyweight", "WomensBantamweight", "WomensStrawweight"]
   
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
        for e in rows[:length]:
            result = result + e[4]
        faughtInLastYear = False
        timeFaught = int(str(rows[0][5])[0:4])*12 + int(str(rows[0][5])[5:7])
        InitialTime = int(str(time)[0:4])*12 + int(str(time)[5:7])
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
categories  = ("Heavyweight", "LightHeavyweight", "Middleweight", "Welterweight", "Lightweight", "Featherweight", "Bantamweight", "Flyweight", "WomensBantamweight", "WomensStrawweight", "WomensFeatherweight")
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
        return [int(rows[0][1]),int(rows[0][2]),str(rows[0][3]),age]
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
    name1, name2 = fightToCall[5], fightToCall[6]
    name1_f , name2_f = fillRank.formatName(fightToCall[5]), fillRank.formatName(fightToCall[6])
#    print("name2",name2)
    #rank1_w,rank1_s,rank1_r 
    rank1 = fillRank.retriveRank(name1_f,fightToCall[0])[0]
    (FaughtInLastYear1, LastResultsAverage1) = retriveLastResults(name1_f,fightToCall[0])
    NumOfUFCFights1 = retrieveNumberOfFights(name1_f, fightToCall[0])
    (height1, reach1, stance1, age1) = retriveFighterInfos(name1,fightToCall[0])
    rank2 = fillRank.retriveRank(name2_f,fightToCall[0])[0]
    (FaughtInLastYear2, LastResultsAverage2) = retriveLastResults(name2_f,fightToCall[0])
    NumOfUFCFights2 = retrieveNumberOfFights(name2_f, fightToCall[0])
    (height2, reach2, stance2, age2) = retriveFighterInfos(name2,fightToCall[0])
    #'win', datetime.date(2015, 12, 10), 'KailinCurran', 162, 165, 'Orthodox', 24.666666666666668, 2471, 2489, 2362, True, 0.0, 2, 'WomensStrawweight'
            #"resutl, time,           name,           height1, reach1, stance1, age1, rank_wres, rank_strike, rank, FaughtInLastYear1, LastResultsAverage1, NumOfUFCFights1"
    res = (result, fightToCall[0], fightToCall[5], height1, reach1, stance1, age1, rank1[0], rank1[1],rank1[2],FaughtInLastYear1,LastResultsAverage1,NumOfUFCFights1, fightToCall[6], height2,reach2,stance2,age2,rank2[0],rank2[1],rank2[2],FaughtInLastYear2,LastResultsAverage2,NumOfUFCFights2,fightToCall[15])
    return res
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
    weights = getWeights()
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
        self.length = len(init_list) 
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
                for j in range(0, self.length-1):
                    res[i](key)[j] = data[i](key)[j]/data[i](key)[j][self.length-1] 
        return res
def calculateAveragesForCat(category):
    table_names = ("Average"+category+"Win","Average"+category+"Loss","Average"+category+"Draw")
    result = []
    for table in table_names:
        result.append(dropCreateAverages.selectAverages(table))
    return result
def calculateVarHeiReachAgeLastResAvNumUFCFight(category):
    table_names = ("Average"+category+"Win","Average"+category+"Loss","Average"+category+"Draw")
    result = []
    for table in table_names:
        result.append(dropCreateAverages.calculateVarHeiReachAgeLastResAvNumUFCFight(table))
    return result
def normDistr(x,av,var):
    return math.exp((-(x-av)*(x-av)/(2*var))) / math.sqrt(2 * 3.141592 * var)
def probaDiffExpH_R_A_LRAV_numUFCF(category, h1, r1, a1, lrav1, numUFCF1, h2, r2, a2, lrav2, numUFCF2):
    av = dropCreateAverages.selectDiffAveragesCat(category)
    var = dropCreateAverages.selectDiffVarCat(category, av)
    av_win = av[0][1]
    var_win = var[0][1]
    av_draw = av[1][1]
    var_draw = var[1][1]
    diff1win = [h1-h2, r1-r2, a1-a2, lrav1-lrav2, numUFCF1-numUFCF2]
    diff2win = []
    res = []
    for i in range(0,len(diff1win)):
        diff2win.append(-diff1win[i])
    for i in range(0,len(diff1win)):
        proba1win = normDistr(diff1win[i], av_win[i], var_win[i]) 
        proba2win = normDistr(diff2win[i], av_win[i], var_win[i])
        proba1win, proba2win = Normilize(proba1win, proba2win, 1)
        print("AfterNormiliation p1win, p2win", proba1win, proba2win)
        if(var_draw[i] == 0):
            probaDraw = -1
        else:
            probaDraw = math.exp(-(diff1win[i]-av_draw[i])*(diff1win[i]-av_draw[i])/(2*var_draw[i])) / (math.sqrt(2*3.141592*var_draw[i]))
        res.append([proba1win, proba2win, probaDraw])
    return res
def DrawORWLProba():
    #select throw all categories
    tmp = []
    weights = getWeights()
    for e in weights:
        tmp.append(dropCreateAverages.getCountsCat(e))
    res = [0, 0] 
    for e in tmp:
        res[0] = res[0] + e[0]
        res[1] = res[1] + e[1]
    return (res[0]/(res[0]+res[1]), res[1]/(res[0]+res[1]))
def probaExpH_R_A_LRAV_numUFCF(category, h1, r1, a1, lrav1, numUFCF1, h2, r2, a2, lrav2, numUFCF2):
    av = dropCreateAverages.selectAveragesCat(category)
    var = dropCreateAverages.selectVarCat(category, av)
    print("Averages ", av[0][1])
    print("Variat", var[0][1])
    av_win = av[0][1]#second half is loose actually
    var_win = var[0][1]
    av_draw = av[1][1]
    var_draw = var[1][1]
    data1 = [h1, r1, a1, lrav1, numUFCF1]
    data2 = [h2, r2, a2, lrav2, numUFCF2]
    res = []
    for i in range(0,len(data1)):
        print("data1, av, var ", data1[i], av_win[i], var_win[i])
        proba1win = normDistr(data1[i], av_win[i], var_win[i])
        print("proba " , proba1win)
        proba1loose = normDistr(data1[i], av_win[i+len(data1)], var_win[i+len(data1)]) 
        print("1win", proba1win, "1loose", proba1loose)
        proba2win = normDistr(data2[i], av_win[i], var_win[i])
        proba2loose = normDistr(data2[i], av_win[i+len(data1)], var_win[i+len(data1)])
        print("data2, av, var ", data2[i], av_win[i], var_win[i])
        print("2win", proba2win, "2loose", proba2loose)
        proba1win, proba2win = Normilize(proba1win, proba2win, 1)
        proba1loose, proba2loose = Normilize(proba1loose, proba2loose, 1)
        print("After normalization", "proba1win", proba1win, "proba2win", proba2win, "probaloose1", proba1loose, "probaloose2", proba2loose)
        proba1win, proba2win = Normilize(math.sqrt(proba1win*proba2loose), math.sqrt(proba2win*proba1loose), 1)
        print("After normilization resulting pwin1 and pwin2", proba1win, proba2win)
        probaDraw = -1
        res.append([proba1win, proba2win, probaDraw])
    return res
def Normilize(p1,p2,total):
    return [total * (p1/(p1+p2)), total * (p2/(p1+p2))]
def calculateDiffProbas(category, h1, r1, a1, lrav1, numUFCF1, h2, r2, a2, lrav2, numUFCF2):
    WLProba, DrawProba = DrawORWLProba()
    pdraw = DrawProba
    pwin1 = WLProba/2
    pwin2 = WLProba/2
    proba_h_r_a_lrav_numUFC = probaDiffExpH_R_A_LRAV_numUFCF(category, h1, r1, a1, lrav1, numUFCF1, h2, r2, a2, lrav2, numUFCF2)
    for e in proba_h_r_a_lrav_numUFC:
        pwin1 = pwin1 * e[0]
        pwin2 = pwin2 * e[1]
    pwin1, pwin2 = Normilize(pwin1, pwin2, 1-pdraw)
    return [pwin1, pwin2, pdraw] 
def calculateProbas(category, h1, r1, a1, lrav1, numUFCF1, h2, r2, a2, lrav2, numUFCF2):
    WLProba, DrawProba = DrawORWLProba()
    pdraw = DrawProba
    pwin1 = WLProba/2
    pwin2 = WLProba/2
    proba_h_r_a_lrav_numUFC = probaExpH_R_A_LRAV_numUFCF(category, h1, r1, a1, lrav1, numUFCF1, h2, r2, a2, lrav2, numUFCF2)
    for e in proba_h_r_a_lrav_numUFC:
        pwin1 = pwin1 * e[0]
        pwin2 = pwin2 * e[1]
    pwin1, pwin2 = Normilize(pwin1, pwin2, 1-pdraw)
    return [pwin1, pwin2, pdraw]     
if __name__ == "__main__":
    #for count in range(2000,2001):
        #my_slice = (str(count) + "0101", str(count) + "1231")
        #f_info = fillRank.selectFighteInfo(my_slice[0], my_slice[1])
        #for fightToCall in f_info:
        #    if fightToCall[3] == "win" or fightToCall[3] == "draw":
        #        fightInInfoOut(fightToCall)
    my_slice = (str(2015) + "1201", str(2015) + "1231")
    f_info = fillRank.selectFighteInfo(my_slice[0], my_slice[1])
    fightToCall = f_info[11]
    for category in categories:
        dropCreateAverages.CreateAveragesTable(category)
    for fightToCall in f_info:
        info = fightInInfoOut(fightToCall)
        print(info)
        dropCreateAverages.writeInDB(info)  
    dropCreateAverages.selecttest()
    
#WL table - # h  r  a  lrAv numUFCF
    av = dropCreateAverages.selectDiffAveragesCat('Featherweight')
    print("av before call", av)
    var = dropCreateAverages.selectDiffVarCat('Featherweight', av)
    print('var',var)
    print('draw or wl proba', DrawORWLProba())

    print(calculateDiffProbas('Featherweight', 180, 187, 37, 600, 14, 177, 185, 36, 600, 7))
    print('Without diffs')
    print(calculateProbas('Featherweight', 180, 187, 37, 600, 14, 177, 185, 36, 600, 7))
#TODO switch age and NumUFCFights to most succesfull fighter, 
# age + NumUFCfights are correlated, reach + heights are correlated.     
#For now ignore draw i.e. Pdraw is 0.3 * Pdraw  Pwin1 = Pwin/2 * (p*p*p - sum is normilized to 0.7)
   
     
#('win', datetime.date(2015, 12, 19), 'CharlesOliveira', 177, 187, 'Orthodox', 26.166666666666668, 2599, 2507, 2639, True, 592.3333333333334, 14, 'MylesJury', 177, 185, 'Orthodox', 27.166666666666668, 2590, 2601, 2680, True, 629.3333333333334, 7, 'Featherweight')