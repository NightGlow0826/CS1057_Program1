#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : 5_favorite_shares.py
@Author  : Gan Yuyang
@Time    : 2023/4/1 21:13
"""
import os.path
import time
import random

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from streamlit_echarts import st_pyecharts
from streamlit_echarts import Map as st_Map
from stock_info import StockInfo, code2cn_name
import json
import streamlit.components.v1 as components
import numpy as np
import akshare as ak

st.set_page_config(layout="wide")
sto = StockInfo(headless=True, fine_update=False, simulate=False)


def favorit():
    path = r'./favorite.csv'
    if not os.path.exists(path):
        with open(path, 'w+', encoding='utf-8'):
            pass
    try:
        df = pd.read_csv(path, index_col=0)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=['code', 'name'])
        # df.loc['0'] = '601318', '中国平安'

    return df


def favorite_query():
    st.header('Favorite Quick Query')
    with st.form(key='fq'):
        data = favorit()
        c1, c2 = st.columns(2)

        code = c1.selectbox('Find One', zip(data['code'].tolist(), data['name'].tolist()))[0]
        p = c2.selectbox('Previous Length', (120, 15, 30, 60, 180, 240, 360, 720))
        submission_button = st.form_submit_button(label='Start')
        if submission_button:
            try:
                st.info(f'Drawing {code2cn_name(code)}:{code} ...')
            except IndexError:
                st.info(f'Your code is not valid')
            # st_pyecharts(sto.draw_single(code, previous=50, render=False))
            components.html(sto.draw_single(code, previous=p, render=False).render_embed(), height=800, width=1200)


def select():
    st.header('Favorit Shares')
    a1, a2 = st.columns([3, 1])
    a1.info('You can double click to edit the name if the name is missing or you think the name is ugly')
    a2.info('After fixing, remember to press Enter')
    with st.form(key='select'):
        data = favorit()
        # st.write(data)
        responce = AgGrid(data, height=500, editable=True, fit_columns_on_grid_load=True, )
        # df_edited = response["data"]
        # st.write("Edited DataFrame:")
        # st.dataframe(df_edited)
        n = responce['data']
        st.write(n)
        code = st.text_input(label='Input a code', )
        if not code:
            code = '1'
        col1, col2 = st.columns(2)
        add_button = col1.form_submit_button(label='Add')
        del_button = col2.form_submit_button(label='Del')
        update_button = st.form_submit_button(label='Update')
        # print(data['code'].tolist()[0])
        exsit_list = data['code'].tolist()

        if update_button:
            st.info('Update Successfully')
            n.to_csv(r'./favorite.csv')
            return None

        elif add_button:
            try:
                cn_name = code2cn_name(str(code))
            except Exception:
                st.error('Invalid Code')
                return None

            if int(code) in exsit_list:

                st.error(f'{cn_name}: {code} Already Exist')
            else:
                data.loc[str(len(data))] = str(code), cn_name
                st.success(f'{cn_name}: {code} Add Successfully, Please Update')

        elif del_button:
            if int(code) not in data['code'].tolist():
                st.error('Not in favorite list')
            else:
                st.warning(f'{code2cn_name(code)}: {code} Delete Successfully, Please Update')

                data = data.drop(index=data[data['code'] == int(code)].index)
        data.to_csv(r'./favorite.csv')
if __name__ == '__main__':

    favorite_query()
    select()