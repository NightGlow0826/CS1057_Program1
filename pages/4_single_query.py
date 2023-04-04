#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : 4_single_query.py
@Author  : Gan Yuyang
@Time    : 2023/4/1 21:08
"""
import random
import re

import akshare as ak
import pandas as pd
import requests
import streamlit as st
from fake_useragent import UserAgent
from streamlit_echarts import st_pyecharts
from stock_info import StockInfo, code2cn_name
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

sto = StockInfo(headless=True, simulate=False)


def view(cnname):
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
    rep = requests.get(f'https://xueqiu.com/k?q={name}', headers=headers)
    rep.encoding = 'utf-8'
    # print(rep.url)
    key = re.findall(pattern=r'k?(q=.*)', string=rep.url)[0]
    b = f'https://xueqiu.com/query/v1/search/status.json?sortId=1&{key}&count=20&page=1'
    info = requests.get(b, headers=headers)
    info.encoding = 'utf-8'
    content = info.text
    # with open('1.txt', 'w+', encoding='utf-8') as f:
    #     f.write(content)
    # with open('1.txt', 'r+', encoding='utf-8') as f:
    #     content = f.read()

    # 去除超链接, 图片链接
    content = re.sub(r'<a.*?>', '', content)
    content = re.sub(r'<\a>', '', content)
    content = re.sub(r'<img.*?>', '', content)
    content = re.sub(r'<br/>+', '<br/>', content)
    content = re.sub(r'网页链接', '<br/>', content)
    text_part = re.findall(r'"text":"(.*?)"', content)
    title_part = re.findall(r'"title":"(.*?)"', content)
    for text, title in zip(text_part, title_part):
        # st.subheader('q')
        pos = text_part.index(text)
        # print(len(text))
        with st.expander(f'View #{pos + 1},\t Possible len: {len(text)}', expanded=pos < 3):
            components.html(title, height=30)
            components.html(text, height=max(min(len(text) / 2, 450), 40), scrolling=True)


def single_query():
    st.header('Single Share Query')
    with st.form(key='form_query', ):
        c1, c2 = st.columns(2)

        code = c1.text_input(
            label='input a code',
            value='601318',
            key='placeholder'
        )
        option = c2.selectbox('Previous Length', (120, 15, 30, 60, 240, 360, 720))
        col1, col2 = st.columns(2)
        submission_button = col1.form_submit_button(label='Start')
        luck_button = col2.form_submit_button(label='Luck')

        if submission_button:
            try:
                st.info(f'Drawing {code2cn_name(code)}: {code} ...')
            except IndexError:
                st.error(f'Your code is not valid')
            # st_pyecharts(sto.draw_single(code, previous=50, render=False))
            components.html(sto.draw_single(code, previous=option, render=False).render_embed(), height=600, width=1200)
            st.success('GOOD LUCK')
            view(code2cn_name(code))
        elif luck_button:
            a = ak.stock_info_a_code_name()
            a = a['code'].tolist()
            st.info('Choosing A Lucky Number ...')
            for i in range(42):
                luck = random.sample(a, 1)[0]
                try:
                    code2cn_name(luck)
                except Exception:
                    if i % 6 == 0:
                        st.error("luck dosen't work this time")
                    continue

                try:
                    st.info(f'Drawing {code2cn_name(luck)}: {luck} ...')
                    break
                except Exception:
                    # st.write(f'Your code is not valid')
                    st.warning(f'This stock {code2cn_name(luck)}: {luck} stopped selling/Trading')

            components.html(sto.draw_single(luck, previous=120, render=False).render_embed(), height=600, width=1200)
            view(code2cn_name(luck))
            a1, a2 = st.columns(2)
            a1.success('GOOD LUCK')
            a2.code(luck)


if __name__ == '__main__':
    single_query()