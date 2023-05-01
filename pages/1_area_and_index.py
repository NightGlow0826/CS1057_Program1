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

import args
from stock_info import StockInfo
import streamlit.components.v1 as components
import json
st.set_page_config(layout="wide")

sto = StockInfo(headless=True, simulate=False)


@st.cache_data
def area_init(update=False):
    if not update:
        with open(r'basic_html/area_distribution.html', 'r', encoding='utf-8') as f:
            return f.read()

    return sto.area_df


def area_and_index(update=False):

    a, b = st.columns(2)
    with a:
        st.header('Area Distribution')
        if not update:
            components.html(area_init(), height=500, width=1000,
                            scrolling=False)
        else:
            components.html(sto.draw_area_chart(render=False, df=area_init(update)).render_embed(), height=500, width=1000,
                            scrolling=False)
    with b:
        with st.form(key='Index'):
            st.header('Index Query')
            c1, c2 = st.columns(2)

            choice = c1.selectbox('Index', zip(args.index_name, args.index_code))
            option = c2.selectbox('Segment', ('day', 'week','month', 'quarter'))

            sumb = st.form_submit_button('Draw')
            if sumb:
                st.info(f'Draw {choice} ')
                components.html(sto.draw_single(index=True, symbol=choice[1],seg=option, render=False).render_embed(), height=600, width=1200)

if __name__ == '__main__':
    area_and_index()
