import os
import re
import sys
import json
import queue
import getopt
import shelve
import shutil
import sqlite3
import requests
import platform

import datetime
from tqdm import tqdm
from contextlib import closing
from concurrent.futures import ThreadPoolExecutor

redstr = "\033[1;31;40m{}\033[0m"
CloudName = ''
path = ''
default_down_dir = '/home/share/abd/'
url_syntax = 'https://www.acfun.cn/v/{}'
IsAcno = True
ac_no = ''
acer_no = ''
m3u8_full_url = ''
title = ''
ac_data = {}
# config_path = '/home/configs/acfun/acfun_data.json'
db_path = '/home/configs/acfun/acfun_data'
db_dir = '/home/configs/acfun'
wdb_path = './ac_data'
wdb_dir = './ac_data'

opts, args = getopt.getopt(sys.argv[2:], 'c:g:d:', ['up=', 'gd=', 'od=', 'gd', 'od', 'all'])

for o, a in opts:
    if o == '-c':
        CloudName = a
    if o == '-d':
        CloudName = 'od'
    if o == '-g':
        CloudName = 'gd'

if platform.system() == 'Windows':
    db_path = wdb_path
    db_dir = wdb_dir
    pass
elif platform.system() == 'Linux':
    pass
else:
    print('Your system is not supported!!!')
    sys.exit(0)

try:
    path = sys.argv[2]
    if not path.endswith('/'):
        path += '/'
except:
    path = './'
    pass



try:
    firstArgeement = sys.argv[1]
except:
    print("Please give me a number!!!!!")
    sys.exit(0)

if firstArgeement.startswith("ac") or firstArgeement.startswith("AC"):
    IsAcno = True
    ac_no = firstArgeement.lower()
else:
    IsAcno = False
    acer_no = firstArgeement

# get configs from config.ini

# read configuration from local database
if not os.path.isdir(db_dir):
    os.makedirs(db_dir)
if not os.path.isfile(db_path + '.dat'):
    with closing(shelve.open(db_path, 'c')) as sf:
        sf['ac_data'] = ac_data
else:
    with closing(shelve.open(db_path, 'r')) as sf:
        ac_data = sf['ac_data']


def concaturl(head, params):
    '''
        @author:amdone
    '''
    url = '?'
    for k in params.keys():
        url = url + k + '=' + params[k] + '&'
    return head + url[:-1]


def bigThanDate(str_date1: str, str_date2: str):
    if '前' in str_date1:
        return True
    if '前' in str_date2:
        return False
    return int(str_date1.replace('-', '')) > int(str_date2.replace('-', ''))


headers = {
    'referer': 'https://www.acfun.cn/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83'
}


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


class user():
    def __init__(self, space_no):
        self.space_no = space_no

    def get_vlist(self):
        vlist = {}
        aclist = []
        down_list = []
        acer_name = ''

        url_head = "https://api-new.app.acfun.cn/rest/app/user/resource/query"
        params_data = {'count': '999',
                       'authorId': str(self.space_no),
                       'resourceType': '2',
                       'sortType': '3'}
        data = json.loads(requests.get(concaturl(url_head, params_data)).content)
        date_record = '1990-01-01'
        # print(data)

        aclist = Sql_Acer(self.space_no).get_aclist()

        for v in data['feed']:
            if acer_name == '':
                acer_name = v['user']['name']
            if ('ac' + v['dougaId']) in aclist:
                print(redstr.format('ac' + v['dougaId'] + ' already downloaded!'))
                continue
            part_list = v['videoList']
            Sql_Acer(self.space_no).insert_video('ac' + v['dougaId'], acer_name, v['title'], part_list[0]['uploadTime'])
            down_list.append('ac' + v['dougaId'])
            #vlist[v['dougaId']] = v['title']
            # uploadTime = v['videoList']['uploadTime']
            newest_uploadTime = Sql_Acer(self.space_no).get_newest_uploadTime()
            if int(part_list[0]['uploadTime']) > newest_uploadTime:
                date_record = v['createTime']
            if len(part_list) > 1:
                for i in range(len(part_list) - 1):
                    ac_no_p = 'ac' + v['dougaId'] + '_' + str(i + 2)
                    Sql_Acer(self.space_no).insert_video(ac_no_p, acer_name, v['title'],
                                                         part_list[0]['uploadTime'])
                    down_list.append(ac_no_p)
            # print(v['dougaId'])
            # print(v['title'])
            # print(v['description'])
            # print(v['coverUrl'])
            # print(v['createTime'])
            # print(v['user']['name'])
            # print()
        return Sql_Acer(self.space_no).get_vlist(), down_list, acer_name, date_record

    def get_profile(acer_no):
        url_head = "https://api-new.app.acfun.cn/rest/app/feed/profile"
        params_data = {'pcursor': '0',
                       'userId': str(acer_no),
                       'count': '1'
                       }
        data = json.loads(requests.get(concaturl(url_head, params_data)).content)
        print(data)
        try:
            acer_name = data['feedList'][0]['user']['userName']
            down_dir = default_down_dir + "/" + acer_name
        except:
            print("can not get the name of acer!")
            down_dir = default_down_dir + "/acer_video"
        print("Acer is " + data['feedList'][0]['user']['userName'])
        return acer_name


