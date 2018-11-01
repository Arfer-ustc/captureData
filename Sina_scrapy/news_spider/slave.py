import json
import socket
import time

import pymongo
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime

from Sina_scrapy.news_spider.settings import Settings


class Slave:
    settings = Settings()
    __port=settings.__port__
    __adress=settings.__adress__
    __slave_id=None

    __mongoaddr=settings.__adressdb__
    __mongoport=settings.__portdb__

    __item_info=None

    def __init__(self, id):
        self.__slave_id = id
    # 获取任务函数 #
    def __get_task__(self):
        # 向Master节点发送的结构中包含一个'get'标志和自己的id
        req = dict(
            id=self.__slave_id,
            cmd="get"
        )
        res = self.__send_msg__(req)
        if res["status"]["code"] == 0:
            return res["data"]["news_url"]
        return -1
    # 发送和获取响应函数 #

    def __send_msg__(self, dict_msg):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.__adress, self.__port))
        sock.send(json.dumps(dict_msg).encode("utf-8"))
        res = json.loads(sock.recv(1024))
        sock.close()
        return res
    # 完成任务函数 #

    def __done_task__(self, news_url):
        # 这里会向Master节点发送一个完成任务的请求
        req = dict(
            id=self.__slave_id,
            cmd="done",
            data=dict(
                news_url=news_url
            )
        )
        self.__send_msg__(req)


    def mongoset(self):
        client = pymongo.MongoClient()

        ceshi = client['Arfer_news_scrapy']
        item_info = ceshi['info']
        self.__item_info=item_info

    def captureData(self):
        chrome_options = webdriver.ChromeOptions()  # 获取ChromeWebdriver配置文件
        prefs = {"profile.managed_default_content_settings.images": 2}  # 设置不加载图片以加快速度
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--headless")  # 不使用GUI界面
        chrome_options.add_argument("--disable-gpu")
        __webdriver=webdriver.Chrome(chrome_options=chrome_options)
        __webdriver.set_page_load_timeout(10)

        while True:
            try:
                url=self.__get_task__()
                if url == -1:
                    print("all work have been done")
                    time.sleep(2)
                    continue
                print("当前URL："+url)
                #抓取页面数据
                __webdriver.get(url)
                query = self.__item_info.find_one({"url": url})
                if query is not None:
                    break
                # 下拉滚动条，使浏览器加载出动态加载的内容，可能像这样要拉很多次，中间要适当的延时（跟网速也有关系）。
                # 如果内容都很长，就增大下拉的长度。
                __webdriver.execute_script("window.scrollBy(0,10000)")
                time.sleep(3)
                __webdriver.execute_script("window.scrollBy(0,20000)")
                time.sleep(3)
                __webdriver.execute_script("window.scrollBy(0,20000)")
                time.sleep(3)
                __webdriver.execute_script("window.scrollBy(0,30000)")
                time.sleep(3)
                __webdriver.execute_script("window.scrollBy(0,40000)")
                time.sleep(4)
                __webdriver.execute_script("window.scrollBy(0,50000)")
                time.sleep(4)

                soup = BeautifulSoup(__webdriver.page_source, 'xml')
                contents = soup.find_all('p', {'class': 'bd_i_txt_c'})  # 新闻的内容
                times = soup.find_all('p', {'class': 'bd_i_time_c'})  # 发表时间

                realdata = dict(
                    _id=url,
                    name=self.settings.getName(url),
                    data=[]
                )

                for content, _time in zip(contents, times):  # 这里_time的下划线是为了与time模块区分开
                    data_get = []
                    json_data = dict(
                        symbolTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+_time.get_text(),
                        time=_time.get_text(),  # 时间
                        content=content.get_text()  # 文章
                    )
                    data_get.append(json_data)
                    realdata["data"].extend(data_get)
                    print(content.get_text(), _time.get_text())

                self.__item_info.insert_one(realdata)
                json_data.clear()
                realdata.clear()
            except socket.error:
                print("something error occured")
                time.sleep(5)
