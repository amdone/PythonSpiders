import re
import os
import sys
import time
import json
import requests

ac_no = ''
acer_no = ''
acer_name = ''
down_dir = ''
default_down_dir = "/home/share"

# configs
DownVideo = False
IsAcno = False

try:
    firstArgeement = sys.argv[1]
    down_dir = sys.argv[2]
except:
    pass

# if firstArgeement:
#     pass
# else:
#     print("must input ac_no or profile_no")
#     exit()
# if firstArgeement.startswith("ac"):
#     IsAcno = True
#     ac_no = firstArgeement
# else:
#     IsAcno = False
#     acer_no = firstArgeement
# if down_dir:
#     if os.path.exists(down_dir):s
#         print("down path has already existed!But that is ok!")
#         pass
#     else:
#         os.mkdir(down_dir)
# else:
#     down_dir = default_down_dir
#     if os.path.exists(down_dir):
#         print("down path has already existed!But that is ok!")
#         pass
#     else:
#         os.mkdir(down_dir)


def requests_get(ac_url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 "
                      "Safari/537.1"
    }
    r = requests.get(ac_url, headers=headers).text
    # print(r)
    if "出错啦！" in r:
        print("并没有找到你想要的信息！")
        return 0
    a = get_video_informations(r)
    return a


def get_video_informations(r):
    informations = []
    filename = ''
    url1 = ''
    p1 = ''
    p2 = ''
    p3 = ''
    p4 = ''
    p5 = ''
    p6 = ''
    p7 = ''
    p8 = ''
    urls = re.findall("[a-zA-z]+://[^\s]*", r)
    for url in urls:
        if "tx" in url:
            informations = url.split("{")
        for information in informations:
            if '2160p' in information:
                p1 = re.findall("[a-zA-z]+://[^\s]*", information)
                p1 = "2160p地址:" + p1[0][0:p1[0].index("\\")]
                url1 = p1[8:]
                print(url1)
            elif "1080p60" in information:
                p2 = re.findall("[a-zA-z]+://[^\s]*", information)
                p2 = "1080p60地址:" + p2[0][0:p2[0].index("\\")]
            elif "720p60" in information:
                p3 = re.findall("[a-zA-z]+://[^\s]*", information)
                p3 = "720p60地址:" + p3[0][0:p3[0].index("\\")]
            elif '1080p+' in information:
                p4 = re.findall("[a-zA-z]+://[^\s]*", information)
                p4 = "1080p+:" + p4[0][0:p4[0].index("\\")]
            elif '1080p' in information:
                p5 = re.findall("[a-zA-z]+://[^\s]*", information)
                p5 = "1080p地址:" + p5[0][0:p5[0].index("\\")]
            elif '720p' in information:
                p6 = re.findall("[a-zA-z]+://[^\s]*", information)
                p6 = "超清地址:" + p6[0][0:p6[0].index("\\")]
            elif "540p" in information:
                p7 = re.findall("[a-zA-z]+://[^\s]*", information)
                p7 = "高清地址:" + p7[0][0:p7[0].index("\\")]
            elif "360p" in information:
                p8 = re.findall("[a-zA-z]+://[^\s]*", information)
                p8 = "标清地址:" + p8[0][0:p8[0].index("\\")]

            elif "title" in information:
                index = information.index("fileName")
                filename = information[index + 11:information.index("\",\"id\"", index)]
    
    return p1, p2, p3, p4, p5, p6, p7, p8, filename, url1


def get_best_video(video_list):
    pass


def get_profile(acer_no):
    url_head = "https://api-new.app.acfun.cn/rest/app/feed/profile"
    params_data = {'pcursor': '0',
                   'userId': str(acer_no),
                   'count': '1'
                   }
    data = json.loads(requests.get(concaturl(url_head, params_data)).content)
    try:
        acer_name = data['feedList'][0]['user']['userName']
        down_dir = default_down_dir + "/" + acer_name
    except:
        print("can not get the name of acer!")
        down_dir = default_down_dir + "/acer_video"
    print("Acer is " + data['feedList'][0]['user']['userName'])


def down_m3u8(ipt2):
    m3u8_url = ''
    if ipt2 == '1':
        m3u8_url = a[0][8:]
    elif ipt2 == '2':
        m3u8_url = a[1][11:]
    elif ipt2 == '3':
        m3u8_url = a[2][9:]
    elif ipt2 == '4':
        m3u8_url = a[3][8:]
    else:
        print("输入错误！")
        return 0
    cmd = '/home/tools/m3u8-linux-amd64 -u=' + m3u8_url
    cmd2 = 'ffmpeg -i ' + m3u8_url + ' -vcodec copy -acodec copy -absf aac_adtstoasc output.mp4'
    os.system(cmd)
    # os.system('mv /movie/output.mp4 /home/down/123.mp4')

    return 1


def download_m3u8(ipt2):
    path = '/home/down'
    print("正在下载m3u8")
    download = ""
    if ipt2 == '1':
        download = a[0][8:]
    elif ipt2 == '2':
        download = a[1][5:]
    elif ipt2 == '3':
        download = a[2][5:]
    elif ipt2 == '4':
        download = a[3][5:]
    else:
        print("输入错误！")
        return 0
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 "
                      "Safari/537.1"
    }
    r = requests.get(download, headers=headers, stream=True).text
    with open(path + "/2.txt", "w+") as f:
        f.write(r)
    f.close()
    print("完成")
    return 1


