import getopt
import sys
import time

from Sina_scrapy.news_spider.master import Master
from Sina_scrapy.news_spider.settings import Settings
from Sina_scrapy.news_spider.slave import Slave

"""
分布式动态网页爬取
内容财经要闻
"""


def main(argv):
    #根据当前运行的是主机还是从机进行任务分配，从机负责爬取数据
    #设置master和slave的参数
    settings=Settings()
    currentType=settings.getCurrentMachine(argv)

    if currentType=="master":
        #实例化以后master开始给slave发送URL请求
        master=Master()
        master.sendtask()
        master.dispatch()

    elif currentType=="slave":
        #slave开始处理网页爬去数据工作
        slave=Slave(int(time.time()))
        slave.mongoset()
        slave.captureData()

if __name__ == '__main__':
    main(sys.argv)