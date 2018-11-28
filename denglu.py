from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

url = 'https://chushou.tv/'
user = '15962059810'
pwd = '123456.q'

browser.get(url)
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.cs_right a#chushou_login')))
if button:
    print('success')
button.click()

browser.switch_to.frame('G_login_layer')
input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.login_right_center div.login_info input#login_phone_text')))
if input:
    print('success')
password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.login_right_center div.login_info input#login_phone_password')))
if password:
    print('success')

input.send_keys(user)
password.send_keys(pwd)

denglu = wait.until(EC.element_to_be_clickable((By.ID, 'login_btn')))
if denglu:
    print('111111')
    denglu.click()



#input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#login_phone_text')))
#if input :
#    print('success')


browser.execute_script('window.open()')
browser.switch_to_window(browser.window_handles[1])
browser.get('https://chushou.tv/')

image = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.cs_user_avatar')))
if image:
    print('222')

ActionChains(browser).move_to_element(image).perform()

#browser.execute_script('document.getElementsByClassName("cs_nav_cont")[0].style="display: block;"')
tuichu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.loginOutBtn')))
tuichu.click()

button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.cs_right a#chushou_login')))
if button:
    print('success')
button.click()

browser.switch_to.frame('G_login_layer')
input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.login_right_center div.login_info input#login_phone_text')))
if input:
    print('success')
password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.login_right_center div.login_info input#login_phone_password')))
if password:
    print('success')

input.send_keys('19916025449')
password.send_keys('123456.q')

denglu = wait.until(EC.element_to_be_clickable((By.ID, 'login_btn')))
if denglu:
    print('111111')
    denglu.click()

browser.execute_script('window.open()')
browser.switch_to_window(browser.window_handles[2])
browser.get('https://chushou.tv/')

image = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.cs_user_avatar')))
if image:
    print('222')

ActionChains(browser).move_to_element(image).perform()

#browser.execute_script('document.getElementsByClassName("cs_nav_cont")[0].style="display: block;"')
tuichu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.loginOutBtn')))
tuichu.click()

button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.cs_right a#chushou_login')))
if button:
    print('success')
button.click()

browser.switch_to.frame('G_login_layer')
input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.login_right_center div.login_info input#login_phone_text')))
if input:
    print('success')
password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.login_right_center div.login_info input#login_phone_password')))
if password:
    print('success')

input.send_keys('19916025449')
password.send_keys('123456.q')

denglu = wait.until(EC.element_to_be_clickable((By.ID, 'login_btn')))
if denglu:
    print('111111')
    denglu.click()