class m3u8_url():
    def __init__(self, f_url):
        self.url = f_url

    def get_m3u8(self):
        global flag, qua, rel_path
        html = requests.get(self.url, headers=headers).text
        first_json = json.loads(re.findall('window.pageInfo = window.videoInfo = (.*?)};', html)[0] + '}', strict=False)
        name = first_json['title'].strip().replace("|", '')
        video_info = json.loads(first_json['currentVideoInfo']['ksPlayJson'], strict=False)['adaptationSet'][0][
            'representation']
        Label = {}
        num = 0
        for quality in video_info:  # 清晰度
            num += 1
            Label[num] = quality['qualityLabel']
        print(Label)
        # choice = int(input("请选择清晰度: "))
        # print((name,video_info[choice - 1]['url'],path))
        # Download(name + '_{}'.format(Label[1]), video_info[0]['url'], path).download_with_m3dl()
        # return Download(name + '_{}'.format(Label[1]), video_info[0]['url'], path).get_info()
        if '_' in self.url:
            name = name + '_P' + self.url[-1:]
            # print(name)
        return name, video_info[0]['url'], path
        # Download(name + '[{}]'.format(Label[choice]), video_info[choice - 1]['url'], path).start_download()


class ThreadPoolExecutorWithQueueSizeLimit(ThreadPoolExecutor):
    """
    实现多线程有界队列
    队列数为线程数的2倍
    """

    def __init__(self, max_workers=None, *args, **kwargs):
        super().__init__(max_workers, *args, **kwargs)
        self._work_queue = queue.Queue(max_workers * 2)


def make_sum():
    ts_num = 0
    while True:
        yield ts_num
        ts_num += 1


