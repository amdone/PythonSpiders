import os
import re
import csv
import sys
import json
import getopt
import sqlite3
import requests
from time import sleep
from Sql_Tweets import Sql_Tweet
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# create some value for easy use:
imgUrls = set()
imgsDict = {}
videoUrls = set()
twerID = ""
twerName = ""
twitter_url = "https://twitter.com"
# twitter_url = "https://twitter.com/"
twerDescription = ""
twerCreatedDate = ""
twerFans = ""
twerLocation = ""
timeSet = set()
imgcc = 0
CloudName = ""

try:
    twerID = sys.argv[1]
except:
    print("please give me a ID")
    sys.exit(0)

opts, args = getopt.getopt(sys.argv[2:], 'u:g:d:', ['up=', 'gd=', 'od=', 'gd', 'od', 'all'])

for o, a in opts:
    if o == '-u':
        CloudName = a
    if o == '-d':
        CloudName = 'od'
    if o == '-g':
        CloudName = 'gd'

# chrome start setting
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')  # root用户不加这条会无法运行
chrome_options.add_argument('--disable-dev-shm-usage')
prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
            }
        }
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_window_size(480, 1080)

# get cookie,twerlist form files
try:
    with open('cookie.json', 'r', encoding='utf8')as fp:
        cookieData = json.load(fp)
except:
    print("Warning: cannot load cookie file...")


def img_url_fomat(img_url):
    surl = re.search("^https?:\/\/pbs\.twimg\.com\/media\/.*?(?:jpg|png)&name=?.*?$", img_url)
    if surl == None:
        return None
    return surl.group(0).split('&')[0] + "&name=orig"


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
    except:
        pass


def down_img(url, img_name):
    os.makedirs('./' + twerID + '/', exist_ok=True)
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
        final_filename = './' + twerID + '/' + img_name
        #print(final_filename)
        with open(final_filename, 'wb') as fd:
            fd.write(r.content)
    except Exception as e:
        print(e)
        pass


def get_tweet_data(card):
    video_url = ''
    tweet_time_id = ''
    """Extract data from tweet card"""
    try:
        username = card.find_element_by_xpath('.//span').text
    except:
        return
    try:
        handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text.replace('@', '')
    except NoSuchElementException:
        return

    try:
        postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
        reslist = re.findall('\d+', postdate)
        tweet_time_id = ''.join(reslist)
        #print(tweet_time_id)
    except NoSuchElementException:
        return
    try:
        tweet_url = card.find_element_by_xpath('.//a[@dir="auto"]').get_attribute('href')
        # print(tweet_url)
        if card.find_element_by_xpath('.//video'):
            video_url = tweet_url
            # print(video_url)
    except:
        pass
    comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    text = comment + responding
    reply_cnt = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    retweet_cnt = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    like_cnt = card.find_element_by_xpath('.//div[@data-testid="like"]').text
    imgs = card.find_elements_by_xpath('.//img')
    img_urls = [i.get_attribute('src') for i in imgs if
                i.get_attribute('src').startswith('https://pbs.twimg.com/media/')]
    # img_urls = [img_url_fomat(i)+'@' for i in img_urls if img_url_fomat(i)]
    img_url = ''.join([img_url_fomat(i) + '@' for i in img_urls if img_url_fomat(i)])
    for i, v in enumerate(img_urls):
        if img_url_fomat(v):
            # imgUrls.add(img_url_fomat(i))
            imgsDict.setdefault(tweet_time_id+str(i+1), img_url_fomat(v))


    # get a string of all emojis contained in the tweet
    """Emojis are stored as images... so I convert the filename, which is stored as unicode, into 
    the emoji character."""
    emoji_tags = card.find_elements_by_xpath('.//img[contains(@src, "emoji")]')
    emoji_list = []
    for tag in emoji_tags:
        filename = tag.get_attribute('src')
        try:
            emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename).group(1), base=16))
        except AttributeError:
            continue
        if emoji:
            emoji_list.append(emoji)
    emojis = ' '.join(emoji_list)
    if not video_url == '':
        videoUrls.add(video_url)
    tweet = (tweet_time_id, handle, username, postdate, text, reply_cnt, like_cnt, retweet_cnt, img_url, video_url)
    # int_reply_cnt = 0 if reply_cnt == '' else int(reply_cnt.replace(',',''))
    # int_like_cnt = 0 if like_cnt == '' else int(like_cnt.replace(',',''))
    # int_retweet_cnt = 0 if retweet_cnt == '' else int(retweet_cnt.replace(',',''))
    # Sql_Tweet(handle).insert_tweet(tweet_time_id, handle, username,  postdate, text, reply_cnt, like_cnt, retweet_cnt, img_url, video_url)
    return tweet


