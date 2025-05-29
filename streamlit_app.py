import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from utils import calculate_indicators, fetch_stock_data

st.set_page_config(page_title="Dashboard", layout="wide", page_icon="📊")

# Load CSS for El Garamond + custom styles
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("assets/styles.css")

st.title("📊 QuantPilot Dashboard")

# Sidebar inputs for ticker and dates
st.sidebar.header("Stock Data Input")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="SMCI").upper().strip()

start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2025-06-19"))

fetch_button = st.sidebar.button("Fetch Data & Plot", help="Fetch stock data from Yahoo Finance and plot")

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Instructions:**  
    - Enter a valid stock ticker symbol (e.g., AAPL, MSFT).  
    - Select start and end dates for data range.  
    - Click **Fetch Data & Plot** to view charts and download data.
    """
)

# Main area for output
if fetch_button:
    if start_date > end_date:
        st.sidebar.error("❌ Start date must be before end date.")
    elif not ticker:
        st.sidebar.warning("⚠️ Please enter a ticker symbol.")
    else:
        with st.spinner("Fetching and processing data... ⏳"):
            data = fetch_stock_data(ticker, start_date, end_date)

        if data.empty:
            st.warning(f"⚠️ No data found for ticker '{ticker}'. Check ticker symbol and try again.")
        else:
            data = calculate_indicators(data)

            st.success(f"✅ Data fetched successfully for {ticker}!")
            
            # Layout: two charts side-by-side
            price_col, rsi_col = st.columns([3, 1.5])

            with price_col:
                price_fig = go.Figure()
                price_fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode="lines", name="Close Price"))
                price_fig.add_trace(go.Scatter(x=data.index, y=data["MA20"], mode="lines", name="MA 20"))
                price_fig.add_trace(go.Scatter(x=data.index, y=data["MA50"], mode="lines", name="MA 50"))
                price_fig.update_layout(
                    title=f"Price Chart for {ticker}",
                    yaxis_title="Price (USD)",
                    template="plotly_white",
                    legend=dict(x=0, y=1)
                )
                st.plotly_chart(price_fig, use_container_width=True)

            with rsi_col:
                rsi_fig = go.Figure()
                rsi_fig.add_trace(go.Scatter(x=data.index, y=data["RSI"], mode="lines", name="RSI"))
                rsi_fig.update_layout(
                    title=f"RSI (Relative Strength Index)",
                    yaxis_title="RSI",
                    yaxis=dict(range=[0, 100]),
                    template="plotly_white"
                )
                st.plotly_chart(rsi_fig, use_container_width=True)

            # Download CSV button at bottom full width
            csv = data.to_csv().encode()
            st.download_button(
                label="⬇️ Download stock data with indicators as CSV",
                data=csv,
                file_name=f"{ticker}_data.csv",
                mime="text/csv",
                help="Click to download the data used in the charts."
            )
else:
    st.info("Use the sidebar to input stock ticker and date range, then click 'Fetch Data & Plot'.")