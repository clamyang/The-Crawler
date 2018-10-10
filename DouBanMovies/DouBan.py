import codecs
import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'http://movie.douban.com/top250/'


def get_info(url):
    """用于获取页面信息并返回"""

    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
        }
    resp = requests.get(url, headers=headers).content
    return resp

def parse_html(html):
    """解析获得页面信息，提取电影名所在标签"""
    soup = BeautifulSoup(html)

    movie_list = soup.find("ol", class_="grid_view")

    movie_name_list = []

    # 一层一层解析页面
    for movie_li in movie_list.find_all("li"):
        movie_div = movie_li.find("div", class_="hd")
        movie_name = movie_div.find("span", class_="title")
        movie_name_list.append(movie_name.string)


   #到下一页遍历电影名称
    next_page_url = soup.find("span", class_="next").find("a")
    if next_page_url:
        return movie_name_list, DOWNLOAD_URL + next_page_url['href']
    return movie_name_list, None

def main():
    url = DOWNLOAD_URL
    with codecs.open('movies', 'wb', encoding='utf-8') as fp:
        while url:
            html = get_info(url)
            movies, url = parse_html(html)
            fp.write('{movies}\n'.format(movies='\n'.join(movies)))


if __name__ == '__main__':
    main()
    

