import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

st.set_page_config(page_title="QuantPilot", layout="wide")

st.title("📈 QuantPilot: AI-Powered Stock Dashboard")

# Sidebar input
ticker = st.sidebar.text_input("Enter stock ticker (e.g., AAPL)", value="SMCI")
start_date = st.sidebar.date_input("Start Date", value=datetime(2022, 1, 1))
end_date = st.sidebar.date_input("End Date", value=datetime(2025, 6, 19))

# Download data
@st.cache_data(ttl=3600)
def get_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['Returns'] = df['Close'].pct_change()
    df['RSI'] = compute_rsi(df['Close'], 14)
    df['MACD'], df['Signal'] = compute_macd(df['Close'])
    return df

# RSI Function
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# MACD Function
def compute_macd(series):
    exp1 = series.ewm(span=12, adjust=False).mean()
    exp2 = series.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

# Get data
if ticker:
    try:
        df = get_data(ticker, start_date, end_date)

        # Display chart
        st.subheader(f"📊 Price Chart for {ticker}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close'))
        fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], mode='lines', name='MA20'))
        fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], mode='lines', name='MA50'))
        fig.update_layout(height=500, xaxis_title='Date', yaxis_title='Price', template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        # Indicators
        with st.expander("📐 Technical Indicators"):
            st.line_chart(df[['RSI']].dropna(), height=150, use_container_width=True)
            st.line_chart(df[['MACD', 'Signal']].dropna(), height=150, use_container_width=True)

        # Fundamentals
        with st.expander("📄 Stock Summary Info"):
            stock = yf.Ticker(ticker)
            info = stock.info
            st.markdown(f"**Name**: {info.get('shortName', 'N/A')}")
            st.markdown(f"**Market Cap**: {info.get('marketCap', 'N/A')}")
            st.markdown(f"**Sector**: {info.get('sector', 'N/A')}")
            st.markdown(f"**PE Ratio (TTM)**: {info.get('trailingPE', 'N/A')}")
            st.markdown(f"**Dividend Yield**: {info.get('dividendYield', 'N/A')}")

        # Download data
        st.download_button("📥 Download Data as CSV", df.to_csv().encode(), file_name=f"{ticker}_data.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Error fetching data: {e}")