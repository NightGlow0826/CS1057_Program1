#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : 3_industry_query.py
@Author  : Gan Yuyang
@Time    : 2023/4/1 20:58
"""
import os.path
import time
import random

import pandas as pd
import streamlit as st
from streamlit_echarts import st_pyecharts
from stock_info import StockInfo
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

sto = StockInfo(headless=True)

def industry():
    st.header('Classified Draw')
    fdf = sto.fine_industry_df
    cn_name = fdf.loc[:, 'industry'].tolist()
    ind_code = fdf.loc[:, 'industry_code'].tolist()
    with st.form(key='industry', ):

        l = [f'{i}: {j}' for i, j in zip(ind_code, cn_name)]
        c1, c2 = st.columns(2)
        options = c1.multiselect('Choose Some Industries', l)
        previous = int(c2.number_input('Previous', min_value=7, max_value=15))
        submission_button = st.form_submit_button(label='Start')
        st.info('This may takes a long time, especially if the computer/internet is not good.')

        # print(l)
        if submission_button:
            for ind in options:
                df = pd.read_csv(f'fine_field_csv_folder/{ind[:3]}.csv')
                # print(df)
                if len(df) <= 10:
                    pass
                st_pyecharts(sto.draw_industry(ind[:3], previous, render=False))

if __name__ == '__main__':
    industry()