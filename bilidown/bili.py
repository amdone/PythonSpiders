import getopt
import os
import sys
import time
import json
import requests
from Sql_Bili import Sql_Bili

path = './'
cookie_path = './cookie.txt'

opts, args = getopt.getopt(sys.argv[2:], 'u:g:d:', ['up=', 'gd=', 'od=', 'gd', 'od', 'all'])

for o, a in opts:
    if o == '-u':
        CloudName = a
    if o == '-d':
        CloudName = 'od'
    if o == '-g':
        CloudName = 'gd'

print(CloudName)


def ft(longlonglongsequence: str):
    return longlonglongsequence.replace('\n', '</br>').replace("'", "''")


def down_img(url, out_path):
    kw = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    if url == '':
        return
    r = requests.get('http://' + url, headers=kw)
    with open(out_path, 'wb') as fd:
        fd.write(r.content)


class user:
    def __init__(self, space_no):
        self.space_no = space_no

    def get_vlist(self):
        av_list = []
        video_list = []  # aid, created, title,  description, pic, mid, author
        pn = 1
        video_list_request_url = "http://api.bilibili.com/x/space/arc/search"
        stop = False
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) "
                          "Chrome/22.0.1207.1 "
                          "Safari/537.1"}
        while True:
            params_data = {'mid': self.space_no,
                           'pn': pn,
                           'ps': 100}  # 将携带的参数传给params
            data = json.loads(requests.get(video_list_request_url, params=params_data, headers=headers).content)
            if data['code'] != 0:
                break
            vlist = data['data']['list']['vlist']
            if len(vlist) == 0:
                break
            for i, v in enumerate(vlist):
                av_list.append(v['aid'])
                video_list.append(
                    (v['aid'], v['created'], ft(v['title']), ft(v['description']), v['pic'][2:], v['mid'], v['author']))
            pn += 1
        return av_list, video_list


class Down:
    def __init__(self, space_no):
        self.space_no = space_no
        self.exits_videos = Sql_Bili(space_no).get_vlist()

    def down_all_video(self, av_list, exits_avlist, dir_path='./'):
        author = Sql_Bili(self.space_no).get_author()
        try:
            if not os.path.isdir(dir_path + author):
                os.makedirs(dir_path + author)
            if not os.path.isdir(dir_path + author + '/cover'):
                os.makedirs(dir_path + author + '/cover')
        except:
            pass
        else:
            # dir_path += author + '/'
            pass
        count = 1
        if cookie_path is None:
            annie_cmd = "annie -o " + dir_path + author + "/ -p "
        else:
            annie_cmd = "annie -o " + dir_path + author + "/ -c " + cookie_path + " -p {}"
        for av in av_list:
            if av in exits_avlist:
                continue
            str_av = 'av' + str(av)
            print("[" + str(count) + "]" + str_av + " start...")
            os.system(annie_cmd.format(str_av))
            print("[" + str(count) + "]" + str_av + " done!")
            count += 1
            # Sql_Bili(self.space_no).insert_video()
            cover_url, title = Sql_Bili(self.space_no).get_cover(av)
            img_type = cover_url.split('.')[-1]
            down_img(cover_url, '{}/{}/cover/{}_av{}.{}'.format(dir_path, author, title, av, img_type))
            # down_img(cover_url, dir_path + "/" + author + "/cover/" + title + str(av) + '.' + img_type)
            if not CloudName == '':
                cmd = "rclone copy '{0}{1}/' {2}:/uploads/bilibili/{1}/ -P".format(dir_path, author, CloudName)
                print(cmd)
                os.system(cmd)
                cmd = "rm -rf {0}{1}/*.mp4 {0}{1}/cover/*".format(dir_path, author)
                os.system(cmd)
        if not CloudName == '':
            cmd = "rm -rf {}".format(dir_path + author)
            os.system(cmd)

    def down_cover(self, url, out_path):
        kw = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
        }
        if url == '':
            return
        r = requests.get(url, headers=kw)
        with open(out_path, 'wb') as fd:
            fd.write(r.content)


if __name__ == '__main__':
    space_id = sys.argv[1]
    exits_vlist = Sql_Bili(space_id).get_vlist()
    vl, vs = user(space_id).get_vlist()
    print('Find {} videos！'.format(len(vl)))
    # [print(i) for i in vl]
    Sql_Bili(1).insert_video_from_list(vs)
    print(Sql_Bili(space_id).get_author())
    Down(space_id).down_all_video(vl, exits_vlist)
