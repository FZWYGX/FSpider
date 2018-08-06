# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from traceback import format_exc
from ..items import LianjiaZufangItem, LianjiaErshoufangItem, LianjiaNewItem
import re


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    # sh表示上海, hz表示杭州, bj表示北京, sz表示深圳, cd表示成都
    host = ['sh', 'hz', 'bj', 'sz', 'cd']  # 'gz'广州, 'cq'重庆 (区域地址可以增加)

    def start_requests(self):
        """
        构造起始链接
        """

        new_start_urls = ['https://{}.fang.lianjia.com/loupan/'.format(host) for host in self.host]
        er_start_urls = ['https://{}.lianjia.com/ershoufang/'.format(host) for host in self.host]
        zu_start_urls = ['https://{}.lianjia.com/zufang/'.format(host) for host in self.host]

        for url_new in new_start_urls:
            # 下面代码是去抓取链家新房信息
            yield Request(url_new, callback=self.parse_area_new, errback=self.error_back)

        for url_er in er_start_urls:
            # 下面代码是去抓取链家二手房信息
            yield Request(url_er, callback=self.parse_area_er, errback=self.error_back)

        for url_zu in zu_start_urls:
            # 下面代码是去抓取链家租房信息
            yield Request(url_zu, callback=self.parse_area_zu, errback=self.error_back)

    def parse_area_new(self, response):
        url = response.url
        host = re.findall(r'https://(\w+)\.fang\.lianjia\.com/', url)
        # 匹配出host, 为后面的拼接新房地址链接做准备
        host = host[0]
        # 匹配每一个区,　如：北京的朝阳区,　成都的锦江区等等
        new_urls = response.xpath("//ul[@class='district-wrapper']/li/@data-district-spell").extract()
        if new_urls is not None:
            for new_url in new_urls:
                # 讲基础的url与匹配来的区域进行拼接
                new_url = 'https://{}.fang.lianjia.com/loupan/'.format(host) + new_url
                print(new_url)
                # 回调新房翻页代码
                yield Request(new_url,
                              callback=self.parse_new_fanye,
                              errback=self.error_back,
                              meta={"host": host})

    def parse_new_fanye(self, response):
        host = response.meta["host"]
        new_url = response.url
        # 手动拼写翻页规则
        for i in range(1, 30):
            url = new_url + "/" + "pg" + str(i) + "/"
            print(url)
            # 回调解析新房列表页的代码
            yield Request(url,
                          callback=self.NewHouse_index_pag,
                          errback=self.error_back,
                          meta={"host": host})

    def NewHouse_index_pag(self, response):
        host = response.meta["host"]
        # 匹配每一个列表页的所有详情页的url链接
        urls = response.xpath('//ul[@class="resblock-list-wrapper"]//li/a/@href').extract()
        if urls is not None:
            for url in urls:
                print('https://{}.fang.lianjia.com'.format(host) + url)
                # 回调解析详情页的代码
                yield Request(url='https://{}.fang.lianjia.com'.format(host) + url,
                              callback=self.NewHouse_detail_pag,
                              errback=self.error_back,
                              priority=5)

    def NewHouse_detail_pag(self, response):
        """
        这个代码是用来解析新房详情页
        """

        # 实例化新房item
        item = LianjiaNewItem()
        # 城市
        item['city'] = response.xpath('//div[@class="mid-content"]/div/a[2]/text()').extract_first().replace("新房", "")
        # 区域
        item['region'] = ">".join(response.xpath('//div[@class="mid-content"]//a/text()').extract())
        # 名字
        item['name'] = response.xpath('//div[@class="banner-box"]//h1/text()').extract_first()
        # url
        item['url'] = response.url

        # 地址
        price = response.xpath('//div[@class="banner-box"]//p[@class="jiage"]//text()').extract()
        item['price'] = ":".join(i.strip() for i in price if len(i.strip()) > 0 and "别名" not in i)

        # 户型介绍
        typeInfos = response.xpath('//div[@data-index="0"]//div[@class="houselist"]//li[@class="info-li"]')
        item["typeInfo"] = []
        item["typeInfo"] += ["-".join(i.xpath('./p[1]//text()').extract()) for i in typeInfos]

        # 房屋信息
        houseInfo = response.xpath('//div[@class="box-loupan"]//p//text()').extract()
        houseInfo = [i.strip().replace("：", "") for i in houseInfo if len(i.strip()) > 0]

        for i in range(len(houseInfo)):
            if "项目地址" in houseInfo[i]:
                # 地址
                item['address'] = houseInfo[i + 1]
            elif "售楼处地址" in houseInfo[i]:
                # 售楼处地址
                item['saleAddress'] = houseInfo[i + 1]
            elif "开发商" in houseInfo[i]:
                # 开发商
                item['developer'] = houseInfo[i + 1]
            elif "最新开盘" in houseInfo[i]:
                # 最新开盘
                item['openTime'] = houseInfo[i + 1]
            elif "物业类型" in houseInfo[i]:
                # 物业类型
                item['property'] = houseInfo[i + 1]

        # 房屋信息
        item['houseInfo'] = {houseInfo[i]: houseInfo[i + 1] for i in range(len(houseInfo) - 1) if i % 2 == 0}
        print(item)
        yield item

    def parse_area_er(self, response):
        # 用正则表达式匹配行政分区, 如：北京的朝阳区,　成都的锦江区等等
        links = re.compile(r'<a href="/ershoufang/([a-z]*?/)"  title=".*?">.*?</a>')
        er_urls = re.findall(links, response.text)
        if er_urls is not None:
            for er_url in er_urls:
                # 用urljoin构造以行政区为单位的二手房列表页
                er_url = response.urljoin(er_url)
                # 回调翻页代码
                yield Request(er_url,
                              callback=self.parse_er_fanye,
                              errback=self.error_back)

    def parse_er_fanye(self, response):
        """
        二手房翻页
        """
        er_url = response.url
        # 链家的翻页信息不在源代码里面, 直接拼接
        for i in range(1, 101):
            url = er_url + "pg" + str(i) + "/"
            yield Request(url,
                          callback=self.Ershoufang_index_pag,
                          errback=self.error_back)

    def Ershoufang_index_pag(self, response):
        """
        解析二手房列表页，并抓取每一个详情页的url链接，
        抓取二手房的列表页,示例网址：https://cd.lianjia.com/ershoufang/jinjiang/
        """
        urls = response.xpath('//ul[@class="sellListContent"]//li/a/@href').extract()
        print(urls)
        if urls is not None:
            for url in urls:
                # 回调二手房列表页小区url的列表
                yield Request(url,
                              callback=self.Ershoufang_detail_pag,
                              errback=self.error_back,
                              priority=5)

    def Ershoufang_detail_pag(self, response):
        """
        抓取二手房小区详情的url,示例网址：https://cd.lianjia.com/ershoufang/106101141691.html
        """
        # 实例化二手房item
        item = LianjiaErshoufangItem()
        # 匹配链家id
        id = re.findall(r'/(\w{0,4}\d+)\.', response.url)
        # 链家编号
        item['id'] = id[0]
        # 名字
        item['name'] = response.xpath('//div[@class="sellDetailHeader"]//h1/@title').extract_first()
        # url
        item['url'] = response.url
        # 城市
        item['city'] = response.xpath('//div[@class="intro clear"]//a[2]/text()').extract_first().replace("二手房", "")
        # 区域
        item['region'] = ">".join(response.xpath('//div[@class="intro clear"]//a/text()').extract())

        # 地址
        address = response.xpath('//div[@class="aroundInfo"]/div[2]/span//text()').extract()
        item['address'] = ">".join(i for i in address if i != "\xa0").replace("\xa0", "")

        price = response.xpath('//div[@class="overview"]//div[@class="price "]//span//text()').extract()
        # 总价
        item['price_total'] = price[0] + price[1]
        # 单价
        item['price_per'] = price[2] + price[3]

        # 房屋信息
        item['houseInfo'] = response.xpath('//div[@class="overview"]//div[@class="houseInfo"]//text()').extract()

        # 基础信息
        BaseInfo = response.xpath('//div[@class="introContent"]/div[1]/div[2]//text()').extract()
        BaseInfo = [i.strip() for i in BaseInfo if len(i.strip()) > 0]
        BaseInfo = {BaseInfo[i]: BaseInfo[i + 1] for i in range(len(BaseInfo) - 1) if i % 2 == 0}
        item['BaseInfo'] = BaseInfo

        # 交易属性
        transactionInfo = response.xpath('//div[@class="introContent"]/div[2]/div[2]//text()').extract()
        transactionInfo = [i.strip() for i in transactionInfo if len(i.strip()) > 0]
        transactionInfo = {transactionInfo[i]: transactionInfo[i + 1] for i in range(len(transactionInfo) - 1) if
                           i % 2 == 0}
        item['transactionInfo'] = transactionInfo

        # 房源特色
        feature = response.xpath('//div[@class="baseattribute clear"]//text()').extract()
        feature = [i.strip() for i in feature if len(i.strip()) > 0]
        feature = {feature[i]: feature[i + 1] for i in range(len(feature) - 1) if i % 2 == 0}
        item['feature'] = feature

        # 经纬度信息
        Position = re.findall(r"resblockPosition:\'(.*?)\',", response.text)
        Position = Position[0]
        item['Position'] = Position

        print(item)
        yield item

    def parse_area_zu(self, response):
        # 用正则表达式匹配行政分区, 如：北京的朝阳区,　成都的锦江区等等
        links = re.compile('<a href="/zufang/([a-z]*?/)">.*?</a>')
        zu_urls = re.findall(links, response.text)
        if zu_urls is not None:
            for zu_url in zu_urls:
                if zu_url is not None:
                    # 用urljoin构造以行政区为单位的租房列表页
                    area_url = response.urljoin(zu_url)
                    # 回调翻页代码
                    yield Request(area_url,
                                  callback=self.parse_zu_fanye,
                                  errback=self.error_back)

    def parse_zu_fanye(self, response):
        zu_url = response.url
        # 租房翻页, 链家的翻页不在源码中, 所以手动拼接
        for i in range(1, 101):
            url = zu_url + "pg" + str(i) + "/"
            # 回调租房列表页
            yield Request(url,
                          callback=self.Zufang_index_pag,
                          errback=self.error_back)

    def Zufang_index_pag(self, response):
        """
        解析租房列表页，并抓取每一个详情页的url链接，
        抓取链家租房列表页，示例网址：https://cd.lianjia.com/zufang/jinjiang/
        """
        urls = response.xpath('//ul[@id="house-lst"]//li/div/a/@href').extract()
        print(urls)
        if urls is not None:
            for url in urls:
                # 回调租房列表页小区url的列表
                yield Request(url,
                              callback=self.Zufang_detail_pag,
                              errback=self.error_back,
                              priority=5)

    def Zufang_detail_pag(self, response):
        """
        解析租房详情页
        """
        # 实例化租房item
        item = LianjiaZufangItem()

        # 链家编号
        id = re.findall(r'/(\w{0,4}\d+)\.', response.url)
        item['id'] = id[0]
        # 城市
        item['city'] = response.xpath('//div[@class="intro clear"]//a[2]/text()').extract_first().replace("租房", "")
        # url
        item['url'] = response.url
        # 行政分区
        item['region'] = ">".join(response.xpath('//div[@class="intro clear"]//a/text()').extract())
        # 名称
        item['name'] = response.xpath('//div[@class="content-wrapper"]//h1/text()').extract_first()

        # 地位信息板块
        overviewInfo = response.xpath('//div[@class="overview"]/div[2]')

        # 租金
        rentalPrice = overviewInfo.xpath('./div[@class="price "]//text()').extract()
        item['rentalPrice'] = "".join(i.strip() for i in rentalPrice if len(i.strip()) > 0)
        # 面积
        item['area'] = "".join(overviewInfo.xpath('./div[@class="zf-room"]/p[1]//text()').extract())
        # 几室几厅
        item['type'] = "".join(overviewInfo.xpath('./div[@class="zf-room"]/p[2]//text()').extract())
        # 楼层
        item['floor'] = "".join(overviewInfo.xpath('./div[@class="zf-room"]/p[3]//text()').extract())
        # 朝向
        item['orientation'] = "".join(overviewInfo.xpath('./div[@class="zf-room"]/p[4]//text()').extract())
        # 地铁
        item['subway'] = "".join(overviewInfo.xpath('./div[@class="zf-room"]/p[5]//text()').extract())

        # 小区
        parkInfo = overviewInfo.xpath('./div[@class="zf-room"]/p[6]//text()').extract()
        item['parkInfo'] = "".join(i.strip() for i in parkInfo if len(i.strip()) > 0)
        # 地址
        item['address'] = "".join(overviewInfo.xpath('./div[@class="zf-room"]/p[7]//text()').extract())
        # 发布时间
        item['publishTime'] = "".join(overviewInfo.xpath('./div[@class="zf-room"]/p[8]//text()').extract())

        # 房源特色
        feature = response.xpath('//div[@class="featureContent"]//li//text()').extract()
        feature = [i.strip().replace("：", "") for i in feature if len(i.strip()) > 0]
        item['feature'] = {feature[i]: feature[i + 1] for i in range(len(feature) - 1) if i % 2 == 0}
        print(item)
        yield item

    def error_back(self, e):
        """
        报错机制
        """
        self.logger.error(format_exc())
