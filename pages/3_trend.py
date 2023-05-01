#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : 3_trend.py
@Author  : Gan Yuyang
@Time    : 2023/4/4 12:39
"""
import json
import re
import ast
from datetime import datetime
from pyecharts.charts import Pie
from pyecharts import options as opts
from st_aggrid import AgGrid

import pandas as pd
import pyperclip
import requests
import streamlit as st
import streamlit.components.v1 as components
from fake_useragent import UserAgent
from streamlit_echarts import st_pyecharts

import time

import args
from args import ua

st.set_page_config(layout="wide")


# @st.cache_data
def trend(top=10, by='volume'):
    url = f'https://stock.xueqiu.com/v5/stock/screener/quote/list.json?type=sha&order_by={by}&order=desc&size=10&page=1'
    session = args.snowball_session()
    rep = session.get(url, headers=args.snowball_simple_headers)
    rep.encoding = args.encoding
    print(rep.status_code)
    a = rep.text

    a = json.loads(a)
    data_dict = a['data']['list']
    cols = list(data_dict[0].keys())
    # print(cols)
    # print(data_dict[0])
    datas = [list(data_dict[i].values()) for i in range(top)]
    df = pd.DataFrame(columns=cols, data=datas)
    df = df[['symbol', 'name', 'volume', 'percent', 'market_capital', 'roe_ttm', 'percent5m', 'amount',
             'main_net_inflows', 'volume_ratio', 'turnover_rate','north_net_inflow' , 'pe_ttm']]
    return df


def draw_trend(top=9, by='volume', render=False):
    df = trend(top, by)
    name = df['name'].tolist()

    by_ = df[by].tolist()
    c = (
        Pie()
            .add(
            "成交量" if by == 'amount' else "成交额",
            [list(z) for z in zip(name, by_)],
            radius=["35%", "75%"],
            center=["45%", "55%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=f"Trend({by})"),
            legend_opts=opts.LegendOpts(orient='vertical', pos_left='-15', pos_top='40'),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}\n{d}%"))
    )
    if render:
        c.render("pie_radius.html")
    return c


def trend_show():
    st.header('Grab the Trend')
    # with st.form(key='trend'):
    a, b = st.columns(2)
    st.subheader('Choose the trend standard')
    by = st.selectbox('Standard', ('volume', 'amount'))
    df = trend(by=by)

    with a:
        st_pyecharts(draw_trend(by=by), key='a')
    with b:
        AgGrid(df[['name', 'symbol', 'percent', 'percent5m', 'turnover_rate', by]],
               fit_columns_on_grid_load=True,
               editable=True)

    df.to_csv('trend.csv')
    st.info('Trend saved. You can see it in Query-> Refer')
    st.success('Grad the opportunity')

if __name__ == '__main__':
    trend_show()
