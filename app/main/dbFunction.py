import app.main.dbModule as dbModule
import math
from flask import request

class DatabaseFunction():
    def getRankList(self):
        
        db_class = dbModule.Database()

        sql = f"""SELECT  id, point, ROUND(IFNULL(odds, 0),1) as odds, ranking 
FROM (SELECT id, point, (winCount/(winCount+loseCount))*100 as odds, rank() over (order by point desc) as ranking FROM rank_info 
ORDER BY point DESC LIMIT 10) sub""" #최대 10개만 출력되게 제한, 랭킹정보 구현
        rows = db_class.executeAll(sql)

        list = []
        for row in rows:
            list.append(row)
        
        db_class.close()
        return list

    #내 랭킹 가져오는 sql
    def getMyRank(self,id):
        db_class = dbModule.Database()

        sql = f"""SELECT * from (SELECT  id, point, winCount, loseCount,totalCount, ROUND(IFNULL(odds, 0),1) as odds, ranking
FROM (SELECT id, point, winCount, loseCount,(winCount+loseCount) as totalCount, (winCount/(winCount+loseCount))*100 as odds, rank() over (order by point desc) as ranking FROM rank_info 
ORDER BY point DESC) sub) subquery WHERE id='{id}'"""  # 최대 10개만 출력되게 제한
        rows = db_class.executeAll(sql)
        db_class.close()
        return rows

    def getProfile(self):
        
        db_class = dbModule.Database()

        sql = f"""SELECT * FROM profile WHERE id != 'user'"""
        rows = db_class.executeAll(sql)
        
        db_class.close()
        return rows

    def getMyProfile(self,id):

        db_class = dbModule.Database()

        sql = f"""SELECT * FROM profile WHERE id='{id}'"""
        rows = db_class.executeAll(sql)

        db_class.close()
        return rows

    def getGameLog(self):
        db_class = dbModule.Database()
        sql = f"""SELECT * FROM game_log WHERE date != 0 ORDER BY date"""
        rows = db_class.executeAll(sql)
        return rows

    def searchLog(self, searchText):
        db_class = dbModule.Database()
        sql = f"""SELECT * FROM game_log WHERE id = '{searchText}' and date != 0 ORDER BY date DESC"""
        rows = db_class.executeAll(sql)
        check = db_class.executeOne(sql)
        try:
            if(check["id"]):
                return True, rows
        except:
            return False, 0
        
    def searchUserLog(self, searchText):
        db_class = dbModule.Database()
        sql = f"""SELECT * FROM profile WHERE id = '{searchText}'"""
        rows = db_class.executeAll(sql)
        check = db_class.executeOne(sql)
        try:
            if(check["id"]):
                return True, rows
        except:
            return False, 0   

    def deleteGameLog(self, game_num):
        db_class = dbModule.Database() 
        sql_select = f"""SELECT * FROM (SELECT * FROM game_log ORDER BY date DESC LIMIT 18446744073709551615) AS order_date GROUP BY id"""
        select = db_class.executeAll(sql_select)
        for i in select:
            if(i["game_num"] == game_num):
                return False
        sql_delete = f"""DELETE FROM game_log WHERE game_num = '{game_num}'"""
        db_class.execute(sql_delete)
        db_class.commit()
        return True




    def gameDataToDB(self,id,user_choice,cpu_choice,result,date,cur_point,game_num):    #db에 게임로그 저장해주는 함수
        db_class = dbModule.Database()
        sql = f"""
            INSERT INTO game_log 
            VALUES ("{id}","{user_choice}", "{cpu_choice}", "{result}", "{date}", "{cur_point}", "{game_num}")
            """
        sql_update_rank=""
        if(result=="Win"):
            sql_update_rank = f"""
                        UPDATE rank_info SET point = "{cur_point}", winCount= winCount+1 WHERE id='{id}';
                        """
        else:
            sql_update_rank = f"""
                        UPDATE rank_info SET point ="{cur_point}", loseCount= loseCount+1 WHERE id='{id}';
                        """
        #랭킹테이블 승,패,포인트 업데이트 sql

        db_class.execute(sql)
        db_class.execute(sql_update_rank)
        db_class.commit()
        return True

    def getCurPoint(self,id):              #DB에서 id가 같은 것중에 최근 날짜순으로 자신의 point를 리턴해주는 함수
        db_class = dbModule.Database()
        sql = f"""
            SELECT cur_point FROM game_log
            WHERE id='{id}'
            ORDER BY date DESC;
            """
        rows = db_class.executeOne(sql)
        return rows["cur_point"]


    def accountDataToDB(self,id, passwd, nick, name):
        db_class = dbModule.Database()

        sql_account = f"""
            INSERT INTO profile (id, password, nickname,name)
            VALUES ("{id}", "{passwd}", "{nick}","{name}");
            """ #회원테이블
        sql_rank = f"""
            INSERT INTO rank_info (id, point,  winCount, loseCount)
            VALUES ("{id}", "0", "0","0");
            """ #랭킹테이블
        try:
            db_class.execute(sql_account)
            db_class.execute(sql_rank)
            db_class.commit()
            return True
        except:
            return False

    def initialgameDB(self,id,game_num):                 # 로그인시 game_log초기값 설정해주는 함수
        db_class = dbModule.Database()
                                                         # 로그인한 id 저장해주고, primary key인 game_num도 설정
        sql = f"""
            INSERT INTO game_log
            VALUES ("{id}","Login","0","0","0",0,"{game_num}")
            """
        try:
            db_class.execute(sql)
            db_class.commit()
            return True
        except:
            return False

    def checkLoginDB(self,id, passwd):
        db_class = dbModule.Database()
        
        sql = f"""
            SELECT * FROM profile
            WHERE id ='{id}' and password = '{passwd}';
            """

        try: 
            rows = db_class.executeOne(sql)
            return True, rows["nickname"],rows["name"]
        except:
            return False, 0, 0

    def banUser(self,id,reason):    #유저 밴시키는 함수
        db_class = dbModule.Database()
        sql = f"""
            INSERT INTO ban 
            VALUES ("{id}","{reason}")
            """
        db_class.execute(sql)
        db_class.commit()
        return True

    def unbanUser(self,id):    #유저 밴푸는 함수
        db_class = dbModule.Database()
        sql = f"""
            DELETE FROM ban
            WHERE id="{id}";
            """
        db_class.execute(sql)
        db_class.commit()
        return True

    def banList(self):    #밴 여부와 사유 가져오는 함수
        db_class = dbModule.Database()
        sql = f"""
            SELECT * FROM ban;
            """
        rows = db_class.executeAll(sql)

        db_class.close()
        return rows

        

        
