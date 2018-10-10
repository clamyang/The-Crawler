import requests
import csv
from pyquery import PyQuery as pq

url = 'https://www.zhihu.com/explore'
headers = {
       'User-Agent' : 'ser-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }

html = requests.get(url, headers=headers).text
doc = pq(html)
items = doc('.explore-tab .feed-item').items()

with open('explore.csv', 'a', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['question', 'anthor', 'answer'])

    for item in items:
        question = item.find('h2').text()
        author = item.find('.author-link-line').text()
        answer = pq(item.find('.content').html()).text()

        writer.writerow([question, author, answer])
            
