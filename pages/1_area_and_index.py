#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : 1_area_and_index.py
@Author  : Gan Yuyang
@Time    : 2023/4/1 20:24
"""
# from webui import *
import os.path
import time
import random

import streamlit as st
from streamlit_echarts import st_pyecharts
from stock_info import StockInfo
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

sto = StockInfo(headless=True, simulate=False)


@st.cache_data
def area_init(update=False):
    if not update:
        with open(r'basic_html/area_distribution.html', 'r', encoding='utf-8') as f:
            return f.read()

    return sto.area_df


def area_and_index(update=False):
    col1, col2 = st.columns(2)

    with col1:
        st.header('Area Distribution')
        if not update:
            components.html(area_init(), height=500, width=1000,
                            scrolling=False)
        else:
            components.html(sto.draw_area_chart(render=False, df=area_init(update)).render_embed(), height=500, width=1000,
                            scrolling=False)
    with col2:
        with st.form(key='Index'):
            st.header('Index Query')
            c1, c2 = st.columns(2)

            choice = c1.selectbox('Index', ('sh000001: 上证指数', 'sh000016: 上证50', 'sh000017: 新综指'))
            option = c2.selectbox('Previous Length (Year)', (1, 2, 3))
            name_dict = {'sh000001: 上证指数': 'sh000001', 'sh000016: 上证50': 'sh000016',
                         'sh000017: 新综指': 'sh000017', }
            code = name_dict.get(choice)
            sumb = st.form_submit_button('Draw')
            if sumb:
                st.info(f'Draw {choice} ')
                st_pyecharts(sto.draw_index(code, render=False, previous=option * 365))


if __name__ == '__main__':
    area_and_index()
