#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
import glob
import sqlite3
import linecache

class DB(object):
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = sqlite3.connect(self.db_file, check_same_thread=False)
        self.db.text_factory = str
        self.cursor = self.db.cursor()
        self.remote_addr = r"?P<ip>[\d.]*"
        self.local_time = r"?P<time>.*?"
        self.method = r"?P<method>\S+"
        self.request = r"?P<request>\S+"
        self.status = r"?P<status>\d+"
        self.bodyBytesSent = r"?P<bodyBytesSent>.+"
        self.create_table()


    def create_table(self):
        values = '''
           ip varchar(20),
           time varchar(255),
           method varchar(20),
           request varchar(255),
           status int(11),
           body varchar(255)
       '''
        query = 'CREATE TABLE IF NOT EXISTS info(%s)'% (values)
        self.cursor.execute(query)


    def readline(self,path):
        return linecache.getlines(path)


    def free(self):
        self.cursor.close()

    def disconnect(self):
        self.db.close()


    def run(self):
        result=[]
        for logfile in glob.glob('log/*.log'):
            for logline in self.readline(logfile):
                p = re.compile(r"(%s)\ -\ -\ \[(%s)]\ \"(%s)?[\s]?(%s)?.*?\"\ (%s)\ (%s)" % (
                    self.remote_addr,self.local_time, self.method, self.request, self.status,self.bodyBytesSent),
                    re.VERBOSE)
                values = re.findall(p, logline)[0]
                result.append(values)
        print "Success found %s records" % len(result)
        sql='INSERT INTO info VALUES(?,?,?,?,?,?)'
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