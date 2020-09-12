# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
#使用adbap 提供的connectpool 異步寫入SQL
from twisted.enterprise import adbapi
from pymysql import cursors
import os
from enviroment import config
import csv

class HousefunPipeline:
    def __init__(self):
        dbparams  = config._Dbparams
        self.conn = pymysql.connect(**dbparams)
        if self.conn:
            print("DB init success")
        else:
            print("DB init fail")
        self.cursor = self.conn.cursor()
        self._sql = None
        self._Insertsql = None
    def process_item(self, item, spider):
        self.cursor.execute(self.Insertsql,(item['title'],item['address'],item['price'],item['connect'],item['size'],item['content'],item['detial'])) 
        self.conn.commit()
    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            SELECT * FROM  renthouse;
            """
        print("self.sql : {}".format(self._sql))
        return self._sql

    @property
    def Insertsql(self):
        if not self._Insertsql:
            self._Insertsql = """
            insert into renthouse (title, address, price, connect, size, content, detial) values (%s,%s, %s, %s, %s,%s, %s);
            """
        print("self._Insertsql : {}".format(self._Insertsql))
        return self._Insertsql

class HousefunTwistedPipeline(object):
    def __init__(self):
        dbparams  = config._Dbparams
        self.dbpol = adbapi.ConnectionPool('pymysql', **dbparams) #根據不同DB lib 建立連接池 (建立對應的conn物件)
        self._Insertsql = None

    @property
    def Insertsql(self):
        if not self._Insertsql:
            self._Insertsql = """
            insert into renthouse (title, address, price, connect, size, content,detial) values (%s,%s, %s, %s, %s,%s, %s);
            """
        print("self._Insertsql : {}".format(self._Insertsql))
        return self._Insertsql
    def process_item(self, item, spider):
        print("="*30)
        print("in pipline")
        print("item :{}".format(item))
        defer = self.dbpol.runInteraction(self.Insert_item, item) #將要執行的異步function帶入
        defer.addErrback(self.handle_error, item, spider)
    def Insert_item(self, cursor , item):
        cursor.execute(self.Insertsql,(item['title'],item['address'],item['price'],item['connect'],item['size'],item['content'], item['detial'])) 
        return item
    def handle_error(self, error, item, spider):
        print("="*10 + "error" + "="*10)
        print(error)
        print("="*10 + "error" + "="*10)

class HousefunCsvPipeline(object):
    def __init__(self):
        self.saveDir = os.path.join(config._BaseDir,config._SaveDir)
        self.savePath = config._saveCsvPath
        print(self.saveDir)
        print(self.savePath)
        if not os.path.exists(self.saveDir):
            os.mkdir(self.saveDir)
        if not os.path.exists(self.savePath):
            with open(self.savePath,"w",encoding="utf-8",newline='') as f:
                header = ["title","address","price","connect","size","content","detial"]
                csvWriter = csv.writer(f,delimiter=',')
                csvWriter.writerow(header)
    def process_item(self, item, spider):
        with open(self.savePath,"a",encoding="utf-8",newline='') as f:
            csvWriter = csv.writer(f,delimiter=',')
            title = item['title']
            address = item['address']
            price = item['price']
            connect = item['connect']
            size = item['size']
            content = item['content']
            detial = item['detial']
            writeList = [title,address,price,connect,size,content,detial]
            csvWriter.writerow(writeList)