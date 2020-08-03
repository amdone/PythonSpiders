import os
import json
import random
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.keys import Keys


# Setting
UseCookie = True
DownImg = True
DownText = False
DownVideo = False
twitter_url = ""


with open('./cookie.json', 'r', encoding='utf8')as fp:
    json_data = json.load(fp)
    print('这是文件中的json数据：', json_data)
    print('这是读取到文件数据的数据类型：', type(json_data))


# 调用函数scroll将左侧的滚动条滑动到底部
def scroll(chrome):
    js = 'window.scrollTo(0,8000)'
    chrome.execute_script(js)


# chrom设置
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')  # root用户不加这条会无法运行
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_window_size(650, 1080)
# driver.get("https://twitter.com/login")

print('=================Chrome Start================')

# 登录twitter
# driver.find_element_by_xpath("//a[@herf='/login']").click()
# input_user = driver.find_elements_by_xpath("//input[@name='session[username_or_email]']")
# input_user[0].send_keys("username")
#
# input_pswd = driver.find_elements_by_xpath("//input[@name='session[password]']")
# input_pswd[0].send_keys("password")
#
# login_button = driver.find_elements_by_xpath("//div[@data-testid='LoginForm_Login_Button']/div")
# login_button[0].click()
#
# print("Login successful!")

# 转入新页面
driver.get("https://twitter.com/")
driver.delete_all_cookies()
for cook in json_data:
    try:
        cook.pop('sameSite')
    except:
        pass
    driver.add_cookie(cook)
driver.get(twitter_url)
# click_button = driver.find_elements_by_xpath("//div[@data-testid='primaryColumn']//div[@role='button']/div")
# click_button[1].click()
sleep(5)
imgUrls = set()


def find_img_url(img_set):
    all_img = driver.find_elements_by_xpath("//img")
    for signal_img in all_img:
        try:
            signal_img_url = signal_img.get_attribute("src")
            surl = re.search("^https?:\/\/pbs\.twimg\.com\/media\/.*?(?:jpg|png)&name=?.*?$", signal_img_url)
            furl = surl.group(0).split('&')[0] + "&name=orig"
            img_set.add(furl)
            if DownImg:
                get_down_img(furl, "elisbai")
            # print(surl.group(0).split('&')[0] + "&name=orig")
        except:
            pass


def get_down_img(url, imgs_dirname):
    os.makedirs('./' + imgs_dirname + '/', exist_ok=True)
    try:
        kw = {
            'authority': 'pbs.twimg.com',
            'method': 'GET',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
        }
        r = requests.get(url, headers=kw)
        img_name = './' + imgs_dirname + '/' + url[-37:-22] + '.jpg'
        with open(img_name, 'wb') as fd:
            fd.write(r.content)
            fd.close()
    except:
        pass


def pulldownToButtom():
    section = driver.find_elements_by_xpath("//div[starts-with(@style,'position: relative;')]")
    body = driver.find_element_by_css_selector('body')
    judge = True
    while judge:
        target = section[0].get_attribute("style")
        temp = target
        for i in range(12):
            body.send_keys(Keys.PAGE_DOWN)
            temp = section[0].get_attribute("style")
            print(temp)
            print("scroll")
            find_img_url(imgUrls)
            sleep(2)
        if temp == target:
            judge = False
            print("bottom!")


def img_url_fomat(img_url):
    img_url = "aasd"


# pulldown()
pulldownToButtom()
print(len(imgUrls))
for iurl in imgUrls:
    print(iurl)
driver.get_screenshot_as_file("sc.png")
sleep(1)
# 打印当前页面URL
# now_url = driver.current_url
# print(now_url)

# 关闭所有窗口
driver.quit()
