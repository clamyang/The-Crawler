import time
from multiprocessing import Process
from proxypool.api import app
from proxypool.getter import Getter
from proxypool.tester import Tester
from proxypool.db import RedisClient
from proxypool.setting import *


class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        """
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)
    
    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)
    
    def schedule_api(self):
        """
        开启API
        """
        app.run(API_HOST, API_PORT)
    
    def run(self):
        print('代理池开始运行')
        # 此处使用多进程，分别执行以下三个函数
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester, args=())
            tester_process.start()
        
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter, args=())
            getter_process.start()
        
        if API_ENABLED:
            api_process = Process(target=self.schedule_api, args=())
            api_process.start()
