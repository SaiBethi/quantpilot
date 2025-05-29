import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="QuantPilot Dashboard", layout="wide")

st.title("📊 QuantPilot Stock Dashboard")
st.markdown("""
Use this dashboard to explore historical price data, technical indicators, and get AI-powered trend predictions.
""")

# --- Sidebar ---
st.sidebar.header("Stock Settings")
ticker = st.sidebar.text_input("Enter stock ticker", value="AAPL")
period = st.sidebar.selectbox("Select time period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
interval = st.sidebar.selectbox("Select interval", ["1d", "1h", "15m"], index=0)

# --- Download Data ---
data = yf.download(ticker, period=period, interval=interval)
if data.empty:
    st.error("No data found. Please try a different ticker or time period.")
    st.stop()
data.reset_index(inplace=True)

# --- Line Chart: Stock Price ---
st.subheader(f"📈 {ticker.upper()} Price Chart")
fig_price = go.Figure()
fig_price.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close'))
fig_price.update_layout(title=f"{ticker.upper()} Closing Price", xaxis_title='Date', yaxis_title='Price')
st.plotly_chart(fig_price, use_container_width=True)

# --- Technical Indicators ---
st.subheader("📊 Technical Indicators")
data['RSI'] = RSIIndicator(close=data['Close']).rsi()
data['MACD'] = MACD(close=data['Close']).macd_diff()
bb = BollingerBands(close=data['Close'])
data['BB_High'] = bb.bollinger_hband()
data['BB_Low'] = bb.bollinger_lband()

col1, col2 = st.columns(2)
with col1:
    st.write("**Relative Strength Index (RSI)**")
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=data['Date'], y=data['RSI'], mode='lines', name='RSI'))
    fig_rsi.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig_rsi, use_container_width=True)

with col2:
    st.write("**MACD Histogram**")
    fig_macd = go.Figure()
    fig_macd.add_trace(go.Bar(x=data['Date'], y=data['MACD'], name='MACD'))
    st.plotly_chart(fig_macd, use_container_width=True)

# --- Bollinger Bands Chart ---
st.write("**Bollinger Bands**")
fig_bb = go.Figure()
fig_bb.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close'))
fig_bb.add_trace(go.Scatter(x=data['Date'], y=data['BB_High'], line=dict(dash='dot'), name='Upper Band'))
fig_bb.add_trace(go.Scatter(x=data['Date'], y=data['BB_Low'], line=dict(dash='dot'), name='Lower Band'))
st.plotly_chart(fig_bb, use_container_width=True)

# --- AI Prediction: Simple Linear Regression ---
st.subheader("🤖 AI Prediction (Linear Regression)")
data['Timestamp'] = data['Date'].astype(np.int64) // 10**9
X = data['Timestamp'].values.reshape(-1, 1)
y = data['Close'].values.reshape(-1, 1)

model = LinearRegression()
model.fit(X, y)

data['Predicted'] = model.predict(X)

fig_pred = go.Figure()
fig_pred.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Actual'))
fig_pred.add_trace(go.Scatter(x=data['Date'], y=data['Predicted'].flatten(), mode='lines', name='Predicted', line=dict(dash='dash')))
fig_pred.update_layout(title="AI Price Trend Prediction", xaxis_title="Date", yaxis_title="Price")
st.plotly_chart(fig_pred, use_container_width=True)

# --- Download CSV ---
st.download_button("📥 Download CSV", data=data.to_csv(index=False), file_name=f"{ticker}_data.csv")