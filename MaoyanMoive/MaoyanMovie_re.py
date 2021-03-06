# 爬取猫眼电影

import time
import json
import requests
import re
from requests.exceptions import RequestException

# 获取第一页的信息
def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
                }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
# 解析页面 这里使用的是正则表达式 正则表达式可维护性不高，如果页面发生变化，就会失效
def parse_one_page(html):
    pattern = re.compile ('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a' 
          + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
          + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
                'index': item[0],
                'image': item[1],
                'title': item[2].strip(),
                'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
                'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
                'score': item[5].strip() + item[6].strip()
                }

# 使用文件保存数据
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+ '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)

