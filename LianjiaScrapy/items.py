# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaNewItem(scrapy.Item):

    name = scrapy.Field()             # 名字
    url = scrapy.Field()              # url
    city = scrapy.Field()             # 城市
    region = scrapy.Field()           # 区域
    address = scrapy.Field()          # 地址
    price = scrapy.Field()            # 价格
    houseInfo = scrapy.Field()        # 房屋信息
    typeInfo = scrapy.Field()         # 户型介绍
    saleAddress = scrapy.Field()      # 售楼处地址
    developer = scrapy.Field()        # 开发商
    openTime = scrapy.Field()         # 最新开盘
    property = scrapy.Field()         # 物业类型


class LianjiaErshoufangItem(scrapy.Item):

    id = scrapy.Field()               # 链家编号
    name = scrapy.Field()             # 名字
    url = scrapy.Field()              # url
    city = scrapy.Field()             # 城市
    region = scrapy.Field()           # 区域
    address = scrapy.Field()          # 地址
    price_total = scrapy.Field()      # 总价
    price_per = scrapy.Field()        # 单价
    houseInfo = scrapy.Field()        # 房屋信息
    BaseInfo = scrapy.Field()         # 基础信息
    transactionInfo = scrapy.Field()  # 交易属性
    feature = scrapy.Field()          # 房源特色
    Position = scrapy.Field()         # 经纬度信息


class LianjiaZufangItem(scrapy.Item):

    id = scrapy.Field()              # 链家编号
    city = scrapy.Field()            # 城市
    url = scrapy.Field()             # url
    region = scrapy.Field()          # 行政分区
    name = scrapy.Field()            # 名称
    rentalPrice = scrapy.Field()     # 租金
    area = scrapy.Field()            # 面积
    type = scrapy.Field()            # 几室几厅
    floor = scrapy.Field()           # 楼层
    orientation = scrapy.Field()     # 朝向
    subway = scrapy.Field()          # 地铁
    parkInfo = scrapy.Field()        # 小区
    address = scrapy.Field()         # 地址
    publishTime = scrapy.Field()     # 发布时间
    feature = scrapy.Field()         # 房源特色

