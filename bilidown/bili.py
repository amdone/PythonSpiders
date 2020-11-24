import os
import time
import json
import requests
from Sql_Bili import Sql_Bili


def ft(longlonglongsequence:str):
    return longlonglongsequence.replace('\n','</br>').replace("'","''")


class user:
    def __init__(self, space_no):
        self.space_no = space_no
        def ft(longlonglongsequence:str):
            return longlonglongsequence.replace('\n','</br>').replace("'","''")

    def get_vlist(self):
        av_list = []
        video_set = [] # aid, created, title,  description, pic
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
                video_set.append((v['aid'], v['created'], ft(v['title']), ft(v['description']), v['pic'][2:], v['mid']))
            pn += 1
        return av_list, video_set


if __name__ == '__main__':
    vl, vs = user(8366990).get_vlist()
    vl.sort(reverse=True)
    [print(i) for i in vs]
    Sql_Bili(254).insert_video_from_set(vs)
    # [Sql_Bili(125).insert_video_from_tuple(i) for i in vs]
    print('{} 个视频！'.format(len(vs)))
