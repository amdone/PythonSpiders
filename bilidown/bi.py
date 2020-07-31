import requests
#from lxml import etree
import os
import json
#from bs4 import BeautifulSoup
from requests import exceptions
import re
import time


def download_page(url):
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    data = requests.get(url, headers=headers)
    return data


def get_video_page(space_num):
    base_url = "https://www.bilibili.com/av"
    url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&pagesize=99&tid=0&page=1&keyword=&order=pubdate".format(space_num)
    data = json.loads(download_page(url).content)['data']
    total = data['count']
    page_num = int(total/99) + 1
    video_list = data['vlist']
    video_url = []
    for video in video_list:
        video_url.append(base_url + str(video['aid']))
    for i in range(2, page_num+1):
        time.sleep(1)
        url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&pagesize=99&tid=0&page={}&keyword=&order=pubdate".format(space_num, i)
        data = json.loads(download_page(url).content)['data']
        video_list = data['vlist']
        for video in video_list:
            video_url.append(base_url + str(video['aid']))
    return video_url

def get_video_av_list(space_num):
    base_url = "https://www.bilibili.com/av"
    url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&pagesize=99&tid=0&page=1&keyword=&order=pubdate".format(space_num)
    data = json.loads(download_page(url).content)['data']
    total = data['count']
    page_num = int(total/99) + 1
    video_list = data['vlist']
    av_list = []
    for video in video_list:
        av_list.append("av" + str(video['aid']))
    for i in range(2, page_num+1):
        time.sleep(1)
        url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&pagesize=99&tid=0&page={}&keyword=&order=pubdate".format(space_num, i)
        data = json.loads(download_page(url).content)['data']
        video_list = data['vlist']
        for video in video_list:
            av_list.append("av" + str(video['aid']))
    return av_list

def annie_all_video(av_list):
    count = 1
    for av in av_list:
        print("[" + count + "]" + av + " start...")
        os.system("annie -c bilibilicookie.txt -p " + av)
        print("[" + count + "]" + av + " done!")
        count+=1

if __name__ == '__main__':
	avlist = get_video_av_list(2223018)
	print(len(avlist))
	print(avlist)
	#print("annie -c /home/configs/bilibilicookie.txt "+vlist[0])
	os.system("annie -v")
	os.system("annie -c bilibilicookie.txt -p "+avlist[0])
