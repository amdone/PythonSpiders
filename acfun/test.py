import json
import time
import sqlite3

import platform

print(platform.system())
import queue

dict = {'0022': {}}

print(True if '0122' in dict.keys() else False)


def bigThanDate(str_date1: str, str_date2: str):
    # '2020-10-31'
    return int(str_date1.replace('-', '')) > int(str_date2.replace('-', ''))


d1 = '2020-12-30'
d2 = '1999-11-01'
d3 = '2010-01-01'

path = 'f:\\PythonProjects'

print(path.replace('\\', '.'))


class Sql_Acer:
    '''
        @author:amdone
    '''

    def __init__(self, acerid):
        self.acerid = acerid
        self.conn = sqlite3.connect('./acfun_data.db')
        self.cur = self.conn.cursor()
        try:
            self.cur.execute('''create table acer(acno varchar(20) primary key, acerid integer,
                             acname varchar(20),  title varchar(40),
                             uploadtime integer)
                             ''')
        except:
            pass

    def insert_video(self, acno, name, title, uploadtime):
        sql_seq = '''insert into acer(acerid, acno, acname, title, uploadtime)values({},'{}','{}','{}',{})'''.format(
            self.acerid,
            acno, name,
            title,
            uploadtime)

        print(sql_seq)
        try:
            self.cur.execute(sql_seq)
        except:
            print("this video has been downloaded!!!")
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def delete_video(self, acno):
        sql_seq = 'delete from acer where acno = {}'.format(acno)
        self.cur.execute(sql_seq)
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def get_vlist(self):
        self.conn = sqlite3.connect('./acfun_data.db')
        self.cur = self.conn.cursor()
        sql_seq = 'select acno,title from acer where acerid={}'.format(self.acerid)
        self.cur.execute(sql_seq)
        self.conn.commit()
        result = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        return result

    def get_aclist(self):
        self.conn = sqlite3.connect('./acfun_data.db')
        self.cur = self.conn.cursor()
        sql_seq = 'select acno from acer where acerid={}'.format(self.acerid)
        self.cur.execute(sql_seq)
        # self.conn.commit()
        result = self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        return [i[0] for i in result]

    def get_newest_uploadTime(self):
        self.conn = sqlite3.connect('./acfun_data.db')
        self.cur = self.conn.cursor()
        sql_seq = 'select uploadtime from acer where acerid={} order by uploadtime desc '.format(self.acerid)
        self.cur.execute(sql_seq)
        # self.conn.commit()
        result = self.cur.fetchone()
        if result is None:
            return 1000
        self.cur.close()
        self.conn.close()
        return result[0]


if __name__ == '__main__':
    # Sql_Acer(1001).create_table()
    # Sql_Acer(1001).get_vlist()
    # Sql_Acer(3366).insert_video('ac100699', '魔术师张三', '今天来变个魔术', 1602042533)
    res = Sql_Acer(33696).get_newest_uploadTime()
    print(res)
    print(time.time())
    print(time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(1602042533)))
