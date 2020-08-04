## 下载up主的所有视频（利用annie)

 确保正确安装了annie以及ffmpeg
 annie : https://github.com/iawia002/annie
 annie用来下载视频，并依赖ffmpeg用来合并视频
 然后在bi.py中配置以下信息
 
 启动时输入参数：
 比如下载“敖厂长”的所有视频到/home/bilibili中：
 '''
 python3 bi.py 122879 /home/bilibili
 '''
space_num = None  # 进入up主的主页，在浏览器的地址栏就可以找到空间号
down_dir = None  # 下载到哪个文件夹内
default_down_dir = "/home/myod/bili/UP主"
cookie_path = "/home/configs/bilibilicookie.txt"  # 利用cookie下载最高画质视频
cookie_path = "" #没有大会员就不填
