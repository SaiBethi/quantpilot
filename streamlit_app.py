import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="QuantPilot", layout="wide")
st.title("📈 QuantPilot: AI-Powered Stock Dashboard")

# User Inputs
ticker = st.text_input("Enter stock ticker (e.g., AAPL)", value="SMCI")
start_date = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("2025-06-19"))

# Helper functions for indicators
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(series, fast=12, slow=26, signal=9):
    exp1 = series.ewm(span=fast, adjust=False).mean()
    exp2 = series.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

def calculate_bollinger_bands(series, window=20, num_std=2):
    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return rolling_mean, upper_band, lower_band

def ai_suggestion(rsi):
    # Simple AI heuristic: classic RSI signals
    if rsi.iloc[-1] < 30:
        return "Strong Buy Signal (RSI < 30)"
    elif rsi.iloc[-1] > 70:
        return "Strong Sell Signal (RSI > 70)"
    else:
        return "Hold - No strong signal"

if ticker:
    # Download and preprocess data
    raw_data = yf.download(ticker, start=start_date, end=end_date, group_by='ticker', auto_adjust=True)
    if raw_data.empty:
        st.error("No data found for this ticker in the selected date range.")
    else:
        # Flatten MultiIndex columns if present
        if isinstance(raw_data.columns, pd.MultiIndex):
            raw_data.columns = ['_'.join(col).strip() for col in raw_data.columns.values]
        else:
            raw_data.columns = [col.strip() for col in raw_data.columns]

        # Find close price column
        close_cols = [col for col in raw_data.columns if 'Close' in col]
        if not close_cols:
            st.error("Couldn't find a 'Close' column for this ticker. Try another.")
        else:
            close_col = close_cols[0]
            close_prices = raw_data[close_col]

            # Calculate indicators
            raw_data['MA20'] = close_prices.rolling(window=20).mean()
            raw_data['MA50'] = close_prices.rolling(window=50).mean()
            raw_data['RSI'] = calculate_rsi(close_prices)
            raw_data['MACD'], raw_data['MACD_Signal'] = calculate_macd(close_prices)
            raw_data['BB_Middle'], raw_data['BB_Upper'], raw_data['BB_Lower'] = calculate_bollinger_bands(close_prices)

            # Price Chart + MAs + Bollinger Bands
            st.subheader(f"📊 Price Chart for {ticker}")
            price_chart_df = raw_data[[close_col, 'MA20', 'MA50', 'BB_Upper', 'BB_Lower']].dropna()
            st.line_chart(price_chart_df)

            # RSI Chart
            st.subheader("📉 RSI Chart")
            st.line_chart(raw_data['RSI'].dropna())

            # MACD Chart
            st.subheader("📈 MACD Chart")
            macd_df = raw_data[['MACD', 'MACD_Signal']].dropna()
            st.line_chart(macd_df)

            # AI-powered suggestion based on RSI
            st.subheader("🤖 AI-Powered Trading Suggestion")
            suggestion = ai_suggestion(raw_data['RSI'].dropna())
            st.info(suggestion)