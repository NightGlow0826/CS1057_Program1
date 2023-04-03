import os.path
import random

import akshare as ak
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from st_aggrid import AgGrid
from streamlit_echarts import st_pyecharts

from stock_info import StockInfo, code2cn_name

st.set_page_config(layout="wide")
sto = StockInfo(headless=True, fine_update=False, simulate=False)


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
                st.info(f'Drawing {code2cn_name(code)}:{code} ...')
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
            a2.code(luck, language='java')


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
        p = c2.selectbox('Previous Length', (15, 30, 60, 120))
        submission_button = st.form_submit_button(label='Start')
        if submission_button:
            try:
                st.info(f'Drawing {sto.code2cn_name(code)}:{code} ...')
            except IndexError:
                st.info(f'Your code is not valid')
            # st_pyecharts(sto.draw_single(code, previous=50, render=False))
            components.html(sto.draw_single(code, previous=p, render=False).render_embed(), height=800, width=1200)


def select():
    st.header('Favorit Shares')
    st.info('You can double click to edit the name if the name is missing or you think the name is ugly')
    st.info('After fixing, remember to press Enter')
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
                cn_name = sto.code2cn_name(str(code))
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
                st.warning(f'{sto.code2cn_name(code)}: {code} Delete Successfully, Please Update')

                data = data.drop(index=data[data['code'] == int(code)].index)
        data.to_csv(r'./favorite.csv')


if __name__ == '__main__':
    st.title('CS1507 Program 1')
    st.header('干雨杨 PB21050969')
