# -*- coding: utf-8 -*-

import os
import scrapy
import time
from urllib import request
from LianJiaSpider.settings import headers
from LianJiaSpider.items import LianjiaspiderItem

# 首先我们看一下 urllib 中的一个函数
# urllib.request.url.urlretrieve()
# 这个函数的功能是将远程的数据下载下来并保存在本地
# 这个函数有两个参数
# 第一个传入你想抓取的链接
# 第二个传入你想保存在本地的位置

class LjspiderSpider(scrapy.Spider):
    name = 'LJSpider'
    allowed_domains = ['lianjia.com']

    def start_requests(self):
        # start_urls = []
        # for page in range(1,6):
        #     url = 'https://bj.lianjia.com/zufang/chaoyang/pg{}l1rp5'.format(page)
        #     start_urls.append(url)

        start_urls = [
            'https://bj.lianjia.com/zufang/chaoyang/pg1l1rp5',
            'https://bj.lianjia.com/zufang/haidian/pg2l1rp5'
        ]

        for start_url in start_urls:
            yield scrapy.Request(url=start_url, headers=headers, dont_filter=True, callback=self.parse)

    def parse(self, response):
        infos = response.xpath('//div[@class="content__list"]/div[@class="content__list--item"]')
        for info in infos:
            # 获取房屋标题名称
            house_titles = info.xpath('.//p[@class="content__list--item--title twoline"]/a/text()').extract()
            # 格式化标题
            house_title = house_titles[0].strip().replace(' ', '')
            # 获取房屋详情连接
            house_url = info.xpath('.//p[@class="content__list--item--title twoline"]/a/@href').extract_first()
            final_url = 'https://bj.lianjia.com' + house_url
            # 获取所处位置
            house_located = info.xpath('.//p[@class="content__list--item--des"]/a[2]/text()').extract_first()
            # meta 参数的作用是，传递信息给下一个函数。
            # 下一个想要使用被传递的信息需要使用 response.meta['key'] 来取值
            yield scrapy.Request(url=final_url, callback=self.detail_parse, headers=headers, dont_filter=True, meta={'house_title':house_title,'final_url':final_url,'house_located':house_located})

    def detail_parse(self, response):
        # 获取房屋详情信息
        infos = response.xpath('//div[@class="content clear w1150"]')
        for info in infos:
            # 获取房源详情编码
            house_code = info.xpath('.//i[@class="house_code"]/text()').extract_first()
            # 获取房子价格
            house_price = info.xpath('.//p[@class="content__aside--title"]/span/text()').extract_first() + ' 元/月'
            # 获取联系人名字
            contact_name = info.xpath('.//span[@class="contact_name"]/@title').extract_first()
            # 获取联系人电话信息
            phone_num = response.xpath('//div[@class="desc"]/div[@class="phone"]/text()').extract_first()
            # 租赁信息
            house_information = info.xpath('.//p[@class="content__article__table"]//span/text()').extract()
            # 租赁方式
            lease_way = house_information[0]
            # 厅室信息
            room_info = house_information[1]
            # 房子大小
            house_size = house_information[2]
            # 房子朝向
            house_direction = house_information[3]
            # 图片存放地址
            house_located = 'E:/test_1/LianJiaSpider/房屋图片/'
            element = response.meta['house_title']
            house_located = house_located + element

            item = LianjiaspiderItem()

            item['house_title'] = response.meta['house_title']
            item['final_url'] = response.meta['final_url']
            item['house_located'] = response.meta['house_located']
            item['house_code'] = house_code
            item['house_price'] = house_price
            item['contact_name'] = contact_name
            item['phone_num'] = phone_num
            item['lease_way'] = lease_way
            item['room_info'] = room_info
            item['house_size'] = house_size
            item['house_direction'] = house_direction
            item['house_located'] = house_located
            yield item


            # 图片下载
            # house_image_urls = info.xpath('.//div[@class="content__article__slide__item"]/img/@src').extract()
            # if len(house_image_urls) != 0:
            #     for download_url in house_image_urls:
            #         img_name = str(time.time()) + '.jpg'
            #         if not os.path.exists(house_located):
            #             os.makedirs(house_located)
            #
            #         # 如下函数会将远程的数据下载到本地
            #         # 第一个参数是 要请求的连接
            #         # 第二个参数是 要保存的位置
            #         request.urlretrieve(download_url, house_located + '/' +img_name)









