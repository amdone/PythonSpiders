import os
import sqlite3


class Sql_Bili:
    '''
        @author:amdone
    '''

    def __init__(self, acerid):
        if not os.path.isfile('./bili_data.db'):
            self.conn = sqlite3.connect('./bili_data.db')
            self.cur = self.conn.cursor()
            self.cur.execute('''create table bili(aid integer primary key, created integer,
                             title text,  description text,
                             pic varchar(100), mid integer)
                             ''')
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        self.acerid = acerid
        self.conn = sqlite3.connect('./bili_data.db')
        self.cur = self.conn.cursor()
        # try:
        #     self.cur.execute('''create table acer(acno varchar(20) primary key, acerid integer,
        #                      acname varchar(20),  title varchar(40),
        #                      uploadtime integer)
        #                      ''')
        # except:
        #     pass

    def insert_video(self, aid, created, title,  description, pic, mid):
        sql_seq = '''insert into bili(aid, created, title,  description, pic, mid)
                        values({},{},'{}','{}','{}',{})
                        '''.format(aid, created, title,  description, pic, mid)
        # print(sql_seq)
        try:
            self.cur.execute(sql_seq)
        except:
            print("this video has been downloaded!!!")
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def insert_video_from_tuple(self, abc: tuple):
        c = ','.join([str(i) if type(i) == type(1) else str("'{}'".format(i)) for i in abc])
        sql_seq = '''insert into bili(aid, created, title,  description, pic, mid)
                        values({})
                        '''.format(c)
        # print(sql_seq)
        # cur.execute(sql_seq)
        try:
            self.cur.execute(sql_seq)
        except Exception as e:
            # print("Warning: This tweet has been recorded!!!")
            print(e)
            pass
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def insert_video_from_set(self, ss: list):
        for v in ss:
            c = ','.join([str(i) if type(i) == type(1) else str("'{}'".format(i)) for i in v])
            # c = c.replace("'","''")
            sql_seq = '''insert into bili(aid, created, title,  description, pic, mid)
                                values({})
                                '''.format(c)
            try:
                self.cur.execute(sql_seq)
            except Exception as e:
                # print("Warning: This tweet has been recorded!!!")
                print(e)
                print(sql_seq)
                pass
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
        return [fuck[0] for fuck in result]

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