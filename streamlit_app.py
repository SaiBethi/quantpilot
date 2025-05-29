import yfinance as yf
import streamlit as st
import pandas as pd

st.title("📈 QuantPilot: AI-Powered Stock Dashboard")
ticker = st.text_input("Enter stock ticker (e.g., AAPL)", value="TSLA")
start_date = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("2025-06-19"))

if ticker:
    data = yf.download(ticker, start=start_date, end=end_date, group_by="ticker")

    # Flatten columns if DataFrame has MultiIndex
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = ['_'.join(col).strip() for col in data.columns.values]

    close_col = f"{ticker}_Close" if f"{ticker}_Close" in data.columns else "Close"
    
    if close_col not in data.columns:
        st.error(f"Could not find close price column for {ticker}. Try a different ticker.")
    else:
        # Calculate moving averages safely
        data['MA20'] = data[close_col].rolling(window=20).mean()
        data['MA50'] = data[close_col].rolling(window=50).mean()

        # Select columns to plot (only those that exist)
        plot_columns = [col for col in [close_col, 'MA20', 'MA50'] if col in data.columns]

        st.subheader(f"Price chart for {ticker}")
        st.line_chart(data[plot_columns])