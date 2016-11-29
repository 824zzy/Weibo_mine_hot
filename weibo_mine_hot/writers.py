# -*- coding:utf-8 -*-
import sys
import MySQLdb
import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')


class Content(object):
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "root"
        self.passwd = "123456"
        self.port = 3306
        self.db = "TestZhu"
        self.charset = "utf8"
        self.use_unicode = "True"
        self.conn = None
        self.cur = None
        self.initDb()

    def initDb(self):
        try:
            self.conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user,
                                        passwd=self.passwd, db=self.db, charset=self.charset,
                                        use_unicode=self.use_unicode)
            self.cursor = self.conn.cursor()

        except MySQLdb.Error, e:
            print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
            print 'Failed to connect to weibo! Please check your config file and confirm your weibo is open'
            sys.exit(-1)
        print 'Success connect weibo'

    def insertIntoDB1(self, m):
        try:
            self.cursor.execute('replace into WeiboInfo1 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', m)
            self.conn.commit()
            print 'success1'
        except:
            pass
    def inserIntoDB2(self, m):
        try:
            self.cursor.execute('replace into PrimaryWeiboInfo VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',m)
            self.conn.commit()
            print 'success2'
        except:
            pass
    def closeResource(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()


def main():
    pass


if __name__ == '__main__':
    main()
