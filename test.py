import os
import random

import bs4
import pandas as pd
import requests
import numpy as np

import akshare as ak
from akshare.stock.cons import hk_js_decode
from py_mini_racer import py_mini_racer

import streamlit as st

df1 = pd.DataFrame()
print(df1.empty)