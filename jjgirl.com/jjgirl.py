import os
import aiohttp
import asyncio
import time

girl_name = 'miku-ohashi'
page_start = 1
page_end = 63

os.makedirs('./'+girl_name+'/',exist_ok=True)


urls = []

sem = asyncio.Semaphore(12)

async def get_img(url):
    with(await sem):
        async with aiohttp.ClientSession() as session:
            kw = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64)'}
            try:
                async with session.get(url,headers=kw) as resp:
                    img_name = './'+girl_name+'/'+girl_name+'_'+url.split('/')[5]+'_'+url.split('-')[3]
                    img = await resp.read()
                    with open(img_name,'wb') as fd:
                        fd.write(img)
                    global img_count
                    img_count+=1
                    print(str(img_count)+'-->'+img_name+'...ok!')
            except aiohttp.client_exceptions.ClientError:
                 print("连接失败")
                 pass
                

def main():
    loop = asyncio.get_event_loop()
    for page_down in range(page_start,page_end+1):
        urls.clear()
        for i in range(0,12):
            urls.append('https://www.jjgirls.com/japanese/'+girl_name+'/'+str(page_down)+'/'+girl_name+'-'+str(i+1)+'.jpg')
        tasks = [get_img(url) for url in urls]
        loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

if __name__ == '__main__':
    start = time.time()
    img_count = 0
    main()
    print('总耗时：%.5f秒' % float(time.time()-start))
