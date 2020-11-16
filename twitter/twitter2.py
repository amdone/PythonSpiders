import json
import os
import re
import csv
from getpass import getpass
from time import sleep

import requests
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


# create some value for easy use:
imgUrls = set()
twerID = "iJoycebabe"
twerName = ""
twitter_url = "https://twitter.com"
twitter_url = "https://twitter.com/ry01204"
twerDescription = ""
twerCreatedDate = ""
twerFans = ""
twerLocation = ""
timeSet = set()
imgcc = 0

# chrome start setting
chrome_options = Options()

chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')  # root用户不加这条会无法运行
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(chrome_options=chrome_options)
#driver.set_window_size(480, 1080)


# get cookie,twerlist form files

with open('cookie.json', 'r', encoding='utf8')as fp:
    cookieData = json.load(fp)


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
            fd.close()
    except:
        pass


def get_tweet_data(card):
    global imgcc
    """Extract data from tweet card"""
    try:
        username = card.find_element_by_xpath('.//span').text
    except:
        return
    try:
        handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    except NoSuchElementException:
        return

    try:
        postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
    except NoSuchElementException:
        return

    comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    text = comment + responding
    reply_cnt = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    retweet_cnt = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    like_cnt = card.find_element_by_xpath('.//div[@data-testid="like"]').text
    imgs = card.find_elements_by_xpath('.//img')
    img_urls = [i.get_attribute('src') for i in imgs if i.get_attribute('src').startswith('https://pbs.twimg.com/media/')]
    # img_urls = [img_url_fomat(i)+'@' for i in img_urls if img_url_fomat(i)]
    img_url = ''.join([img_url_fomat(i)+'@' for i in img_urls if img_url_fomat(i)])
    for i in img_urls:
        if img_url_fomat(i):
            imgUrls.add(img_url_fomat(i))
    a = len(imgUrls)
    if not a == imgcc:
        print('imgs: {}'.format(a))
        imgcc = a

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

    tweet = (username, handle, postdate, text, emojis, reply_cnt, retweet_cnt, like_cnt, img_url)
    return tweet


# # application variables
# user = input('username: ')
# my_password = getpass('Password: ')
# search_term = input('search term: ')

# create instance of web driver


driver.get("https://twitter.com/")
driver.delete_all_cookies()
for cook in cookieData:
    try:
        cook.pop('sameSite')
    except:
        pass
    driver.add_cookie(cook)

driver.get("https://twitter.com/{}".format(twerID))
driver.maximize_window()

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
sleep(3)

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

while scrolling:
    page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    for card in page_cards[-15:]:
        tweet = get_tweet_data(card)
        if tweet:
            tweet_id = ''.join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                data.append(tweet)

    scroll_attempt = 0
    while True:
        # check scroll position
        # driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        body = driver.find_element_by_css_selector('body')
        body.send_keys(Keys.PAGE_DOWN)
        sleep(2)
        curr_position = driver.execute_script("return window.pageYOffset;")
        print(curr_position)
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

for i in imgUrls:
    get_down_img(i, twerID)

with open('{}.csv'.format(twerID), 'w', newline='', encoding='utf-8') as f:
    header = ['UserName', 'Handle', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Likes', 'Retweets', 'imgs']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)
