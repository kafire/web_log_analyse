#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re
import glob
import time
import sqlite3
import linecache

class DB(object):
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = sqlite3.connect(self.db_file, check_same_thread=False)
        self.db.text_factory = str
        self.cursor = self.db.cursor()
        self.remote_addr = r"?P<ip>[\d.]*"
        self.local_time = r".*?"
        self.method = r"?P<method>\S+"
        self.request = r"?P<request>\S+"
        self.status = r"?P<status>\d+"
        self.bodyBytesSent = r"?P<bodyBytesSent>\d+"
        self.refer = r"""?P<refer>[^\"]*"""
        self.userAgent = r"""?P<userAgent>.*"""
        self.create_table()


    def create_table(self):
        values = '''
           ip varchar(20),
           time varchar(255),
           method varchar(20),
           request varchar(255),
           status int(11),
           body int(11),
           referer varchar(255),
           useragent varchar(255)
       '''
        query = 'CREATE TABLE IF NOT EXISTS info(%s)'% (values)
        self.cursor.execute(query)


    def readline(self,path):
        return linecache.getlines(path)


    def free(self):
        self.cursor.close()

    def disconnect(self):
        self.db.close()

    def parsetime(self,date, month, year, log_time):
        time_str = '%s%s%s %s' % (year, month, date, log_time)
        return time.strptime(time_str, '%Y%b%d %H:%M:%S')

    def run(self):
        result=[]
        for logfile in glob.glob('log/*.log'):
            for logline in self.readline(logfile):
                p = re.compile(r"(%s)\ -\ -\ \[(%s)]\ \"(%s)?[\s]?(%s)?.*?\"\ (%s)\ (%s)\ \"(%s)\"\ \"(%s).*?\"" % (
                    self.remote_addr,self.local_time, self.method, self.request,  self.bodyBytesSent, self.status,self.refer, self.userAgent),
                    re.VERBOSE)
                values = re.findall(p, logline)[0]
                result.append(values)
        print "Success found %s records" % len(result)
        sql='INSERT INTO info VALUES(?,?,?,?,?,?,?,?)'
        try:
            self.cursor.executemany(sql,result)
        except BaseException as e:
            print e
        self.db.commit()
        self.free()
        self.disconnect()


if __name__ == "__main__":
    logs=DB("log.db")
    logs.run()