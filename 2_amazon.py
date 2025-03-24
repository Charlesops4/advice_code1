import queue
import random
import threading
import time

import pymysql
import requests
from dbutils.pooled_db import PooledDB
from faker import Faker
from lxml import etree

#爬取amazon指定商品的评级，价格，图片等

fake = Faker()
user_agent = fake.user_agent()
headers = {
        "user-agent":f"{user_agent}",
        "cookie":'' #自行获取
}
max_retry = 2

lock = threading.Lock()

#尝试了下数据库的JDBC连接池

def get_conn():
    for _ in range(1,11):
        print('开始初始化数据库连接--------')
        pool = PooledDB(
            creator=pymysql,
            maxconnections=10,
            mincached=2,
            maxcached=5,
            maxshared=0,
            blocking=False,
            maxusage=None,
            setsession=[],
            host='XXXX',
            port=XXXX,
            user='XXXX',
            password='XXXX',
            database='XXXX',
            autocommit=True)
        print('初始化数据库连接成功--------')
        return pool

#自建的一个proxy，已废弃
# def get_proxy():
#     proxy_api_url = "http://localhost:xxxx/random"
#     try:
#         response = requests.get(proxy_api_url)
#         if response.status_code == 200:
#             proxy_pool = response.text
#             proxies = {'http': 'http://' + proxy_pool}
#             return proxies
#     except ConnectionError:
#         return None


def get_amazon_html(file,commodity,retries=0):
  #拼接url
    url = "https://www.amazon.com/s?k=" + commodity
    try:
        response = requests.get(url=url,headers=headers)
        content = response.text
        with open(file,"w",encoding="utf-8") as f:
            text = f.write(content)
        time.sleep(random.randint(5,10))
        get_amazon_data(text)
    except Exception as e:
        print(str(e))
        if retries < max_retry:
            return get_amazon_html(commodity,retries + 1)

#利用xpath获取页面数据
def get_amazon_data(text):
    with open(file, "r", encoding="utf-8") as f:
        content = etree.HTML(f.read())
    result = {}
    titles_list = []
    titles = content.xpath('//div/div/div/div/span/div/div/div[2]/div[1]/a/h2')
    for index,title in enumerate(titles):
        titles_list.append(title.xpath('./span/text()')[0])
    result['titles_list'] = titles_list
    prices_list = []
    prices = content.xpath('//div/div/div/div/span/div/div/div[2]/div[3]/div/div[1]/a/span[1]')
    for index,price in enumerate(prices):
        prices_list.append(price.xpath('./span[1]/text()')[0])
    result['prices_list'] = prices_list
    grads_list = []
    grads = content.xpath('//div/div/div/div/span/div/div/div[2]/div[2]/div[1]/span[1]/a')
    for index,grad in enumerate(grads):
        grads_list.append(grad.xpath('./span/text()')[0])
    result['grads_list'] = grads_list
    imgs_list = []
    imgs = content.xpath('//div/div/div/div/span/div/div/div[1]/span/a/div/img/@src')
    for index,img in enumerate(imgs):
        imgs_list.append(img.xpath('./@src')[0])
    result['imgs_list'] = imgs_list
    return result

#将数据保存在数据库中
def save_mysql(result):
    with lock:
        with get_conn().connection() as conn:
            with conn.cursor() as cursor:
                for i in range(len(result['grads_list'])):
                    sql = f"insert into amazon_list(title,price,grad,img) values('{result['titles_list'][i]}','{result['prices_list'][i]}','{result['grads_list'][i]}','{result['imgs_list'][i]}')"
                    cursor.execute(sql)

if __name__ == '__main__':
    commodity = input("请输入你要查询的商品：")
    file = 'amazon.html'
    # proxies = get_proxy()
    get_amazon_html(file,commodity,retries=0)
    result = get_amazon_data(file)
    get_amazon_data(file)
    save_mysql(result)

#还有部分不太完美，例如有些商品没有评级数据，会导致数据保存时的错位问题，可在页面一个一个商品提取【涉及的数据】，这块自行补充哈
