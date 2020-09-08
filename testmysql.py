from itemadapter import ItemAdapter
import pymysql

class HousefunPipeline:
    def __init__(self):
        dbparams = {
            'host' : '127.0.0.1',
            'port' : 3306,
            'user' : 'root',
            'password' : 'MysqlJackRabbit0618',
            'database' : 'housefun',
            'charset' : 'utf8'
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
        myresult = self.cursor.fetchall()
        for x in myresult:
            print(x)
        return item
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
try:
    test = HousefunPipeline()
    test.process_item({
        'title' : "test",
        "address" : "test address",
        "price" : "123456",
        "connect" : "royce",
        "size" : "60",
        "content" : "test describe",
        'detial' : "test detial"
    },None)
except Exception as e:
    print(e)
finally :
    test.conn.close()
