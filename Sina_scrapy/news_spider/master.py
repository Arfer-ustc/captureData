import json
import socket
import threading
import time

from selenium import webdriver

from Sina_scrapy.news_spider.settings import Settings
from Sina_scrapy.news_spider.taskManage import TaskList


class Master:
    settings = Settings()
    __list=None
    __socket=None
    __url="http://finance.sina.com.cn/7x24/?tag="

    __adress=settings.__ADRESS__
    __port_=settings.__PORT__
    def __init__(self):
        # 对主机socket进行设置
        self.__list=TaskList(30)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind(("0.0.0.0", 8888))
        self.__socket.listen(50)


    #往任务列表中添加任务
    def sendtask(self):
        chrome_options = webdriver.ChromeOptions()  # 获取ChromeWebdriver配置文件
        prefs = {"profile.managed_default_content_settings.images": 2}  # 设置不加载图片以加快速度
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--headless")  # 不使用GUI界面
        chrome_options.add_argument("--disable-gpu")  # 禁用GPU渲染加速
        driver = webdriver.Chrome(chrome_options=chrome_options)  # 创建ChromeWebdriver
        driver.set_page_load_timeout(10)  # 设置连接超时时间为15s
        driver.get("http://finance.sina.com.cn/7x24/?tag={}".format("1"))

        news_url=list()
        for i in range(1,9):
            news_url.append("http://finance.sina.com.cn/7x24/?tag="+str(i))
        self.__list.put_tasks(news_url)
        time.sleep(1)

        driver.close()

    # 监听网络端口以分发任务 #
    def dispatch(self):
        print("Waiting.................")
        while True:
            # 若任务列表为空，则程序退出
            if self.__list.is_empty():
                print("No task in list")
            # 接受来自Slave节点的连接
            conn, addr = self.__socket.accept()
            try:
                conn.settimeout(10)
                # 接收请求数据
                req = json.loads(conn.recv(1024).decode("utf-8"))
                # 若Slave的请求命令为get，则向其发送新任务并将任务加入pending队列中
                if req["cmd"] == "get":
                    res = dict(
                        status=dict(
                            code=0,
                            msg="success"
                        ),
                        data=dict(
                            news_url=self.__dispatch_task__()  # 调用dispatch_task()函数时会自动将任务加入pending队列
                        )
                    )
                    conn.send(json.dumps(res).encode("utf-8"))
                    print("Dispatch {0} to slave {1}".format(res["data"], req["id"]))
                # 若Slave的请求命令为done，则将pending队列中相应的任务移除
                elif req["cmd"] == "done":
                    self.__done_task__(req["data"]["news_url"])
                    res = dict(
                        status=dict(
                            code=0,
                            msg="success"
                        ),
                        data=""
                    )
                    conn.send(json.dumps(res).encode("utf-8"))
                    print("Slave {0} done fetching '{1}'".format(req["id"], req["data"]["news_url"]))
            except socket.timeout:
                print("Connection timeout")
            conn.close()
    # 分发任务 #
    def __dispatch_task__(self):
        news_url = self.__list.get_task()
        if news_url is None:
            return -1
        return news_url

    # 完成任务 #
    def __done_task__(self, news_url):
        self.__list.done_task(news_url)    # 将任务从pending列表中移除



