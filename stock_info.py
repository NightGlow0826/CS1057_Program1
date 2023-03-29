#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : stock_info.py
@Author  : Gan Yuyang
@Time    : 2023/3/27 18:09
"""
import re

import bs4
import pandas as pd
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import args

from pyecharts import options as opts
from pyecharts.charts import Map, Page, Bar

class StockInfo:
    def __init__(self, headless=False):
        self.area_classify_link = r'http://www.sse.com.cn/assortment/stock/areatrade/area/'
        self.industry_classify_link = r'http://www.sse.com.cn/assortment/stock/areatrade/trade/'
        self.specified_industry_base = r'http://www.sse.com.cn/assortment/stock/areatrade/trade/detail.shtml?csrcCode='

        self.driver = args.Driver(headless=headless).blank_driver

    @property
    def area_df(self):
        """
        This func aims to get the area data (for drawing the stocks nums of each province)
        :return: area df
        """

        area_df = pd.DataFrame(columns=['area', 'A', 'AB', 'B'])

        # rep = requests.get(self.area_classify_link, headers=args.headers_area)
        # rep.encoding = 'utf-8'
        # text = rep.text
        # text = repr(text).replace(r'\n', '').replace(r'\t', '').replace(' ', '').replace(r'\r', '').replace(r'\\', '')
        #
        # with open('dust/1.txt', 'w+', encoding='utf-8') as f:
        #     f.write(text)

        with open('dust/1.txt', 'r', encoding='utf-8') as f:
            rep = f.read()
            t = re.findall(r"\[\\'<atarget.*?]", rep)
        for item in t:
            # print(item)
            area = re.findall('>(.*?)<', item)[0]
            digits = re.findall(r"'(\d*?)\\", item)
            digits = [int(i) for i in digits]
            # print(digits)
            a, ab, b = digits[:]
            # print(area, a, ab, b)
            # quit()
            area_df.loc[t.index(item)] = area, a, ab, b
        return area_df

    @property
    def area_chart(self):
        province = list(self.area_df['area'])
        A_shares = list(self.area_df['A'])
        for i in range(len(province)):
            if province[i] in ['北京', '重庆', '天津', '上海']:
                province[i] = province[i] + '市'
            elif province[i] in ['内蒙古', '西藏']:
                province[i] = province[i] + '自治区'
            elif province[i] in ['新疆']:
                province[i] = province[i] + '维吾尔自治区'
            elif province[i] in ['宁夏']:
                province[i] = province[i] + '回族自治区'
            elif province[i] in ['广西']:
                province[i] = province[i] + '壮族自治区'
            else:
                province[i] = province[i] + '省'
        c = (
            # Map(init_opts=opts.InitOpts(width='1500px', height='900px'))
            Map()
                .add("A股发行数量", [list(z) for z in zip(province, A_shares)], "china",
                     is_map_symbol_show=False)
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="A股各省份发行数量", is_show=True),
                visualmap_opts=opts.VisualMapOpts(max_=300, is_show=True, pos_left='300', pos_bottom='60'),

            )

                .render("A_share released.html")
        )  # render 后c成为路径字符串, 不render则是Map()

        return c

    def cover_maker(self):
        page = Page(layout=Page.DraggablePageLayout)
        page.add(s.area_chart, s.area_chart)
        # page.render('temp.html')
        # quit()

        # page.save_resize_html("temp.html",
        #                       cfg_file="cover_config.json",
        #                       dest="cover.html")

    @property
    def rough_industry_df(self):
        rough_industry_df = pd.DataFrame(
            columns=['href', 'rough_industry', 'industry_code', 'share_num', 'total_value', 'ave_pe', 'ave_price'])

        # self.driver().get(self.industry_classify_link)
        # page_source= self.driver().page_source
        # with open('trade.html', 'w+', encoding='utf-8') as f:
        #     f.write(page_source)
        # quit()
        with open('trade.html', 'r+', encoding='utf-8') as f:
            bs = bs4.BeautifulSoup(f, 'lxml')
        t = bs.find("div", {"class": "sse_colContent js_tradeClassification"})
        t = t.find("script")
        text = repr(str(t)).replace(r'\n', '').replace(r'\t', '').replace(' ', '').replace(r'\r', '')
        l = re.findall(r"\[\\'<ahref.*?]", text)
        for item in l:
            href = r'http://www.sse.com.cn' + re.findall(r'"(.*?)"', item)[0]
            rough_industry = re.findall(r'>(.*?)</a', item)[0]
            industry_code = href[-1]
            digits = re.findall(r"'([\d|\.|\-]*?)\\", item)
            digits = [float(i.replace('-', '0')) for i in digits]
            # print(item)
            share_num, total_value, ave_pe, ave_prive = digits[:]
            rough_industry_df.loc[
                l.index(item)] = href, rough_industry, industry_code, share_num, total_value, ave_pe, ave_prive

        return rough_industry_df

    @property
    def rough_chart(self):
        rough_df = self.rough_industry_df
        c = (
            Bar()
                .add_xaxis(list(rough_df['rough_industry']))
                .add_yaxis("总股数", list(rough_df['share_num']))
                .add_yaxis("总市值(千亿)", list(round(rough_df['total_value'] / 1e11, 2)))
                .add_yaxis("市盈率", list(rough_df['ave_pe']))
                .add_yaxis("平均股价", list(rough_df['ave_price']))
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="大致分类"),
                                 xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-60)),
                                 datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
                                 )
                .render("rough_chart.html")
        )
        return c

    def fine_classify(self):
        # self.driver.get(self.industry_classify_link)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, r'/html/body/div[9]/div/div[2]/div/div[1]/div[1]/table/tbody[2]/tr[1]/td[2]')))
        # page_source = self.driver.page_source
        # with open('fine.html', 'w+', encoding='utf-8') as f:
        #     f.write(page_source)
        with open('fine.html', 'r+', encoding='utf-8') as f:
            h = f.read()

            bs = bs4.BeautifulSoup(h, 'lxml')
            main = bs.find_all('div', {"class": "table-responsive"})[0]

        l = main.find_all_next('tr')[1:]
        #     l 的第一个元素是总结
        print(l)



    def test(self):
        pass



    def code_select(self):
        pass


s = StockInfo(headless=True)
s.fine_classify()
# page = Page(layout=Page.DraggablePageLayout)
# page.add(s.area_chart)
# page.render('temp.html')
