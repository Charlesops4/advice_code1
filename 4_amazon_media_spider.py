import os
import time

import requests
from faker import Faker

#data_url.txt（media_url for amazon.com）
"""
https://m.media-amazon.com/images/S/vse-vms-transcoding-artifact-us-east-1-prod/143a6514-bf70-43e3-857b-5fc14f364058/default.jobtemplate.hls1080.m3u8
"""

#ts.txt（movie split to ts data）  
"""
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:7
#EXT-X-MEDIA-SEQUENCE:1
#EXT-X-PLAYLIST-TYPE:VOD
#EXTINF:6,
default.jobtemplate.hls1080_00001.ts
#EXTINF:6,
default.jobtemplate.hls1080_00002.ts
#EXTINF:6,
default.jobtemplate.hls1080_00003.ts
#EXTINF:6,
default.jobtemplate.hls1080_00004.ts
#EXTINF:6,
default.jobtemplate.hls1080_00005.ts
#EXTINF:5,
default.jobtemplate.hls1080_00006.ts
#EXT-X-ENDLIST

"""

fake = Faker()
user_agent = fake.user_agent()
headers = {
        "user-agent":f"{user_agent}",
        "referer":"https://www.amazon.com/",
}

#自建代理，已废弃
def get_proxy():
    proxy_api_url = "http://localhost:xxx/random"
    try:
        response = requests.get(proxy_api_url)
        if response.status_code == 200:
            proxy_pool = response.text
            return proxy_pool
    except ConnectionError:
        return None

#无代理可不写
proxies={'http':'http://' + get_proxy()}

#start 响应中获取ts数据
def getTsDatabystartUrl(starturlFile):
    with open(starturlFile,'r',encoding='utf-8') as f:
        starturl = f.readline()
    response = requests.get(url=starturl,headers=headers,proxies=proxies) 
    response.encoding = 'utf-8'
    content = response.text
    with open('ts.txt','w',encoding='utf-8') as ts:
        ts.write(content)
    ts_datas = []
    with open('ts.txt','r',encoding='utf-8') as f:
        while True:
            data_str = f.readline()
            if 'default.' in data_str:
                ts_data = data_str[len('default.'):]
                ts_datas.append(ts_data)
            if '#EXT-X-ENDLIST' in data_str:
                break
    return ts_datas

#拼接ts_url
def getTsUrl(starturlFile,ts_datas):
    ts_urls = []
    with open(starturlFile, 'r', encoding='utf-8') as f:
        starturl = f.readline()
    for ts_data in ts_datas:
        sub_index = starturl.find('default.') + len('default.')
        ts_url = starturl[0:sub_index] + ts_data.replace('\n','')
        ts_urls.append(ts_url)
    return ts_urls


#下载ts文件
def download(ts_urls,tsFiles):
    for i in range(len(ts_urls)):
        ts_url = ts_urls[i]
        try:
            response = requests.get(url=ts_url,headers=headers,proxies=proxies)
        except Exception as e:
            print('异常请求: %s' % e.args)
            return
        ts_path = tsFiles + '/{0}.ts'.format(i)
        with open(ts_path,'wb+') as file:
            for chunk in response.iter_content(chunk_size=1024):     #1024及其倍数下载
                if chunk:
                    file.write(chunk)
        time.sleep(.57)

#将ts文件按顺序加入列表
def file_walker(path):
    file_list = os.listdir(path)
    file_list.sort(key=lambda x: int(x[:-3]))
    file_list_ = []
    for fn in file_list:
        p = str("tsfiles" + '/' + fn)
        file_list_.append(p)
    return file_list_

#将ts文件组合为mp4视频
def combine(ts_path, file_name):
    file_list = file_walker(ts_path)
    file_path = file_name + '.MP4'
    with open(file_path, 'wb+') as fw:
        for i in range(len(file_list)):
            fw.write(open(file_list[i], 'rb').read())

if __name__ == '__main__':
    ts_datas = getTsDatabystartUrl('data_url.txt')
    ts_urls = getTsUrl('data_url.txt',ts_datas)
    download(ts_urls,'tsFiles')
    combine("tsFiles", "xiaojiejie")
