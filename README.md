# captureData
此段代码为科大第一学期工程实践前期项目摸底训练——用分布式框架爬去新浪财经新闻，将数据存储到mongodb上
在本地模拟两台机器，开两个节点 master slave 
其中 master负责分发任务，slave负责从任务池中获取URL列表，爬去对应网站新闻内容
节点设置如下：
1、edit configuration里点+号 parameter填--master 然后路径神马的统统复制一遍，相同的步骤再来一遍 parameter填--slava
运行startpage

特别注意：
文件中import 的内容前部分为完整路径 如Sina_scrapy.news_spider.master，Sina_scrapy.news_spider部分可根据你实际文件路径进行调整

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
