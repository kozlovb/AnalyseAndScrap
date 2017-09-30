import urllib.request
import psycopg2
import sys
sys.path.append('/usr/lib/python2.7/dist-packages')
from bs4 import BeautifulSoup
import re
import db
class Scraper(object):
    #loops over each fight pages 
    #extracts KD number, reverse, ground strikes 
    def getFightDetailsSum(self, addr):
        fightpages = self.getDetailedUFCFightPages(addr)
        res = []
        for el in fightpages:
             res.append(self.getFightDetails(el))
        return res
    def getPages(self,addr,search_str):
        page = urllib.request.urlopen(addr)
        soup = BeautifulSoup(page, "html5lib")
        txt = soup.prettify()
        res =  []
        pos_link_to_fight = 0
        while pos_link_to_fight!=-1:
            pos_link_to_fight = txt.find(search_str, pos_link_to_fight+1)
            end_pos = min(txt.find('\"',pos_link_to_fight), txt.find(')',pos_link_to_fight), txt.find('\'',pos_link_to_fight))
            if pos_link_to_fight != -1:
                if txt[pos_link_to_fight:end_pos] not in res:
                    res.append(txt[pos_link_to_fight:end_pos])
        return res
    def getDetailedFightersPages(self, addr):
        return self.getPages(addr, 'http://www.fightmetric.com/fighter-details/')
    def getDetailedUFCFightPages(self, addr):
        return self.getPages(addr, 'http://www.fightmetric.com/fight-details/')
    def extractPair(self, table, row_number, column_number):
        rows = table.findAll("tr")
        cells_first_fighter = rows[row_number].findAll("td")
        p = cells_first_fighter[column_number].findAll("p")
        res = [p[0].text, p[1].text]
        return res
    def extractFirst(self, table, row_number, column_number):
        rows = table.findAll("tr")
        cells_first_fighter = rows[row_number].findAll("td")
        p = cells_first_fighter[column_number].findAll("p")
        return p[0].text

    def toInt(self, pair):
        intRes = []
        for el in pair:
            m = re.search(r'([0-9]+)', el) 
            intRes.append(int(m.group(0)))
        return intRes
    def hlp(self,text, pos):
        tmp = re.sub(r'\s','',text)
        return tmp[pos:] 
    def getFighter(self, addr):
        try:
            return self.getFighterInt(addr)
        except Exception as e:
            print ("failed at getFighter" + str(addr))
            print (e)
            raise
    def getFighterInt(self, addr):
        page = urllib.request.urlopen(addr)
        soup = BeautifulSoup(page, "html5lib")
        txt = soup.prettify()
        span = soup.findAll('span', {'class': 'b-content__title-highlight'})
        li = soup.findAll('li', {'class': 'b-list__box-list-item b-list__box-list-item_type_block'}) 
        name = re.sub(r'\s','',span[0].text)
        name = re.sub(r'\'','',name)
        height = self.hlp(li[0].text, len('heightt'))
        reach = self.hlp(li[2].text, len('reachc'))
        stance = self.hlp(li[3].text, len('stancee'))
        if stance != "Southpaw" or stance != 'Orthodox':
            stance = "Orthodox"
        dob = self.hlp(li[4].text, len('dobb'))
        if height == '--':
            height = "5'10'" 
        if dob == '--':
            dob = 'May26,1976'
         
        month = month_converter(dob[:3])
        day = dob[3:dob.find(',')]
        year = dob[dob.find(',')+1:]      
        return (name, height, reach, stance, day, month, year)

    def getFightDetails(self, addr):
        page = urllib.request.urlopen(addr)
        soup = BeautifulSoup(page, "html5lib")
        text = soup.prettify()
        #totals_table
        section = soup.findAll('section', {'class': 'b-fight-details__section js-fight-section'})
        totals_table = section[1]
        #strikes table 
        tbody = soup.findAll('tbody', {'class': 'b-fight-details__table-body'})
        strikes_table = tbody[2]
        #Fighters
        fighters = self.extractPair(totals_table, 1, 0)
        fighters = [re.sub(r'\s','',fighters[0]),re.sub(r'\s','',fighters[1])]
        fighters = [re.sub(r'\'','',fighters[0]),re.sub(r'\'','',fighters[1])]  
        #KD 
        kd = self.toInt(self.extractPair(totals_table, 1, 1))
        #Reverse
        reverse = self.toInt(self.extractPair(totals_table, 1, 9))  
        #ground strikes
        gr = self.toInt(self.extractPair(strikes_table, 0, 8))
        txt = soup.get_text()
        txt_string = str(txt.encode('utf-8'))
        line = re.sub(r'\s+', ' ', txt_string)
        pos_method = line.find("Method")
        pos_round = line.find("Round")
        score_diff = -1
        res_fight = 0 
        #if line.find("KO/TKO", pos_method, pos_round) != -1:
        #    res_fight = 0
        #elif line.find("Submission", pos_method, pos_round) != -1:
        #    res_fight = 1
        if line.find("Decision", pos_method, pos_round) != -1:
            score_diff = 0
            res_fight = 2 
            pos_beg = line.find("Details")
            pos_end = line.find("Totals")
            score_str = re.findall(r'[0-9]+', line[pos_beg:pos_end])
            pair = 0
            for counter, el in enumerate(score_str):
                if counter % 2 == 0:
                    pair = int(el)
                else:
                    score_diff = score_diff + int(el) - pair
        return (fighters, kd, reverse, gr, [abs(score_diff), abs(score_diff)])               
    def getMainPage(self, addresse):
        try: 
            return self.getMainPageInt(addresse)
        except Exception as e:
            print ("failed at getMainPage")
            print (e)
            raise    
    def getMainPageInt(self, addresse):
        page = urllib.request.urlopen(addresse)
        soup = BeautifulSoup(page, "html5lib")
        text = soup.get_text()
        text = str(text.encode('utf-8'))
        txt = soup.prettify()
        #print (txt.encode('utf-8'))
        tbody = soup.findAll('tbody', {'class': 'b-fight-details__table-body'})
        strikes_table = tbody[0]
        rows_number = len(strikes_table.findAll("tr"))
        res = [] 
        fightpages = self.getDetailedUFCFightPages(addresse)
        for i in range(0, rows_number): 
            try: 
                res_fight = re.sub(r'\s','', self.extractFirst(strikes_table, i, 0))
                fighters = self.extractPair(strikes_table, i, 1)
                fighters = [re.sub(r'\s','',fighters[0]),re.sub(r'\s','',fighters[1])]
                strikes = self.toInt(self.extractPair(strikes_table, i, 2))
                res_method = re.sub(r'\s','', self.extractFirst(strikes_table, i, 7))
                tp = (res_fight, res_method, re.sub(r'\'','',fighters[0]), re.sub(r'\'','',fighters[1]), self.toInt(self.extractPair(strikes_table, i, 2))[0],self.toInt(self.extractPair(strikes_table, i, 2))[1], self.toInt(self.extractPair(strikes_table, i, 3))[0],self.toInt(self.extractPair(strikes_table, i, 3))[1], self.toInt(self.extractPair(strikes_table, i, 4))[0],self.toInt(self.extractPair(strikes_table, i, 4))[1],self.toInt(self.extractPair(strikes_table, i, 5))[0],self.toInt(self.extractPair(strikes_table, i, 5))[1], re.sub(r'\s','', self.extractFirst(strikes_table, i, 6)), int(re.sub(r'\s','',self.extractFirst(strikes_table, i, 8))), re.sub(r'\s','',self.extractFirst(strikes_table, i, 9))   )
                details = self.getFightDetails(fightpages[i])
                if(tp[2] != details[0][0]):
                    details = self.swapTouple(details)
                for det in details[1:]:
                    #print (det)
                    tp = tp + (det[0], det[1])
                #tp = tp + details[1:]
                res.append(tp)
            except Exception as e:
                print(e)
                print ("occured while on ")
                print (str(addresse))   
        return res
    def swapTouple(self, tp):
        for i in range(0, len(tp)):
            el = tp[i]
            if not isinstance(el, int):
                tp[i][0], tp[i][1] = tp[i][1], tp[i][0] 
        return tp  

    def getLocDateAttend(self, addresse):
        page = urllib.request.urlopen(addresse)
        soup = BeautifulSoup(page, "html5lib")
        ul = soup.findAll('ul', {"class": "b-list__box-list"})
        li = ul[0].findAll("li")
        date = re.sub(r'\s',' ',li[0].text)
        date = re.sub(r',','',date)
        date = re.sub(r'  ','',date)
        #date = li[0].text
        date = date[len("Date:"):]
        location = re.sub(r'\s','',li[1].text)
        location = location[len("Location:"):]  
        attendance = re.sub(r'\s','',li[2].text)
        attendance = attendance[len("Attendance:"):]
        if len(attendance) == 0:
            attendance = "0"   
        return (date, location, attendance)
    def getFightData(self, addr):
        return (self.getMainPage(addr) , self.getLocDateAttend(addr))
    def getFighters(self, addr):
        res = []
        addreses = self.getDetailedFightersPages(addr)
        for e in addreses:
           res.append(self.getFighter(e))
        return res
