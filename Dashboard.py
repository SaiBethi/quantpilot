import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

st.title("📊 Price Dashboard")

ticker = st.text_input("Enter stock ticker (e.g., AAPL)", value="SMCI")
start_date = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("2025-06-19"))

if ticker:
    try:
        data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
        data['MA20'] = data['Close'].rolling(20).mean()
        data['MA50'] = data['Close'].rolling(50).mean()

        # RSI calculation
        delta = data['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()
        rs = avg_gain / avg_loss
        data['RSI'] = 100 - (100 / (1 + rs))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close Price'))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], name='MA20'))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], name='MA50'))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Relative Strength Index (RSI)")
        st.line_chart(data['RSI'])

        st.download_button("Download CSV", data.to_csv().encode('utf-8'), f"{ticker}_data.csv", "text/csv")

    except Exception as e:
        st.error(f"Error fetching data: {e}")