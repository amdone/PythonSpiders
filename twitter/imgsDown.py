import os
import ssl

import aiohttp
import asyncio
import time

import requests

urls = []
imgsdir = "imgs"
img_count = 1
os.makedirs('./' + imgsdir + '/', exist_ok=True)
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.89 Safari/537.36'
}

sem = asyncio.Semaphore(12)


async def get_img(url):
    with(await sem):
        async with aiohttp.ClientSession() as session:
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
            # try:
            #     async with session.get(url, headers=kw, ssl=False) as resp:
            #         img_name = './imgs/'+url[-37:-22]+'.jpg'
            #         img = await resp.read()
            #         with open(img_name, 'wb') as fd:
            #             fd.write(img)
            #         #img_count += 1
            #         print(img_name + '...ok!')
            # except aiohttp.client_exceptions.ClientError:
            #     print(aiohttp.client_exceptions.ClientError.__context__)
            #     pass
            async with session.get(url, headers=kw, verify_ssl=False) as resp:
                img_name = './imgs/' + url[-37:-22] + '.jpg'
                img = await resp.read()
                with open(img_name, 'wb') as fd:
                    fd.write(img)
                # img_count += 1
                print(img_name + '...ok!')


async def get_img2(url):
    print(url)
    await request_url(url)


async def request_url(url):
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
    img_name = './imgs/' + url[-37:-22] + '.jpg'
    with open(img_name, 'wb') as fd:
        fd.write(r.content)
        fd.close()


def get_img_onebyone(urllist):
    for surl in urllist:
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
        r = requests.get(surl, headers=kw)
        img_name = './imgs/' + surl[-37:-22] + '.jpg'
        with open(img_name, 'wb') as fd:
            fd.write(r.content)
            fd.close()


def main():
    with open("urls.txt") as lines:
        for line in lines:
            urls.append(line.rstrip('\n'))
            print(line)
    print(len(urls))
    # loop = asyncio.get_event_loop()
    # # img_count = 1
    # tasks = [asyncio.ensure_future(get_img2(url)) for url in urls]
    # loop.run_until_complete(asyncio.wait(tasks))
    # loop.close()
    get_img_onebyone(urls)


if __name__ == '__main__':
    start = time.time()
    # img_count = 0
    main()
    print('总耗时：%.5f秒' % float(time.time() - start))
