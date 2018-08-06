# -*- coding: utf-8 -*-

# Scrapy settings for LianjiaScrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'LianjiaScrapy'

SPIDER_MODULES = ['LianjiaScrapy.spiders']
NEWSPIDER_MODULE = 'LianjiaScrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Cookie': 'select_city=510100; all-lj=ed5a77c9e9ec3809d0c1321ec78803ae; lianjia_ssid=a763e302-a9d5-43d6-a640-03352a627598; lianjia_uuid=b7533e69-8eef-4c6c-95e1-129edada1c1a; TY_SESSION_ID=15c3f613-d07a-4d1e-89c6-7f5e01e40e8c; gr_user_id=47967b75-60e5-4fd8-b96c-49d85c3dfce6; gr_session_id_a1a50f141657a94e=e8be30f7-d87e-4a47-a612-be4d0d3c2c57; _jzqa=1.4236220147237116000.1532574069.1532574069.1532574069.1; _jzqc=1; _jzqckmp=1; _qzja=1.963616111.1532574068958.1532574068958.1532574068958.1532574068958.1532574068958.0.0.0.1.1; _qzjc=1; _qzjto=1.1.0; _smt_uid=5b593975.2588e3a9; UM_distinctid=164d4887136519-0f22a0b8d38afc-454c092b-1fa400-164d488713770c; CNZZDATA1253492306=2059677479-1532570860-%7C1532570860; CNZZDATA1254525948=778168439-1532569486-%7C1532569486; CNZZDATA1255633284=19171736-1532572374-%7C1532572374; CNZZDATA1255604082=1749984547-1532573179-%7C1532573179; _jzqb=1.1.10.1532574069.1; _qzjb=1.1532574068958.1.0.0.0; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1532574069; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1532574069; gr_session_id_a1a50f141657a94e_e8be30f7-d87e-4a47-a612-be4d0d3c2c57=true; _ga=GA1.2.1303821376.1532574071; _gid=GA1.2.1793237328.1532574071',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'LianjiaScrapy.middlewares.LianJiaScrapySpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'LianjiaScrapy.middlewares.UAMiddleware': 100,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'LianjiaScrapy.pipelines.LianjiaMongodbPipeline': 100,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MONGODB_HOST = 'localhost'  # 本地数据库
MONGODB_PORT = '27017'  # 数据库端口
MONGODB_URI = 'mongodb://{}:{}'.format(MONGODB_HOST, MONGODB_PORT)
MONGODB_DATABASE = 'LianJia'  # 数据库名字
