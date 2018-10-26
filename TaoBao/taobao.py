from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from urllib.parse import quote
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import pymongo

MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


# 登录淘宝的时候，需要身份验证，用自己的手机淘宝扫码登录即可。
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 18)
KEYWORD = 'iPad'


def get_page(page):
    print('正在爬取第%d页' % page)
    try:
        if page > 1:       
            input = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
            #等待以上两个节点加载出来
            input.clear()
            input.send_keys(page)
            button.click()
       
        # 确保商品信息全部加载出来
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'),
            str(page))) 
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item'))) 

        get_product()
    
    except TimeoutException:
        # 如果连接失败 重新连接
        get_page(page)
        print('正在重试')


def get_product():
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
                'image': item.find('.pic .img').attr('data-src'),
                'price': item.find('.price').text(),
                'deal': item.find('.deal-cnt').text(),
                'title':  item.find('.title').text(),
                'shop': item.find('.shop').text(),
                'location': item.find('.location').text()
                }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到MongoDB成功')
    except Exception:
            print('存储到MongoDB失败')

max_page = 101

def main():
    url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
    browser.get(url)
    for page in range(1, max_page):
        get_page(page)
    browser.close()

if __name__ == '__main__':
    main()
        

