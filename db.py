import psycopg2
import re
class DB(object):
    def connect(self):
        connect_str = "dbname='testpython' user='kozlov' host='localhost' " + "password='parasha'"
        self.conn = psycopg2.connect(connect_str)
        self.cursor = self.conn.cursor()
    def commit(self):
        self.conn.commit()
    def close(self):
        self.conn.close() 
    def insert_fighters(self, data):
        el_str = ""
        done = True
        for el in data:
            try:
                done = True
                day = el[4]
                month = el[5]
                year = el[6]
                h_str = el[1][0:len(el[1])-1]
                a = h_str[2:]  
                height = int(int(h_str[0])*30.48+int(a)*2.54)
                if el[2] == '--':
                    reach = height
                else: 
                    reach = int(int(el[2][:el[2].find('"')])*2.54)
                el_str = "INSERT INTO fighters VALUES ("+"'"+el[0]+"',"+str(height)+","+str(reach)+",'"+el[3]+"','"+str(year)+"-"+str(month)+"-"+str(day)+"');" 
            except Exception as e:
                print(e)
                print(el[0]) 
                done = False 
            if done:  
                try:
                    self.cursor.execute(el_str)
                    self.conn.commit()
                except Exception as e:
                    s = str(e)
                    if s.find("already exists") == -1:
                        print (e)
                        print ("heppened while inserting line" + el_str)
                    self.conn.rollback()
    def insert_fights(self, data):
        data = self.adopte(data)
        for el in data:
            try:
                self.cursor.execute(el)
                self.conn.commit()   
            except Exception as e:
                print (e)
                print ("heppened while inserting line" + el) 
                self.conn.rollback()
    def adopte(self, data):
        data_res = []
        date = data[1][0]
        date_l = date.split()
        month = month_converter(date[0:3])
        day = date_l[1]
        year = date_l[2]
        fight_place = data[1][1]
        attendance = re.sub(r',','',data[1][2]) 
        #print (data[1])
        for el in data[0]:
            time_end = to_time(el[14])
            weight = re.sub(r'\'','',el[12])
            el_new = ("'"+el[0] + "'","'"+el[1] + "'","'"+el[2] + "'","'"+el[3] + "'") + el[4:12]+("'"+weight + "'",) + (el[13], time_end) + el[15:len(el)-1]
            el_str = "INSERT INTO fights VALUES ("+"'"+str(year)+"-"+str(month)+"-"+str(day)+"','"+str(data[1][1])+"',"+str(attendance)+","
             
            for el in el_new:
                el_str = el_str + str(el) + ","
            el_str = el_str[0:len(el_str)-1]
            el_str = el_str + ");"
            #print (el_str)
            data_res.append(el_str)
        #TODO transform data[1] 
        return (data_res)
def to_time(data):
    minut = int(data[0:data.find(":")])
    sec = int(data[data.find(":")+1:])
    return minut*60+sec 
def month_converter(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month) + 1
   #returns list of tuples where each tuple is - win/draw/nc, method,
    #fighter win, fighter loss, strikes, takedowns, submitions, passage, weight, round end
    # time end, kd, reverse, gr strikes, score_diff symmetric
    #
    # res_fight = 0 - ko/tko, 1 - sub, 2 - dec

def main():
    deb = DB()
    deb.connect()
    test = ([('win', 'KO/TKO', 'ConorMcGregor', 'EddieAlvarez', 32, 9, 0, 0, 0, 0, 0, 0, 'Lightweight', 2, '3:04', 3, 0, 0, 0, 5, 0, -1, -1),('win', 'KO/TKO', 'ConorMcGregor', 'EddieAlvarez', 32, 9, 0, 0, 0, 0, 0, 0, 'Lightweight', 2, '3:04', 3, 0, 0, 0, 5, 0, -1, -1)], ('November 12 2016 ', 'NewYorkCity,NewYork,USA', '20,427'))
    test2 = [('ConorMcGregor', '5\'9"', '74"', 'Southpaw', '14', 7, '1988'),('EddieAlvarez', '5\'9"', '69"', 'Orthodox', '11', 1, '1984')]
    #deb.insert_fihters(test)
    deb.insert_fighters(test2)
    deb.close()
if __name__ == "__main__":
    main()




