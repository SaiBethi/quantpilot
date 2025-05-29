import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📈 QuantPilot: AI-Powered Stock Dashboard")

ticker = st.text_input("Enter stock ticker (e.g., AAPL)", value="AAPL")
start_date = st.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("today"))

if ticker:
    data = yf.download(ticker, start=start_date, end=end_date)

    if data.empty:
        st.error("No data found. Please check the ticker symbol or date range.")
    else:
        # Calculate moving averages safely
        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['MA50'] = data['Close'].rolling(window=50).mean()

        st.subheader(f"Price chart for {ticker}")
        try:
            st.line_chart(data[['Close', 'MA20', 'MA50']])
        except KeyError as e:
            st.error(f"Missing columns in data: {e}")