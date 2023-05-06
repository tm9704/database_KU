import pymysql
import numpy as np

class Database():

    def __init__(self):
         self.db = pymysql.connect(host = 'localhost', port=3306, user = 'root', password='1234', db='rsp', charset='utf8')
         self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args = {}):
        self.cursor.execute(query, args)
    
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row
    
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()
    
    def close(self):
        self.db.close()
     
        
    


