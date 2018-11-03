** attention: this is only used for feasibility analysis and codes are not optimized for production. **

## PyCrawlerForText(WIP) ##

......分布式框架 master负责分布urls urls也是从网页中爬取出来的 
slave负责从URL中爬取新闻信息 此段代码与上层capture雷同，但结构更严谨，爬取效率更高

### Usages ###

Run master node:

```
python newscrawler.py --master
```

Run slave node:

```
python newscrawler.py --slave
```
