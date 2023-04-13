#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : 2_macro_and_classification.py
@Author  : Gan Yuyang
@Time    : 2023/4/1 20:53
"""
import re
import time

import pandas as pd
import requests
import streamlit as st
from fake_useragent import UserAgent
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from streamlit_echarts import st_pyecharts
from streamlit_echarts import Map as st_Map
from tqdm import tqdm

import args
from stock_info import StockInfo
import json
import streamlit.components.v1 as components
import numpy as np

st.set_page_config(layout="wide")

sto = StockInfo(headless=True, simulate=False)


def macro_by_requests(previous=60):
    ua = UserAgent()
    headers = {
        'Referer': 'http://www.sse.com.cn/',

        'User-Agent': ua.random
    }
    session = requests.Session()
    session.get('http://www.sse.com.cn/', headers=headers)

    h_data_dict_list = []
    dl = sto.hist_date_list(previous=previous)
    my_bar = st.progress(0, text='Updating')

    for date in dl:
        print(date)
        my_bar.progress((dl.index(date) + 1) / len(dl), text=f':orange[{date}]')
        a = int(time.time() - 30) * 1000 - 100
        url = f'http://query.sse.com.cn/commonQuery.do?jsonCallBack=jsonpCallback32438768&sqlId=COMMON_SSE_SJ_GPSJ_CJGK_MRGK_C&PRODUCT_CODE=01%2C02%2C03%2C11%2C17&type=inParams&SEARCH_DATE={date}&_={a}'
        resp2 = session.get(url, headers=headers)
        resp2.encoding = args.encoding
        content = resp2.text
        content = re.findall(pattern=f'.*?\((.*?)\)', string=content)[0]
        try:
            content = json.loads(content)['result'][0]
            h_data_dict_list.append(content)
        except Exception:
            continue
        time.sleep(0.1)
    try:
        df = pd.DataFrame(data=h_data_dict_list, index=dl)
    except Exception:
        df = pd.DataFrame(data=h_data_dict_list, index=dl[:-1])

    df = df[
        ['TOTAL_VALUE', 'NEGO_VALUE', 'TRADE_VOL', 'TRADE_AMT', 'AVG_PE_RATE', 'TOTAL_TO_RATE', 'NEGO_TO_RATE', ]]
    df.to_csv('macro_hist.csv')
    st.success('Updated, Refresh to display')


def macro():
    st.header('A Share Historic Macro Data')
    # previous = st.slider('Previou_date', 3, 15, 7)

    st_pyecharts(sto.draw_macro(render=False, previous=45))

    with st.form(key='macro_update'):
        fsb = st.form_submit_button('Click to Update')
        if fsb:
            macro_by_requests(previous=60)


@st.cache_data
def get_rough_df():
    return sto.rough_industry_df


@st.cache_data
def get_fine_df():
    return sto.fine_industry_df


def classify():
    st.header('A Share Classification')
    # c1, c2 = st.columns(2)

    option = st.selectbox('Classification Degree', ('Rough', 'Fine'))
    df_1 = {'Rough': get_rough_df(), 'Fine': get_fine_df()}[option]
    st.info(f'Switching to {option} mode ...')
    st_pyecharts(sto.draw_classify_chart(df_1, render=False))


if __name__ == '__main__':
    macro()

    classify()
