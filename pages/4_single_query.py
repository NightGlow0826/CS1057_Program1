#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : 4_single_query.py
@Author  : Gan Yuyang
@Time    : 2023/4/1 21:08
"""
import random
import akshare as ak
import pandas as pd
import streamlit as st
from streamlit_echarts import st_pyecharts
from stock_info import StockInfo
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

sto = StockInfo(headless=True)


def single_query():
    st.header('Single Share Query')
    with st.form(key='form_query', ):
        c1, c2 = st.columns(2)

        code = c1.text_input(
            label='input a code',
            value='601318',
            key='placeholder'
        )
        option = c2.selectbox('Previous Length', (120, 15, 30, 60))
        col1, col2 = st.columns(2)
        submission_button = col1.form_submit_button(label='Start')
        luck_button = col2.form_submit_button(label='Luck')

        if submission_button:
            try:
                st.info(f'Drawing {sto.code2cn_name(code)}:{code} ...')
            except IndexError:
                st.error(f'Your code is not valid')
            # st_pyecharts(sto.draw_single(code, previous=50, render=False))
            components.html(sto.draw_single(code, previous=option, render=False).render_embed(), height=600, width=1200)
            st.success('GOOD LUCK')
        elif luck_button:
            a = ak.stock_info_a_code_name()
            a = a['code'].tolist()
            st.info('Choosing A Lucky Number ...')
            for i in range(42):
                luck = random.sample(a, 1)[0]
                try:
                    sto.code2cn_name(luck)
                except Exception:
                    if i % 6 == 0:
                        st.error("luck dosen't work this time")
                    continue

                try:
                    st.info(f'Drawing {sto.code2cn_name(luck)}:{luck} ...')
                    break
                except Exception:
                    # st.write(f'Your code is not valid')
                    st.warning(f'This stock {sto.code2cn_name(luck)}: {luck} stopped selling/Trading')

            # st_pyecharts(sto.draw_single(code, previous=50, render=False))
            components.html(sto.draw_single(luck, previous=120, render=False).render_embed(), height=600, width=1200)
            a1, a2 = st.columns(2)
            a1.success('GOOD LUCK')
            a2.code(luck)

if __name__ == '__main__':
    single_query()