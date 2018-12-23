import json
import re
from .utils import get_page
from pyquery import PyQuery as pq


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies
       
#    def crawl_daili66(self, page_count=4):
#        """
#        获取代理66
#        :param page_count: 页码
#        :return: 代理
#        """
#        start_url = 'http://www.66ip.cn/{}.html'
#        urls = [start_url.format(page) for page in range(1, page_count + 1)]
#        for url in urls:
#            print('Crawling', url)
#            html = get_page(url)
#            if html:
#                doc = pq(html)
#                trs = doc('.containerbox table tr:gt(0)').items()
#                for tr in trs:
#                    ip = tr.find('td:nth-child(1)').text()
#                    port = tr.find('td:nth-child(2)').text()
#                    yield ':'.join([ip, port])
#

    def crawl_ip3366(self):
        for page in range(1, 4):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = get_page(start_url)
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address+':'+ port
                yield result.replace(' ', '')
