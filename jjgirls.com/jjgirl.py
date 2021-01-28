import os
import aiohttp
import asyncio
import time
import argparse

parser = argparse.ArgumentParser(description='Just give mw a name!')
parser.add_argument('girlname', type=str, help="girl's name")
parser.add_argument('-s', '--start', type=int, help="Start Page's Number", default=1)
parser.add_argument('-e', '--end', type=int, required=True, help="End Page's Number")
parser.add_argument('-t', '--time', type=int, help="Sleep seconds When Downloading images", default=0)
parser.add_argument('-q', '--quiet', help="Quiet Run", action='store_true')
parser.add_argument('-E', '--error', help="show error url", action='store_true')
args = parser.parse_args()

girl_name = args.girlname
page_start = args.start
page_end = args.end
sleep_seconds = args.time
show_error = args.error
print('Name: {}\nStart_Page: {}\tEnd_Page: {}\t\nStarting...\n'.format(girl_name, page_start, page_end, sleep_seconds))

os.makedirs('./' + girl_name + '/', exist_ok=True)

urls = []
error_urls = []


# sem = asyncio.Semaphore(12)

async def get_img(url):
    # with(await sem):
    async with aiohttp.ClientSession() as session:
        kw = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'}
        try:
            async with session.get(url, headers=kw) as resp:
                # img_name = './'+girl_name+'/'+girl_name+'_'+url.split('/')[5]+'_'+url.split('-')[3]
                img_name = './{0}/{0}_{1:0>2d}_{2:0>3d}.jpg'.format(girl_name, url.split('/')[5], url.split('-')[3])
                img = await resp.read()
                with open(img_name, 'wb') as fd:
                    fd.write(img)
                global img_count
                img_count += 1
                if args.quiet is True:
                    print('\r{}'.format(img_count))
                else:
                    print(str(img_count) + '-->' + img_name + '...ok!')
        except aiohttp.client_exceptions.ClientError:
            global error_img_count
            error_img_count += 1
            error_urls.append(url)
            if args.quiet is True:
                pass
            else:
                print(str(img_count) + '-->' + img_name + '...Connect Error!')


def main():
    loop = asyncio.get_event_loop()
    for page_down in range(page_start, page_end + 1):
        urls.clear()
        for i in range(0, 12):
            urls.append(
                'https://www.jjgirls.com/japanese/' + girl_name + '/' + str(page_down) + '/' + girl_name + '-' + str(
                    i + 1) + '.jpg')
        tasks = [get_img(url) for url in urls]
        loop.run_until_complete(asyncio.wait(tasks))
        time.sleep(sleep_seconds)
    loop.close()


if __name__ == '__main__':
    start = time.time()
    img_count = 0
    error_img_count = 0
    main()
    print('总耗时：%.5f秒' % float(time.time() - start))
    print('Error: {}'.format(error_img_count))
    if show_error:
        for error in error_urls:
            print(error)
