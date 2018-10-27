from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import time

browser = webdriver.Chrome()
browser.get('https://weibo.com/6018279722/GEB5H5OYh?type=repost')
wait = WebDriverWait(browser, 10)

def get_page():
    try:
        #确保页面全部加载出来
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.repeat_list div.list_ul .list_li')))
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'div.W_pages a.page.next.S_txt1 > span'), '下一页'))

        parse_page() 

        #实现翻页功能
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.W_pages a.page.next.S_txt1 > span')))
        button.click()

    except TimeoutException:
        print("超时了！")

def parse_page():
    #解析页面，获取用户昵称
    html = browser.page_source
    doc = pq(html)
    items = doc('.list_ul .list_li').items()
    with open('name.txt', 'a+', encoding='utf-8') as f:
        for item in items:
            name = item.find('.WB_text a').text()
            f.write('\n'+ name+ '\n')

def main():
    for i in range(1,233):
        print('正在采集第%d页' % i)
        get_page()
        time.sleep(0.5)

if __name__=='__main__':
    main()

