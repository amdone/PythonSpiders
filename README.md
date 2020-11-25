# PythonSpiders
some net-spider in python

## 半成品
## 主要运行环境为linux命令行界面
## one command then download all videos of video_uper
## 一键下载博主所有博文(包括视频，图片)
## 目前脚本文件名含有2的(acfun2.py)基本上可以用
## 主打一键下载所有博文而不是单条博文下载，利用cookie可以下载最高画质
## 利用rclone命令上传到网盘中

-------------------
开发中...

1. acfun
2. bilibili
3. jjgirls
4. twitter

-------------------
未开发...

5. instgram
6. artstation
7. pixiv
8. flicker
9. ...

### 详细说明

#### acfun2.py

类似命令:
```
python3 acfun2.py <uid> ./ -u <drivername>
```

uid就是up主的空间号，分享该up主主页的链接中就有

./ 下载到./目录下

```<drivername>``` 云盘的配置名

#### twitter2.py

```
python twitter2.py <id>
```

将```<id>```设置为要爬取的推主的id

然后运行即可

如果需要上传至云盘

运行： ```python twitter2.py <id> -u <drivername>```

#### jjgirls.py

给定一个英文名，然后下载她的所有图片


#### bili.py

```python bili.py <space_no>```


