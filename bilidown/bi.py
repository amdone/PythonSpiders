import os
import sys
import json
import time
import requests

# 确保正确安装了annie以及ffmpeg
# annie : https://github.com/iawia002/annie
# annie用来下载视频，并依赖ffmpeg用来合并视频
# 利用命令 python3 bi.py 123456 下载空间号为123456用户的所有视频
# 利用命令 python3 bi.py 123456 /home/bilibili 下载空间号为123456用户的所有视频到/home/bilibili文件夹下

# 然后配置以下信息
space_num = None  # 进入up主的主页，在浏览器的地址栏就可以找到空间号, 以up主“老番茄”为例
down_dir = None  # 下载到哪个文件夹内
default_down_dir = "/home/myod/bili/UP主"
cookie_path = "/home/configs/bilibilicookie.txt"  # 利用cookie下载最高画质视频
# cookie_path = "" #没有大会员就不填

try:
    space_num = sys.argv[1]
    down_dir = sys.argv[2]
except:
    pass

if space_num:
    pass
else:
    print("must input space_num")
    exit()
if down_dir:
    if os.path.exists(down_dir):
        print("down path has already existed!But that is ok!")
        pass
    else:
        os.mkdir(down_dir)
else:
    down_dir = default_down_dir
    if os.path.exists(down_dir):
        print("down path has already existed!But that is ok!")
        pass
    else:
        os.mkdir(down_dir)


def download_page(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 "
                      "Safari/537.1"}
    data = requests.get(url, headers=headers)
    return data


def get_name(arg_space_num):
    # space_url = "https://space.bilibili.com/" + str(space_num) + "/"
    url = "https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp".format(arg_space_num)
    # html_contect = download_page(space_url).content
    data = json.loads(download_page(url).content)['data']
    return data['name']


def get_video_page(arg_space_num):
    base_url = "https://www.bilibili.com/av"
    url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&pagesize=99&tid=0&page=1&keyword=&order=pubdate".format(
        arg_space_num)
    data = json.loads(download_page(url).content)['data']
    total = data['count']
    page_num = int(total / 99) + 1
    video_list = data['vlist']
    video_url = []
    for video in video_list:
        video_url.append(base_url + str(video['aid']))
    for i in range(2, page_num + 1):
        time.sleep(1)
        url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}" \
              "&pagesize=99&tid=0&page={}&keyword=&order=pubdate".format(arg_space_num, i)
        data = json.loads(download_page(url).content)['data']
        video_list = data['vlist']
        for video in video_list:
            video_url.append(base_url + str(video['aid']))
    return video_url


def get_video_av_list(arg_space_num):
    base_url = "https://www.bilibili.com/av"
    url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}" \
          "&pagesize=99&tid=0&page=1&keyword=&order=pubdate".format(arg_space_num)
    data = json.loads(download_page(url).content)['data']
    total = data['count']
    page_num = int(total / 99) + 1
    video_list = data['vlist']
    av_list = []
    for video in video_list:
        av_list.append("av" + str(video['aid']))
    for i in range(2, page_num + 1):
        time.sleep(1)
        url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}" \
              "&pagesize=99&tid=0&page={}&keyword=&order=pubdate".format(arg_space_num, i)
        data = json.loads(download_page(url).content)['data']
        video_list = data['vlist']
        for video in video_list:
            av_list.append("av" + str(video['aid']))
    return av_list


def annie_all_video(arg_up_name, av_list):
    count = 1
    if cookie_path is None:
        annie_cmd = "annie -o " + down_dir + "/" + arg_up_name + "/ -p "
    else:
        annie_cmd = "annie -o " + down_dir + "/" + arg_up_name + "/ -c " + cookie_path + " -p "
    for av in av_list:
        print("[" + str(count) + "]" + av + " start...")
        os.system(annie_cmd + av)
        print("[" + str(count) + "]" + av + " done!")
        count += 1


if __name__ == '__main__':
    up_name = get_name(space_num)
    print("UP: " + up_name)
    avlist = get_video_av_list(space_num)
    print("Find " + str(len(avlist)) + " videos")
    print("Download start...")
    if not os.path.isdir(down_dir + "/" + up_name):
        os.mkdir(down_dir + "/" + up_name)
    annie_all_video(up_name, avlist)
    print("All  done!")
