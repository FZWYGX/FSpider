from scrapy.http import Request
import scrapy.dupefilters


def init_add_request(spider, url):
    """
    此方法用于在，scrapy启动的时候添加一些已经跑过的url，让爬虫不需要重复跑

    """
    rf = spider.crawler.engine.slot.scheduler.df  # 找到实例化对象

    request = Request(url)
    rf.request_seen(request)  # 调用request_seen方法
