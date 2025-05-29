import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="QuantPilot", layout="wide")
st.title("📈 QuantPilot: AI-Powered Stock Dashboard")

ticker = st.text_input("Enter stock ticker (e.g., AAPL)", value="AAPL")
start_date = st.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("today"))

if st.button("Load Data"):
    data = yf.download(ticker, start=start_date, end=end_date)
    if not data.empty:
        st.subheader(f"Price chart for {ticker}")
        st.line_chart(data['Close'])

        st.subheader("Indicators")
        data['MA20'] = data['Close'].rolling(20).mean()
        data['MA50'] = data['Close'].rolling(50).mean()
        st.line_chart(data[['Close', 'MA20', 'MA50']])

        st.subheader("Raw data")
        st.dataframe(data.tail())
    else:
        st.error("No data found. Try a different ticker.")