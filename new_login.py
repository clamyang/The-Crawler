from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains

url = 'https://chushou.tv/'
user = ['15604467713', '19916025449']
pwd = '123456.q'

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

def get_button_change_frame(url, user, pwd):
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.cs_right a#chushou_login')))
    button.click()
    browser.switch_to.frame('G_login_layer')


    input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.login_right_center div.login_info input#login_phone_text')))
    password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.login_right_center div.login_info input#login_phone_password')))
    
    input.send_keys(user)
    password.send_keys(pwd)
    denglu = wait.until(EC.element_to_be_clickable((By.ID, 'login_btn')))
    denglu.click()


def new_window(url, user, pwd):
    range_num = list(range(1,11))
    browser.get('https://chushou.tv/')
    get_button_change_frame(url, user[0], pwd)
    for i in range_num:
        browser.execute_script('window.open()')
        browser.switch_to_window(browser.window_handles[i])
        browser.get('https://chushou.tv/')
        tuichu_user()

def tuichu_user():

    image = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.cs_user_avatar')))

    ActionChains(browser).move_to_element(image).perform()

    tuichu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.loginOutBtn')))
    tuichu.click()



new_window(url, user, pwd)


 
