from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
from io import BytesIO
from PIL import Image

'''
browser = webdriver.Chrome()
browser.get('https://user.mbaex.com/#/login')
time.sleep(3)
wait = WebDriverWait(browser, 20)
test = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_radar_tip_content')))
if test:
    print('找到节点')
    test.click()
else:
    print('节点未找到')

time.sleep(2)

browser.execute_script('document.getElementsByClassName("geetest_canvas_fullbg")[0].style="display: block;"')

user_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name=Login_username]')))

if user_input:
    user_input.send_keys('233')
else:
    print('节点路径错误')

img = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_slice'))
        )
if img:
    print(img.size)
    print(img.location)
'''





username = 'username@163.com'
password = 'password'


class mbaex(object):
    """
    滑动验证码练习
    """
    def __init__(self):
        self.full = 1
        self.user = username
        self.pwd = password
        self.browser = webdriver.Firefox()
        self.wait = WebDriverWait(self.browser, 20)
        self.browser.get('https://user.mbaex.com/#/login')

    def log_in(self):
        #找到用户名框
        user_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name=Login_username]')))
        #找到密码框
        pwd_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name=Login_password]')))
        user_input.send_keys(self.user)
        pwd_input.send_keys(self.pwd)

    def login_btn(self):
        btn = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_radar_tip_content')))
        return btn

    def get_position(self):
        img = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.geetest_canvas_img')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right =  location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width'] 
        return top, bottom, left, right

    def get_screen_shot(self):
        if self.full > 0:
            self.browser.execute_script('document.getElementsByClassName("geetest_canvas_fullbg")[0].style="display: block;"') 
            self.full = -1
        else:
            self.browser.execute_script('document.getElementsByClassName("geetest_canvas_fullbg")[0].style="display: none;"')
        screen_shot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screen_shot))
        return screenshot
        
    def get_geetest_image(self, name='captcha.png'):
        top, bottom, left, right = self.get_position()
        print('验证码位置:', top, bottom, left, bottom)
        screenshot = self.get_screen_shot()
        time.sleep(1)
        captcha = screenshot.crop((left, top, right, bottom))
        return captcha

    def is_pixel_equal(self, image1, image2, x, y):
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        result1 = abs(pixel1[0] - pixel2[0])
        result2 = abs(pixel1[1] - pixel2[1])
        result3 = abs(pixel1[2] - pixel2[2])
        if result1 < threshold and result2 < threshold and result3 < threshold:
            return True
        else:
            return False

    def get_gap(self, image1, image2):
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i , j):
                    left = i
                    return left
        return left
    
    def get_track(self, distance):
        track = []
        current = 0
        mid = distance * 4/5
        t = 0.2
        v = 0

        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3

            v0 = v
            v = v0 + a * t
            move = v0 * t + 1/2 * a * t * t
            current += move
            track.append(round(move))
        return track

    def move_to_gap(self, slider, track):
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(1)
        ActionChains(self.browser).release().perform()

    def get_slider(self):
        slider = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def crack(self):
        self.log_in()
        btn = self.login_btn()
        btn.click()
        time.sleep(2)
        image1 = self.get_geetest_image('tupian1.png')
        image2 = self.get_geetest_image('tupian2.png')
        gap = self.get_gap(image1, image2)
        print(gap)


if __name__ == '__main__':
    geetest = mbaex()
    geetest.crack()



#user = mbaex()
#user.log_in()
#btn = user.login_btn()
#btn.click()
#time.sleep(2)
#image1 = user.get_geetest_image('tupian1.png')
#image2 = user.get_geetest_image('tupian2.png')
