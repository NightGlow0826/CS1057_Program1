#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : 2_macro_and_classification.py
@Author  : Gan Yuyang
@Time    : 2023/4/1 20:53
"""
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from streamlit_echarts import st_pyecharts
from streamlit_echarts import Map as st_Map
from stock_info import StockInfo
import json
import streamlit.components.v1 as components
import numpy as np

st.set_page_config(layout="wide")

sto = StockInfo(headless=True)

def macro():
    st.header('A Share Historic Macro Data')
    previous = st.slider('Previou_date', 3, 15, 7)

    st_pyecharts(sto.draw_macro(render=False, previous=previous, update=False))


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

macro()

classify()