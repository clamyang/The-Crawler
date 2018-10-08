import requests
from pyquery import PyQuery as pq

url = 'https://www.zhihu.com/explore'
headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }

html = requests.get(url, headers=headers).text
doc = pq(html)
# 遍历获取每一个热题
items = doc('.explore-tab .feed-item').items()
for item in items:
    question = item.find('h2').text()
    author = item.find('.author-link-line').text()
    answer = pq(item.find('.content').html()).text()
    with open('result.txt', 'a', encoding="utf-8") as f:
        f.write('\n'.join([question, author, answer]))
        f.write('\n' + '=' * 50 + '\n') 