if cookieData:
    driver.get("https://twitter.com/")
    driver.delete_all_cookies()
    for cook in cookieData:
        try:
            cook.pop('sameSite')
        except:
            pass
        driver.add_cookie(cook)
driver.get("https://twitter.com/{}".format(twerID))
# driver.maximize_window()

# # navigate to login screen
# driver.get('https://www.twitter.com/login')
# driver.maximize_window()
#
# username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
# username.send_keys(user)
#
# password = driver.find_element_by_xpath('//input[@name="session[password]"]')
# password.send_keys(my_password)
# password.send_keys(Keys.RETURN)
sleep(2)

# # find search input and search for term
# search_input = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
# search_input.send_keys(search_term)
# search_input.send_keys(Keys.RETURN)
# sleep(1)

# # navigate to historical 'latest' tab
# driver.find_element_by_link_text('Latest').click()

# get all tweets on the page
data = []
tweet_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True
newest_date = int(Sql_Tweet(twerID).get_newest_timestamp(twerID))
breakCount = 0

while scrolling:
    page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    for card in page_cards[-15:]:
        tweet = get_tweet_data(card)
        if tweet:
            curr_date = int(tweet[0])
            tweet_id = ''.join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                if curr_date <= newest_date:
                    breakCount += 1
                # data.append(tweet)
                Sql_Tweet(twerID).insert_tweet_from_tuple(tweet)

    scroll_attempt = 0
    while True:
        # check scroll position
        # driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        body = driver.find_element_by_css_selector('body')
        body.send_keys(Keys.PAGE_DOWN)
        sleep(2)
        curr_position = driver.execute_script("return window.pageYOffset;")
        # print(curr_position)
        a = len(imgsDict)
        if not a == imgcc:
            print('\rimgs: {0}\t\tposition: {1}'.format(a, curr_position), end='breakCount:{}'.format(breakCount))
            imgcc = a
            # print(breakCount)
        if breakCount >= 4:
            scrolling = False
            break
        if last_position == curr_position:
            scroll_attempt += 1

            # end of scroll region
            if scroll_attempt >= 3:
                scrolling = False
                break
            else:
                sleep(2)  # attempt another scroll
        else:
            last_position = curr_position
            break

# close the web driver
driver.close()

print('Find {} pics'.format(len(imgsDict)))
# for i, v in enumerate(imgUrls):
#     get_down_img(v, twerID)
#     print('\rDownloading... [{}]img'.format(i), end='')

for i, v in enumerate(imgsDict):
    img_filename = '{}_{}_{}.jpg'.format(v[2:8], v[-1], imgsDict[v][-36:-21])
    down_img(imgsDict[v], img_filename)
    # print(imgsDict[v])
    # print(img_filename)
    print('\rDownloading... [{}]img'.format(i), end='')

print('Find {} videos'.format(len(videoUrls)))
for i, v in enumerate(videoUrls):
    cmd = '/usr/local/bin/youtube-dl {} -o ./{}/{}.mp4'.format(v, twerID, v[-19:])
    os.system(cmd)
    print('\rDownloading... [{}]video'.format(i), end='')

if not CloudName == '':
    cmd = 'rclone copy ./{0} {1}:/uploads/twitter/{2}/ -P'.format(twerID, CloudName, twerID)
    print(cmd)
    os.system(cmd)
    # os.remove(path + fin_name + '.mp4')

# [print(i) for i in videoUrls]
# for i in data:
#     Sql_Tweet.insert_tweet(i)

# with open('{}.csv'.format(twerID), 'w', newline='', encoding='utf-8') as f:
#     header = ['Handle', 'UserName', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Likes', 'Retweets', 'imgs', 'video']
#     writer = csv.writer(f)
#     writer.writerow(header)
#     writer.writerows(data)


cmd = "ps aux | grep 'chrome' | awk '{print $2}' | xargs kill"
os.system(cmd)