class M3u8Download:
    """
    :param url: 完整的m3u8文件链接 如"https://www.bilibili.com/example/index.m3u8"
    :param name: 保存m3u8的文件名 如"index"
    :param max_workers: 多线程最大线程数
    :param num_retries: 重试次数
    """

    def __init__(self, url, name, max_workers=64, num_retries=5):
        self.url = url
        self.name = name
        self.max_workers = max_workers
        self.num_retries = num_retries
        self.front_url = None
        self.ts_url_list = []
        self.success_sum = 0
        self.ts_sum = 0
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

        requests.packages.urllib3.disable_warnings()

        self.get_m3u8_info(self.url, self.num_retries)
        with ThreadPoolExecutorWithQueueSizeLimit(self.max_workers) as pool:
            for ts_url, auto_id in zip(self.ts_url_list, range(0, len(self.ts_url_list))):
                pool.submit(self.download_ts, ts_url, auto_id, self.num_retries)
        if self.success_sum == self.ts_sum:
            self.output_mp4()

    def get_m3u8_info(self, m3u8_url, num_retries):
        """
        获取m3u8信息
        """
        try:
            res = requests.get(m3u8_url, timeout=(3, 30), verify=False, headers=self.headers)
            self.front_url = res.url.split(res.request.path_url)[0]
            if "EXT-X-STREAM-INF" in res.text:  # 判定为顶级M3U8文件
                for line in res.text.split('\n'):
                    if "#" in line:
                        continue
                    elif re.search(r'^http', line) is not None:
                        self.url = line
                    elif re.search(r'^/', line) is not None:
                        self.url = self.front_url + line
                    else:
                        self.url = self.url.rsplit("/", 1)[0] + '/' + line
                self.get_m3u8_info(self.url, self.num_retries)
            else:
                m3u8_text_str = res.text
                self.get_ts_url(m3u8_text_str)
        except Exception as e:
            print(e)
            if num_retries > 0:
                self.get_m3u8_info(m3u8_url, num_retries - 1)

    def get_ts_url(self, m3u8_text_str):
        """
        获取每一个ts文件的链接
        """
        if not os.path.exists(f"./{self.name}"):
            os.mkdir(f"./{self.name}")
        new_m3u8_str = ''
        ts = make_sum()
        for line in m3u8_text_str.split('\n'):
            if "#" in line:
                if "EXT-X-KEY" in line and "URI=" in line:
                    key = self.download_key(line, 5)
                    if key:
                        new_m3u8_str += f'{key}\n'
                        continue
                new_m3u8_str += f'{line}\n'
                if "EXT-X-ENDLIST" in line:
                    break
            elif re.search(r'^http', line) is not None:
                new_m3u8_str += f"./{self.name}/{next(ts)}\n"
                self.ts_url_list.append(line)
            elif re.search(r'^/', line) is not None:
                new_m3u8_str += f"./{self.name}/{next(ts)}\n"
                self.ts_url_list.append(self.front_url + line)
            else:
                new_m3u8_str += f"./{self.name}/{next(ts)}\n"
                self.ts_url_list.append(self.url.rsplit("/", 1)[0] + '/' + line)
        self.ts_sum = next(ts)
        with open(f"./{self.name}.m3u8", "w") as f:
            f.write(new_m3u8_str)

    def download_ts(self, ts_url, save_ts_name, num_retries):
        """
        下载 .ts 文件
        """
        ts_url = ts_url.split('\n')[0]
        try:
            if not os.path.exists(f"./{self.name}/{save_ts_name}"):
                res = requests.get(ts_url, stream=True, timeout=(5, 60), verify=False, headers=self.headers)
                if res.status_code == 200:
                    with open(f"./{self.name}/{save_ts_name}", "wb") as ts:
                        for chunk in res.iter_content(chunk_size=1024):
                            if chunk:
                                ts.write(chunk)
                    self.success_sum += 1
                    print(f"\rDownloading {self.name}：{self.success_sum}/{self.ts_sum}\t", end='')
                else:
                    self.download_ts(ts_url, save_ts_name, num_retries - 1)
                res.close()
            else:
                self.success_sum += 1
        except Exception:
            if os.path.exists(f"./{self.name}/{save_ts_name}"):
                os.remove(f"./{self.name}/{save_ts_name}")
            if num_retries > 0:
                self.download_ts(ts_url, save_ts_name, num_retries - 1)

    def download_key(self, key_line, num_retries):
        """
        下载key文件
        """
        mid_part = re.search(r"URI=[\'|\"].*?[\'|\"]", key_line).group()
        may_key_url = mid_part[5:-1]
        if re.search(r'^http', may_key_url) is not None:
            true_key_url = may_key_url
        elif re.search(r'^/', may_key_url) is not None:
            true_key_url = self.front_url + may_key_url
        else:
            true_key_url = self.url.rsplit("/", 1)[0] + '/' + may_key_url
        try:
            res = requests.get(true_key_url, timeout=(5, 60), verify=False, headers=self.headers)
            with open(f"./{self.name}/key", 'wb') as f:
                f.write(res.content)
            res.close()
            return f'{key_line.split(mid_part)[0]}URI="./{self.name}/key"{key_line.split(mid_part)[-1]}'
        except Exception as e:
            print(e)
            if os.path.exists(f"./{self.name}/key"):
                os.remove(f"./{self.name}/key")
            print("加密视频,无法加载key,揭秘失败")
            if num_retries > 0:
                self.download_key(key_line, num_retries - 1)

    def output_mp4(self):
        """
        合并.ts文件，输出mp4格式视频，需要ffmpeg
        """
        cmd = f"ffmpeg -allowed_extensions ALL -i '{self.name}.m3u8' -acodec copy -vcodec copy -f mp4 '{path + self.name}'.mp4"
        os.system(cmd)
        os.system(f'rm -rf ./"{self.name}" ./"{self.name}.m3u8"')
        print(f"Download successfully --> '{self.name}'")


if __name__ == '__main__':
    print(redstr.format('Download ... ' + ac_no))
    # vlist = user(acer_no).get_vlist()
    if IsAcno:
        # m3u8_url(url_syntax.format(ac_no)).get_m3u8()
        fin_name, fin_url, fin_path = m3u8_url(url_syntax.format(ac_no)).get_m3u8()
        M3u8Download(fin_url, fin_name)
        if not path == '':
            shutil.move('{}.mp4'.format(fin_name), fin_path + '{}.mp4'.format(fin_name))
    else:
        # acer_name = user(acer_no).get_profile()
        vlist, down_videos_list, acer, newest_date = user(acer_no).get_vlist()
        print(acer + '  ' + newest_date)
        try:
            if not os.path.isdir(path + acer):
                os.makedirs(path + acer)
        except:
            pass
        else:
            path += acer + '/'
        for i, v in enumerate(down_videos_list):
            print(str(i) + ' ---> ' + v)
            fin_name, fin_url, fin_path = m3u8_url(url_syntax.format(v)).get_m3u8()
            # # print((fin_url, fin_name))
            M3u8Download(fin_url, fin_name)
            # if not path == '':
            #     shutil.move('{}.mp4'.format(fin_name), fin_path + '{}.mp4'.format(fin_name))
            if not CloudName == '':
                if acer == '':
                    acer = 'unknown'
                cmd = 'rclone copy {0}"{1}" {2}:/uploads/acfun/{3}/ -P'.format(path, fin_name + '.mp4', CloudName, acer)
                print(cmd)
                os.system(cmd)
                os.remove(path + fin_name + '.mp4')

    with closing(shelve.open(db_path, 'c')) as sf:
        sf['ac_data'] = ac_data