def month_converter(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month) + 1
def getAllAddr():
    res = [] 
    start_page = "http://www.fightmetric.com/statistics/events/completed?page=all"
    page = urllib.request.urlopen(start_page)
    soup = BeautifulSoup(page, "html5lib")
    href_tags = soup.find_all(href=True)
    txt = soup.prettify()
    for a in soup.find_all('a', {"class": "b-link b-link_style_black"}, href=True):
        res.append(a['href'])
    return res  
        

    #print (href_tags)
def getOnePage(addr):
    scr = Scraper()
    deb = db.DB()
    deb.connect()
    data_fight = scr.getFightData(addr)
    deb.insert_fights(data_fight)
    data_fighter = scr.getFighters(addr)
    deb.insert_fighters(data_fighter)
    deb.close()

#main function
def main(number_fights_to_retrieve):
    #activate for one addr
    #el = "http://fightmetric.com/event-details/1c3f5e85b59ec710"
    #try: 
    #    getOnePage(el)
    #except Exception as e:
    #    print (e)
    #    print ("failed at addresse ")
    #    print (el)

    addrs = getAllAddr()
    debut = addrs[0:number_fights_to_retrieve]
    for el in debut:
        try:
            getOnePage(el)
        except Exception as e:
            print ("failed at addresse ")
            print (el)
            print (" with ")
            print (e)    
    #returns list of tuples where each tuple is - win/draw/nc, method,
    #fighter win, fighter loss, strikes, takedowns, submitions, passage, weight, round end
    # time end, kd, reverse, gr strikes, score_diff symmetric
    #
    # res_fight = 0 - ko/tko, 1 - sub, 2 - dec
    #fighter = scr.getDetailedFightersPages(addr_mcgreg_alva)[0]
if __name__ == "__main__":
    addrs = getAllAddr()
    print (addrs[0:46])
    #print (addrs[380:386])
    #main runs scrap for last ? fights
    number_fights_to_retrieve = 2
    main(number_fights_to_retrieve)

