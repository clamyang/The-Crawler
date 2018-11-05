from selenium import webdriver
from selenium.webdriver import ActionChains 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PIL import Image
from io import BytesIO
import time


NUMBER = 'user'
PASSWORD = 'password'
BORDER = 6



class Bilibili():
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login'
        self.browser = webdriver.Firefox()
        self.wait = WebDriverWait(self.browser, 20)
        self.user = NUMBER
        self.password = PASSWORD
    
    #def __del__(self):
    #   self.browser.close()

    def get_slider(self):
        slider = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gt_slider_knob')))
        return slider

    def get_position(self):
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gt_cut_fullbg')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return (top, bottom, left, right)
        
    def get_screenshot(self):
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_image(self, name='captcha.png'):
        top, bottom, left, right = self.get_position()
        print('验证码的位置是', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        print('jietuchenggong')
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
        return False
        
    def get_gap(self, image1, image2):
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left


    def move_to_picture(self, slider):
        ActionChains(self.browser).move_to_element(slider).perform()
    
    def get_track(self, distance):
        track = []
        #当前位移
        current = 0
        #减速
        mid = distance * 4/5
        #计算间隔
        t = 0.2
        #初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度
            v = v0 + a * t
            # 移动的距离
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            #round() 函数 四舍五入取整数
            track.append(round(move))
        return track


    def move_to_gap(self, slider, track):
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        ActionChains(self.browser).release().perform()

    def open_page(self):
        self.browser.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        email.send_keys(self.user)
        password.send_keys(self.password)

    def login(self):
        login_button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-login')))
        return login_button

    def crack(self):
        self.open_page()
        slider = self.get_slider()
        self.move_to_picture(slider)
        image1 = self.get_image('tupian1.png')
        slider.click()
        time.sleep(3)
        image2 = self.get_image('tupian2.png')
        gap = self.get_gap(image1, image2)
        gap -= BORDER
        print('缺口位置', gap)
        track = self.get_track(gap)
        print('滑动轨迹', track)
        self.move_to_gap(slider, track)
        if not self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'tips', '验证服务器错误，请刷新页面重试'))):
            self.crack()
        else:
            login_button = self.login()
            login_button.click()
            
        

if __name__ == '__main__':
    crack = Bilibili()
    crack.crack()