def download_ts():
    path = '/home/down'
    with open(path + "/2.txt", "r+") as f:
        t = f.readlines()
    f.close()
    print("开始下载---")
    if not os.path.exists(path + "/vedio"):
        os.mkdir(path + "/vedio")
    l = 0
    for i in t:
        if i[0] != "#" and len(i) > 8:
            s1 = i.split("?")
            s2 = s1[1].split("&")
            s3 = s2[0].split("=")
            s4 = s2[1].split("=")
            params = {
                "pkey": s3[1],
                "safety_id": s4[1][:-1]
            }
            download_url = "https://tx-safety-video.acfun.cn/mediacloud/acfun/acfun_video/segment/" + s1[0]
            # print(download_url)
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 "
                              "Safari/537.1"
            }
            r = requests.get(download_url, headers=headers, params=params, stream=True)
            # print(r.url)
            with open(path + "/vedio/" + str(l) + ".ts", "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            f.close()
            print("正在下载{0}.ts".format(l))
            l += 1

            time.sleep(1)
    print("下载完成---")


def involve_ts():
    path = '/home/down'
    print("合并视频")
    ls = os.listdir(path + "/vedio/")
    print(len(ls))
    contect = ""
    for i in range(len(ls)):
        contect += path + "/vedio/" + str(i) + ".ts"
        if i != len(ls) - 1:
            contect += "|"
    print(contect)
    cmd = "ffmpeg -i concat:\"" + contect + "\" -acodec copy -vcodec copy -vbsf h264_mp4toannexb " + path + "/vedio/out.mp4"
    os.system(cmd)
    print("完成")


def concaturl(head, params):
    url = '?'
    for k in params.keys():
        url = url + k + '=' + params[k] + '&'
    return head + url[:-1]


def get_vlist(space_num):
    vlist = {}
    url_head = "https://api-new.app.acfun.cn/rest/app/user/resource/query"
    params_data = {'count': '999',
                   'authorId': str(space_num),
                   'resourceType': '2',
                   'sortType': '3'}
    data = json.loads(requests.get(concaturl(url_head, params_data)).content)
    for v in data['feed']:
        vlist[v['dougaId']] = v['title']
        # print(v['dougaId'])
        # print(v['title'])
        # print(v['description'])
        # print(v['coverUrl'])
        # print(v['uplosdTime'])
        # print()
    print("Find " + str(len(vlist)) + " videos\n")
    # for v in vlist:
    #     print(v)
    return vlist

def test():
    mkey = "AAHewK3eIAAyMTkyNDkwNTEAAhAAMEP1uwQYjimAYAAAAJQyKyucAT3ZY_RUsa0tV9LBmZYB7YPwVtVFrJ-P3yN8S_rt8klM_WBlObw8GXl5YPopk5dszsb6FTS2j7mzSa5_0TtG2nQ63LaPVDPvKbTKW6TYzG_Urny6kCFH8VQTcw%3D%3D"
    requestUrl = "https://api-new.app.acfun.cn/rest/app/play/playInfo/cast"
    params_data = {'videoId': '14289551',
                   'resourceId': '17920505',
                   'resourceType': '2',
                   'mkey': mkey}

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 "
                      "Safari/537.1"}
    data = json.loads(requests.get(concaturl(requestUrl, params_data)).content)
    # data = json.loads(requests.get(fin_url).content)
    print(data)


if __name__ == "__main__":
    print("acfun.py is starting...\n")
    if IsAcno:
        ac_url = "https://www.acfun.cn/player/" + ac_no
        video = requests_get(ac_url)
        for v in video:
            print(v)

    else:
        print("Got A Acer!!!")
        get_profile(4042290)
        vlist = get_vlist(4042290)
        for v in vlist:
            print('ac{}'.format(v))
            # ac_url = "https://www.acfun.cn/player/ac" + v
            # video = requests_get(ac_url)
            # print(video[0])

    while True:
        print("|---------------------本程序只供学习，不能用作商业---------------------|")
        ipt = input("请输入你要下载的视频ac:(例ac14856217)")
        ac_url = "https://www.acfun.cn/player/" + ipt
        ac_uel_test = "https://www.acfun.cn/player/ac17694381"
        a = requests_get(ac_url)
        if a == 0:
            continue
        print("当前视频title：" + a[8])
        print(a[0] + "\n")
        print(a[1] + "\n")
        print(a[2] + "\n")
        print(a[3] + "\n")
        print(a[4] + "\n")
        print(a[5] + "\n")
        print(a[6] + "\n")
        print(a[7] + "\n")
        while True:
            print("Which do you want to download?")
            print("1：2160P")
            print("2：1080p60")
            print("3：720p60")
            print("4：1080p+")
            ipt2 = input()
            a = down_m3u8(ipt2)
            # a = download_m3u8(ipt2)
            if a == 0:
                continue
            if a == 1:
                # download_ts()
                # involve_ts()
                print("ok!")
            break
        break
        print("|---------------------本程序只供学习，不能用作商业---------------------|")
