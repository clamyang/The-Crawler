# 使用BeautifulSoup解析页面，并使用文档保存下来
from bs4 import BeautifulSoup
import requests

# 获取页面信息
def get_info(url):
    try:
        headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
                }

        html = requests.get(url, headers=headers)
        if html.status_code == 200:
            return html.content
        return None

    except:
        return None

# 解析页面信息
def parse_html(html):
    soup = BeautifulSoup(html)

    all_list = soup.find('dl', class_="board-wrapper")
    items = all_list.find_all('dd')
    name_list = []

    for item in items:
        movie_info = item.find('div', class_="movie-item-info")
        movie_name = movie_info.find('p', class_="name").string
        #movie_actors = movie_info.find('p', class_="star").string
        #movie_time = movie_info.find('p', class_="releasetime").string

        name_list.append(movie_name)
    return name_list

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_info(url)
    movies = parse_html(html)
    with open('demo.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(movies))
    #print('\n'.join(movies))

if __name__ == '__main__':
    for i in range(0,10):
        main(offset=i * 10)

'''
实现翻页功能时，因为下一页的每一个class属性都不一样无法定位，或者定位比较繁琐，观察url发现，每一叶只有最后一个参数不同，所以我们只需构造一个url每次传入最后一个参数，一个参数代代表一个页面。使用for循环迭代
'''
