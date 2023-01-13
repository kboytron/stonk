import pandas as pd
import yfinance as yf
import datetime
import streamlit as st 
import plotly
import plotly.graph_objects as go 
from pandas_datareader import data as wb
import requests

today = datetime.date.today()
inception = datetime.date(2022, 12, 1)
diff = inception - today

full = '2019-01-01'
strInception = str(inception)
strToday = str(today)

stonks = pd.read_excel('stonks.xlx', 'base')

mainBook = pd.DataFrame(stonks)

print("hi")  