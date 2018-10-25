from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from urllib.parse import quote
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq


browser = webdriver.Chrome()
wait = WebDriverWait(browser, 18)
KEYWORD = 'iPad'

def get_page(page):
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url)
        if page > 1:
            
            input = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))

            button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form')))

            input.clear()
            input.send_keys(page)
            button.click()
       
       
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'),
            str(page)))
        
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        
        get_product()
    
    except TimeoutException:
        get_page(page)
        print('超时')


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


max_page = 101
def main():
    for page in range(1, 6):
        get_page(page)
    browser.close()
if __name__ == '__main__':
    main()
        

