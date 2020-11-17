import os
import sqlite3


class Sql_Tweet:
    '''
        @author:amdone
        UserName,Handle,Timestamp,Text,Emojis,Comments,Likes,Retweets,imgs,video
    '''

    def __init__(self, twer_id):
        if not os.path.isfile('./tweets.db'):
            self.conn = sqlite3.connect('./tweets.db')
            self.cur = self.conn.cursor()
            self.cur.execute('''create table tweets(Fuk_id varchar(50) primary key, Twer_id varchar(40), Username varchar(40),
                             CreateTime varchar(25), Text varchar(500), Comments varchar(10), Likes varchar(10), Retweets varchar(10),
                             Imgs varchar(200), Video varchar(50))
                             ''')
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        self.twer_id = twer_id
        self.conn = sqlite3.connect('./tweets.db')
        self.cur = self.conn.cursor()
        # try:
        #     self.cur.execute('''create table acer(acno varchar(20) primary key, acerid integer,
        #                      acname varchar(20),  title varchar(40),
        #                      uploadtime integer)
        #                      ''')
        # except:
        #     pass

    def insert_tweet(self, fuk_id, Handle, UserName, Timestamp, Text, Comments, Likes, Retweets, Imgs, Video):
        sql_seq = '''insert into tweets(Fuk_id, Twer_id, Username, CreateTime, Text, Comments, Likes, Retweets, Imgs, Video)
                        values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                        '''.format(fuk_id, Handle, UserName, Timestamp, Text, Comments, Likes, Retweets, Imgs, Video)

        # print(sql_seq)
        # cur.execute(sql_seq)
        try:
            self.cur.execute(sql_seq)
        except Exception as e:
            # print("Warning: This tweet has been recorded!!!")
            # print(e)
            pass
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def insert_tweet_from_tuple(self, *args):
        a = args[0]
        b = "','".join(a)
        c = "('{}')".format(b)
        sql_seq = '''insert into tweets(Fuk_id, Twer_id, Username, CreateTime, Text, Comments, Likes, Retweets, Imgs, Video)
                        values{}
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

    def delete_tweet(self, Handle, ID):
        sql_seq = '''delete from tweets where Twer_id = '{}' and ID = '{}' '''.format(
            Handle, ID)

        # print(sql_seq)
        try:
            self.cur.execute(sql_seq)
        except:
            print("Warning: Something is wrong!!!")
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def get_newest_timestamp(self, Handle):
        sql_seq = '''select Fuk_id from tweets where Twer_id='{}' order by Fuk_id desc '''.format(
            Handle)

        # print(sql_seq)
        try:
            self.cur.execute(sql_seq)
        except:
            print("Warning: Something is wrong!!!")
        result = self.cur.fetchone()
        self.conn.commit()
        self.cur.close()
        self.conn.close()

        if result is None:
            return 1000
        else:
            return result[0]
        
        
# if __name__ == '__main__':
#     tweet=('20201205132514332','abcd','dddd','2020-11-05T16:44:18.000Z','2','2', '214', '151', '' ,'asd')
#     Sql_Tweet('1100').insert_tweet_from_tuple(tweet)
#     a = Sql_Tweet('110').get_newest_timestamp('abcd')
#     print(a)