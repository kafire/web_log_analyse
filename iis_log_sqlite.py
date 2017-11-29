#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re
import glob
import sqlite3

class DB(object):
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = sqlite3.connect(self.db_file, check_same_thread=False)
        self.db.text_factory = str
        self.cursor = self.db.cursor()
        self.create_table()

    def create_table(self):
        values = '''
           date varchar(20),
           time varchar(20),
           s_sitename varchar(20),
           s_ip varchar(20),
           cs_method varchar(20),
           cs_uri_stem varchar(255),
           cs_uri_query varchar(255),
           s_port varchar(11), 
           cs_username varchar(255),
           c_ip varchar(20),
           cs_User_Agent varchar(255),
           sc_status int(11),
           sc_substatus int(11),
           sc_win32_status int(11)
       '''
        query = 'CREATE TABLE IF NOT EXISTS info(%s)'% (values)
        self.cursor.execute(query)


    def free(self):
        self.cursor.close()

    def disconnect(self):
        self.db.close()


    def run(self):
        result=[]
        for logfile in glob.glob('log/*.log'):
            with open(logfile,"rb") as f:
                for line in f.readlines():
                    if line.startswith("#"):
                        continue
                    values = tuple(line.split())
                    result.append(values)
        print "Success found %s records"% len(result)                    
        sql='INSERT INTO info VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
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