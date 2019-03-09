# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from openpyxl import Workbook

class LianjiaspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class LianjiaJsonPipeline(object):
    def __init__(self):
        self.file = open('lianjia.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # ensure_ascii=False 参数的设定，会输出中文
        str = json.dumps(dict(item), ensure_ascii=False)
        str = str + '\n'
        self.file.write(str)
        return item

    def close_spider(self, spider):
        self.file.close()


class LianjiaSpiderExcelPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['house_title', 'final_url', 'house_located', 'house_code', 'house_price', 'contact_name', 'phone_num', 'lease_way', 'room_info', 'house_size', 'house_direction',])

    def process_item(self, item, spider):
        line = [item['house_title'], item['final_url'], item['house_located'], item['house_code'], item['house_price'], item['contact_name'], item['phone_num'], item['lease_way'], item['room_info'], item['house_size'], item['house_direction'],]
        self.ws.append(line)
        self.wb.save('lianjia.xlsx')

        return item
