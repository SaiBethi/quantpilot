import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from utils import calculate_indicators  # your helper function

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Dashboard")

ticker = st.text_input("Enter stock ticker", value="SMCI").upper().strip()
start_date = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("2025-06-19"))

if start_date > end_date:
    st.error("Start date must be before end date")
elif not ticker:
    st.warning("Please enter a ticker symbol.")
else:
    data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
    if data.empty:
        st.warning("No data found for ticker")
    else:
        data = calculate_indicators(data)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode='lines', name="Close"))
        fig.add_trace(go.Scatter(x=data.index, y=data["MA20"], mode='lines', name="MA 20"))
        fig.add_trace(go.Scatter(x=data.index, y=data["MA50"], mode='lines', name="MA 50"))
        st.plotly_chart(fig, use_container_width=True)
