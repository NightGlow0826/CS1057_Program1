#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : args.py
@Author  : Gan Yuyang
@Time    : 2023/3/27 18:43
"""
import selenium
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from fake_useragent import UserAgent
ua = UserAgent()
# import selenium.webdriver.

headers_area = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "max-age=0",
    "Cookie": "ba17301551dcbaf9_gdp_user_key=; gdp_user_id=gioenc-76d7e0a6%2C625a%2C5a87%2C9a88%2C4ag954951g11; "
              "ba17301551dcbaf9_gdp_session_id_75ef1155-7b30-4fb3-8a6d-4dd9d85b6e42=true; "
              "VISITED_MENU=%5B%228765%22%5D; home-search-scroll=; "
              "VISITED_COMPANY_CODE=%5B%22600000%22%2C%22600028%22%2C%22600097%22%5D; "
              "VISITED_STOCK_CODE=%5B%22600000%22%2C%22600028%22%2C%22600097%22%5D; "
              "seecookie=%5B600000%5D%3A%u6D66%u53D1%u94F6%u884C%2C%5B600028%5D%3A%u4E2D%u56FD%u77F3%u5316%2C"
              "%5B600097%5D%3A%u5F00%u521B%u56FD%u9645; sseMenuSpecial=8534; "
              "ba17301551dcbaf9_gdp_session_id=8897b8d6-49cf-4962-8ebf-2582cf2b8f50; "
              "ba17301551dcbaf9_gdp_session_id_8897b8d6-49cf-4962-8ebf-2582cf2b8f50=true; "
              "VISITED_MENU=%5B%228765%22%2C%228535%22%5D; ba17301551dcbaf9_gdp_sequence_ids={"
              "%22globalKey%22:205%2C%22VISIT%22:3%2C%22PAGE%22:40%2C%22VIEW_CLICK%22:158%2C%22VIEW_CHANGE%22:7}",
    "Host": "www.sse.com.cn",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://www.sse.com.cn/assortment/stock/areatrade/trade/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Mobile Safari/537.36 Edg/111.0.1661.54",
}

headers_trade = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "max-age=0",
    "Cookie": "ba17301551dcbaf9_gdp_user_key=; gdp_user_id=gioenc-76d7e0a6%2C625a%2C5a87%2C9a88%2C4ag954951g11; "
              "ba17301551dcbaf9_gdp_session_id_75ef1155-7b30-4fb3-8a6d-4dd9d85b6e42=true; "
              "VISITED_MENU=%5B%228765%22%5D; home-search-scroll=; "
              "VISITED_COMPANY_CODE=%5B%22600000%22%2C%22600028%22%2C%22600097%22%5D; "
              "VISITED_STOCK_CODE=%5B%22600000%22%2C%22600028%22%2C%22600097%22%5D; "
              "seecookie=%5B600000%5D%3A%u6D66%u53D1%u94F6%u884C%2C%5B600028%5D%3A%u4E2D%u56FD%u77F3%u5316%2C"
              "%5B600097%5D%3A%u5F00%u521B%u56FD%u9645; sseMenuSpecial=8534; "
              "ba17301551dcbaf9_gdp_session_id_8897b8d6-49cf-4962-8ebf-2582cf2b8f50=true; "
              "ba17301551dcbaf9_gdp_session_id=d957072f-9f22-4ffc-a10f-facf884cd325; "
              "ba17301551dcbaf9_gdp_session_id_d957072f-9f22-4ffc-a10f-facf884cd325=true; "
              "ba17301551dcbaf9_gdp_sequence_ids={"
              "%22globalKey%22:224%2C%22VISIT%22:4%2C%22PAGE%22:47%2C%22VIEW_CLICK%22:169%2C%22VIEW_CHANGE%22:7}; "
              "VISITED_MENU=%5B%228765%22%2C%228536%22%5D",
    "Host": "www.sse.com.cn",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://www.sse.com.cn/assortment/stock/areatrade/area/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Mobile Safari/537.36 Edg/111.0.1661.54",
}

class Driver(object, ):
    def __init__(self, driver_path=r"D:\Python Projects\Webdriver\msedgedriver.exe", extension_path=None, proxies=None, headless=False):
        self.driver_path = driver_path
        self.ex_path = extension_path
        self.proxies = proxies
        self.headless = headless
    @property
    def blank_driver(self, mute=False):
        # 初始化selenium driver
        self.browser_option = webdriver.EdgeOptions()
        self.browser_option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser_option.add_experimental_option('excludeSwitches', ['ignore-certificate-errors'])

        self.browser_option.add_argument('--disable-gpu')
        self.browser_option.add_argument('--disable-javascript')
        self.browser_option.add_argument('--user-agent=' + ua.random)

        # mobileEmulation = {'deviceName': 'iPhone X'}
        # self.browser_option.add_experimental_option('mobileEmulation', mobileEmulation)

        self.browser_option.add_experimental_option("detach", True)
        self.browser_option.add_experimental_option("useAutomationExtension", False)
        if self.ex_path:
            self.browser_option.add_extension(self.ex_path)
        if self.proxies:
            self.browser_option.add_argument('--proxy-server=' + self.proxies)
        # self.browser_option.page_load_strategy = 'eager'

        preferences = {
            "webrtc.ip_handling_policy": "disable_non_proxied_udp",
            "webrtc.multiple_routes_enabled": False,
            "webrtc.nonproxied_udp_enabled": False,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        self.browser_option.add_experimental_option("prefs", preferences)

        prefs = {'profile.managed_default_content_settings.images': 2,
                 }
        self.browser_option.add_experimental_option('prefs', prefs)
        if self.headless:
            self.browser_option.add_argument('--headless=chrome') # 无头
        driver = webdriver.Edge(service=Service(self.driver_path),
                                     options=self.browser_option,
                                     )

        if not mute:
            print('driver initialized')

        return driver
