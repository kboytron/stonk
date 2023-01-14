import pandas as pd
import yfinance as yf
import datetime
import streamlit as st 
import plotly
import plotly.graph_objects as go 
from pandas_datareader import data as wb

today = datetime.date.today()
inception = datetime.date(2020, 3, 20)
full = datetime.date(2018,1,1)

# for if you want a bigger chart before you invested 

stonks = pd.read_excel('stonks.xlsx', 'base')

mainBook = pd.DataFrame(stonks)
ticker_list = list(set(mainBook['Ticker']))
current_price = []

for ticker in ticker_list:
    df = wb.DataReader(ticker, 'yahoo', start = inception, end = today)
    df2 = df.iloc[[-1],3]
    current_price.append(float(df2))

#different dataviews
book1 = mainBook['Value'].groupby(mainBook['Ticker']).sum()

book2 = mainBook.loc[mainBook['Transaction'] == 'buy',
 ['Ticker', 'Average']]

book3 = book2['Average'].groupby(book2['Ticker']).mean()

book4 = pd.DataFrame({ 'Titles': book1, 'Buy' : book3 })

book5 = pd.DataFrame(
    {'Current': current_price},
     index = ticker_list)

book6 = pd.concat([book4,book5], axis = 1)

book6['Pc Returns'] = (book6['Current']- 
book6['Buy'])/book6['Buy']
book6['Total_PL'] = ((book6['Titles']*book6['Current']) -
(book6['Titles']*book6['Buy']))

book7 = book6.loc[book6['Titles']>0]

book8 = book6
book8['tot_buy'] = book8['Titles']*book8['Buy']
book8['tot_cur'] = book8['Titles']*book8['Current']
book8 = book8.loc[book8['Titles']>0]

ticker_list2 = list(book8.index)
ticker_list2.append('All')

usd_tot_in = book8['tot_buy'].sum()
usd_cur_in = book8['tot_cur'].sum()
usd_pl = book8['tot_pl'].sum()

st.header('Portfolio Tracker')
st.write('Performance of the port')

indicator2 = st.selectbox("Select an asset:", ticker_list2, 6)

if indicator2 == 'All':
    st.subheader('Portfolio Summary')

    st.write('Port P&L')
    fig9 = go.Figure()
    fig9.add_trace(go.pie(labels = book8.index,
    values = book8['tot_pl'], pull = [0, 0, 0, 0]))
    fig9.update_layout(title='Current P&L')

    fig9.update_layout(height = 600, width = 400)
    st.plotly_chart(fig9, use_container_width=True)

    st.write('Total Invested')
    st.write(float(usd_tot_in))
    st.write('Current Value')
    st.write(float(usd_cur_in))
    st.write('P&L')
    st.write(float(usd_pl))

    st.write('Portfolio Data')
    st.dataframe(book8)

for ticker2 in ticker_list:
    if indicator2 == ticker2:
        st.subheader('Summary')

        ytd = wb.DataReader(ticker2, 'yahoo', start = inception, end = today)

        allTime = wb.DataReader(ticker2, 'yahoo', start = full, end = today)


        ytd['Returns'] = ytd['Close'].pct_change()
        allTime['Returns'] = allTime['Close'].pct_change()

        st.write('YTD Closing Prices')
        fig10 = go.Figure()
        fig10.add_trace(go.Scatter(x = ytd.index, y = ytd['High'],
        mode = 'lines', name = 'YTD Closing Prices'))

        fig10.update_xaxes(type = 'category')
        fig10.update_layout(height = 600, width = 600)
        st.plotly_chart(fig10, use_container_width=True)

        st.write('YTD Stats')
        st.dataframe(ytd.describe())

        st.write('YTD Closing Prices')
        st.dataframe(ytd)

        st.write('Historical Closing Prices')
        fig11 = go.Figure()
        fig11.add_trace(go.Candlestick(x=allTime.index,
        open = allTime['Open'],
        high = allTime['High'],
        low = allTime['Low'],
        close = allTime['Close'], name = 'Historical Closing Prices'))

        fig11.update_xaxes(type = 'category')
        fig11.update_layout(height=600, width=600)
        st.plotly_chart(fig11, use_container_width = True)

        st.write('Historical Closing Prices')
        st.dataframe(allTime)
