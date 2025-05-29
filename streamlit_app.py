import yfinance as yf
import streamlit as st
import pandas as pd

st.title("📈 QuantPilot: AI-Powered Stock Dashboard")

ticker = st.text_input("Enter stock ticker (e.g., AAPL)", value="SMCI")
start_date = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("2025-06-19"))

if ticker:
    # Download data
    raw_data = yf.download(ticker, start=start_date, end=end_date, group_by='ticker', auto_adjust=True)

    # If data has MultiIndex, flatten it
    if isinstance(raw_data.columns, pd.MultiIndex):
        raw_data.columns = ['_'.join(col).strip() for col in raw_data.columns.values]
    else:
        raw_data.columns = [col.strip() for col in raw_data.columns]

    # Determine close price column
    possible_close_cols = [col for col in raw_data.columns if 'Close' in col]
    if not possible_close_cols:
        st.error("Couldn't find a 'Close' column for this ticker. Try another.")
    else:
        close_col = possible_close_cols[0]

        # Compute moving averages
        raw_data['MA20'] = raw_data[close_col].rolling(window=20).mean()
        raw_data['MA50'] = raw_data[close_col].rolling(window=50).mean()

        # Only keep valid columns for charting
        plot_cols = [col for col in [close_col, 'MA20', 'MA50'] if col in raw_data.columns]

        st.subheader(f"Price chart for {ticker}")
        st.line_chart(raw_data[plot_cols])