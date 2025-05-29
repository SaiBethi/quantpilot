import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np

st.title("📈 QuantPilot: AI-Powered Stock Dashboard")

ticker = st.text_input("Enter stock ticker (e.g., AAPL)", value="SMCI")
start_date = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("2025-06-19"))

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

if ticker:
    raw_data = yf.download(ticker, start=start_date, end=end_date, group_by='ticker', auto_adjust=True)

    if isinstance(raw_data.columns, pd.MultiIndex):
        raw_data.columns = ['_'.join(col).strip() for col in raw_data.columns.values]
    else:
        raw_data.columns = [col.strip() for col in raw_data.columns]

    possible_close_cols = [col for col in raw_data.columns if 'Close' in col]
    if not possible_close_cols:
        st.error("Couldn't find a 'Close' column for this ticker. Try another.")
    else:
        close_col = possible_close_cols[0]

        # Calculate moving averages
        raw_data['MA20'] = raw_data[close_col].rolling(window=20).mean()
        raw_data['MA50'] = raw_data[close_col].rolling(window=50).mean()

        # Calculate RSI
        raw_data['RSI'] = calculate_rsi(raw_data[close_col])

        # Prepare columns for plotting (only include if they exist)
        plot_cols = [col for col in [close_col, 'MA20', 'MA50'] if col in raw_data.columns]

        st.subheader(f"📊 Price Chart for {ticker}")
        st.line_chart(raw_data[plot_cols])

        st.subheader("📉 RSI Chart")
        if 'RSI' in raw_data.columns:
            st.line_chart(raw_data['RSI'])
        else:
            st.info("RSI data not available yet.")