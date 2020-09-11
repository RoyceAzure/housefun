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
from dotenv import find_dotenv,load_dotenv
import os

load_dotenv(find_dotenv())

class HousefunPipeline:
    def __init__(self):
        dbparams = {
            'host' : os.environ.get('host'),
            'port' : int(os.environ.get('port')),
            'user' : os.environ.get('root'),
            'password' : os.environ.get('password'),
            'database' : os.environ.get('database'),
            'charset' : os.environ.get('charset')
        }
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
        dbparams = {
            'host' : os.environ.get('host'),
            'port' : int(os.environ.get('port')),
            'user' : os.environ.get('root'),
            'password' : os.environ.get('password'),
            'database' : os.environ.get('database'),
            'charset' : os.environ.get('charset'),
            "cursorclass" : cursors.DictCursor  #一班cursor返回 list, 這裡應是返回dict
        }
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
