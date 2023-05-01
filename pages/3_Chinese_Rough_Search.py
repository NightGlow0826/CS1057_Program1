#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : 3_Chinese_Rough_Search.py
@Author  : Gan Yuyang
@Time    : 2023/4/1 20:58
"""
import ast
import csv
import os.path
import re
import time
import random
import pandas as pd
import requests
import streamlit as st
from fake_useragent import UserAgent
from st_aggrid import AgGrid
from streamlit_echarts import st_pyecharts

import args
from stock_info import StockInfo
import streamlit.components.v1 as components

# st.session_state.update(st.session_state)
st.set_page_config(layout="wide")
sto = StockInfo(headless=True, simulate=False)


def zh_search(cnname):
    ua = UserAgent()
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "device_id=3897773bcfd6ac931684ef9745b97bde; acw_tc=276077a616805830147003852e67ec7e87743933759568c38d82ba8e719830; xq_a_token=ed22783ba339eb1ffc67ec307758bcb3a61b82dd; xqat=ed22783ba339eb1ffc67ec307758bcb3a61b82dd; xq_r_token=8c8e9c78536d2e07227d66416144fd494874bda0; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTY4MjU1NTI0MywiY3RtIjoxNjgwNTgyOTc2MzAzLCJjaWQiOiJkOWQwbjRBWnVwIn0.D6eiGf2Iejys0so29w7GMgUfr2fzec77tT0TyzEKIuQjgoytMLDlodsf-TORWKUPEOgOhrHttxV6QCZilkDGf3kPNdO0yqN4eiUl3XDUasDmeo2Vub1Jdvw9qHxzwW39bfOoA7wl9e-rAZL3qAp8unVa17YKR3tsms7VnJojDBdfDDgVZ5eJCqIsBH8O3oNSDna_VYy5mm-zn3-5I0U_EU97nIXE_6W_Ox378LEEtHYYTjOtrE9M2WNechH7v5oOehDFsxZAxhdkbp-ZLQNFelExDOc1a1UwsjVWFCm7NnYJN90otuaqQjfufKXc5D635onUUd4Dtd-AgouV25CRUA; u=421680583014707",
        "Host": "xueqiu.com",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": ua.random
    }
    name = cnname
    session = args.snowball_session()
    rep = session.get(f'https://xueqiu.com/k?q={name}', headers=headers)
    rep.encoding = 'utf-8'
    # print(rep.url)
    key = re.findall(pattern=r'k?(q=.*)', string=rep.url)[0]
    b = f'https://xueqiu.com/query/v1/search/web/stock.json?{key}&size=3&page=1'
    info = session.get(b, headers=headers).text
    body = re.findall(r'\[(.*?)]', info)[0]
    lst = re.findall(r'\{.*?}', body)
    lst = [ast.literal_eval(i) for i in lst]
    df = pd.DataFrame(lst)
    if df.empty:
        st.error('Too far from a exist stock')
        quit()
    return df[['name', 'code', 'exchange', 'trade_status', 'current']]


def show():
    # with st.form(key='select'):
        name = st.text_input('Input the rough Chinese name of the stock')
        while not name:
            time.sleep(2)

        data = zh_search(name)
        data.to_clipboard()
        path = r'./rough_query.csv'
        if not os.path.exists(path):
            with open(path, 'w+', encoding='utf-8'):

                pass
        data.to_csv(path, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC)
        # st.write(data)
        AgGrid(data, editable=True, fit_columns_on_grid_load=True, )
        st.success('This table is copied to your clipboard')


if __name__ == '__main__':
    show()
