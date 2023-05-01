#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : Financial_Index.py
@Author  : Gan Yuyang
@Time    : 2023/4/14 19:41
"""
import datetime
import json
import os
import time

import fake_useragent
import pandas as pd
import requests
from matplotlib import pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
import streamlit as st


def text_to_df(text, mode='abs'):
    a = json.loads(text)['data']['list']

    lst_of_dct = []
    mode_dct = {'abs': 0, 'relative': 1}
    for i in a:
        for feature in i.keys():
            i[feature] = i[feature] if type(i[feature]) != list else i[feature][mode_dct.get(mode)]
        lst_of_dct.append(i)

    df = pd.DataFrame(data=lst_of_dct)[::-1]
    suffixes = ['年报', '一季报', '三季报', '中报']
    replacements = ['4', '1', '3', '2']
    df.index = list(df['report_name'].apply(lambda x: x[:4] + '-' + replacements[suffixes.index(x[4:])]))
    df.drop(['report_date', 'ctime', 'report_name'], axis=1, inplace=True)
    # print(df.columns)
    return df


class Sheet():
    def __init__(self, code, round=4):
        self.code = code
        self.headers = {
            'User-Agent': fake_useragent.UserAgent().random,
            'origin': 'https://xueqiu.com',
            'referer': f'https://xueqiu.com/snowman/S/{code}/detail'
        }
        self.session = requests.Session()
        self.ecd = 'utf-8'
        self.session.get("https://xueqiu.com", headers=self.headers)

    def financial_index(self):
        url = f'https://stock.xueqiu.com/v5/stock/finance/cn' \
              fr'/indicator.json?symbol={self.code}&type=all&is_detail=true' \
              f'&count=180&timestamp={1000 * (int(time.mktime(time.strptime(f"{2023}-12-31", "%Y-%m-%d"))))}'

        resp = self.session.get(url, headers=self.headers)
        resp.encoding = 'utf-8'
        df_abs = text_to_df(resp.text, mode='abs')

        return df_abs


def draw():
    with st.form('sb'):

        code = st.text_input('code')
        code = str(code).strip()
        if code[:2] == '60' or code[:2] == '68':
            code = 'SH' + code
        else:
            code = 'SZ' + code
        opt = Sheet(code='SH600519').financial_index().columns
        mul_ind = st.multiselect(options=(opt), label='index')
        fsb = st.form_submit_button(label='Start')

        if fsb:
            df = Sheet(code=code).financial_index()
            lst = ['平均净资产收益率', '每股净利润', '每股经营现金流量', '基本每股收益', '资本公积', '未分配利润每股', '总资产利息支出比率', '净销售率', '毛销售率', '总收入',
                   '营业收入同比增长率', '归属于母公司的净利润', '归属于母公司的净利润同比增长率', '扣除非经常性损益后的归属于母公司的净利润', '扣除非经常性损益后的归属于母公司的净利润同比增长率',
                   '营业外收支净额',
                   '运营资本回报率', '资产负债率', '流动比率', '速动比率', '权益乘数', '权益比率', '股东权益', '经营活动产生的现金流量净额与负债总额之比', '存货周转天数',
                   '应收账款周转天数',
                   '应付账款周转天数', '现金循环周期', '营业周期', '总资本周转率', '存货周转率', '应收账款周转率', '应付账款周转率', '流动资产周转率', '固定资产周转率']
            st.line_chart(df[mul_ind])


if __name__ == '__main__':
    draw()
