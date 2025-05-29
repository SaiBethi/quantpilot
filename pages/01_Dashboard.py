import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from utils import calculate_indicators, fetch_stock_data

st.set_page_config(page_title="Dashboard", layout="wide", page_icon="📊")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/styles.css")

st.title("📊 Dashboard")

col1, col2 = st.columns([2,1])

with col1:
    ticker = st.text_input("Enter stock ticker", value="SMCI").upper().strip()
    start_date = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2025-06-19"))
    fetch_button = st.button("Fetch Data & Plot")

with col2:
    st.markdown("### Data Export")
    st.info("Download the stock data with indicators below.")

if fetch_button:
    if start_date > end_date:
        st.error("Start date must be before end date.")
    elif not ticker:
        st.warning("Please enter a ticker symbol.")
    else:
        data = fetch_stock_data(ticker, start_date, end_date)
        if data.empty:
            st.warning(f"No data found for ticker {ticker}")
        else:
            data = calculate_indicators(data)

            # Price + Moving Averages Chart
            price_fig = go.Figure()
            price_fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode="lines", name="Close Price"))
            price_fig.add_trace(go.Scatter(x=data.index, y=data["MA20"], mode="lines", name="MA 20"))
            price_fig.add_trace(go.Scatter(x=data.index, y=data["MA50"], mode="lines", name="MA 50"))
            price_fig.update_layout(title=f"Price Chart for {ticker}", yaxis_title="Price (USD)")

            # RSI Chart
            rsi_fig = go.Figure()
            rsi_fig.add_trace(go.Scatter(x=data.index, y=data["RSI"], mode="lines", name="RSI"))
            rsi_fig.update_layout(title=f"RSI (Relative Strength Index) for {ticker}", yaxis_title="RSI", yaxis=dict(range=[0, 100]))

            st.plotly_chart(price_fig, use_container_width=True)
            st.plotly_chart(rsi_fig, use_container_width=True)

            csv = data.to_csv().encode()
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f"{ticker}_data.csv",
                mime="text/csv",
            )