import pandas as pd
import streamlit as st
from streamlit_echarts import st_pyecharts
from streamlit_echarts import Map as st_Map
from stock_info import StockInfo
import json
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
sto = StockInfo(headless=True, fine_update=False)

@st.cache_data
def area_init():
    with open('basic_html/area_distribution.html', 'r', encoding='utf-8') as f:
        return f.read()


def area():
    st.header('Area Distribution')
    components.html(area_init(), height=500, scrolling=False)


def macro():
    st.header('A Share Historic Macro Data')
    previous = st.slider('Previou_date', 3, 15, 7)

    st_pyecharts(sto.draw_macro(render=False, previous=previous))


@st.cache_data
def get_rough_df():
    return sto.rough_industry_df


@st.cache_data
def get_fine_df():
    return sto.fine_industry_df


def classify():
    st.header('A Share Classification')
    option = st.selectbox('Classification Degree', ('Rough', 'Fine'))
    df_1 = {'Rough': get_rough_df(), 'Fine': get_fine_df()}[option]
    st_pyecharts(sto.draw_classify_chart(df_1, render=False))


def industry():
    st.header('Classified Draw')
    fdf = sto.fine_industry_df
    cn_name = fdf.loc[:, 'industry'].tolist()
    ind_code = fdf.loc[:, 'industry_code'].tolist()
    with st.form(key='industry',):

        l = [f'{i}: {j}' for i, j in zip(ind_code, cn_name)]
        options = st.multiselect('Choose Some Industries', l)
        previous = int(st.number_input('Previous', min_value=7))
        submission_button = st.form_submit_button(label='Done')

        # print(l)
        if submission_button:
            for ind in options:
                df = pd.read_csv(f'fine_field_csv_folder/{ind[:3]}.csv')
                # print(df)
                if len(df) <= 10:
                    pass
                st_pyecharts(sto.draw_industry(ind[:3], previous, render=False))


def single_query():
    st.header('Single Share Query')
    with st.form(key='form_query',):
        code = st.text_input(
            label='input a code',
            value='601318',
            key='placeholder'
        )
        option = st.selectbox('Previous Length', (7, 15, 30, 60, 120))
        submission_button = st.form_submit_button(label='Done')
        if submission_button:
            try:
                st.write(f'Drawing {sto.code2cn_name(code)}:{code} ...')
            except IndexError:
                st.write(f'Your code is not valid')
            # st_pyecharts(sto.draw_single(code, previous=50, render=False))
            components.html(sto.draw_single(code, previous=option, render=False).render_embed(), height=800, width=1200)

def favorit():


if __name__ == '__main__':
    area()
    macro()
    classify()
    industry()
    single_query()
