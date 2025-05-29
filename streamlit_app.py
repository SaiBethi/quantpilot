import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# Load custom styles
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("🔍 QuantPilot Menu")
page = st.sidebar.radio("Navigate", ["Dashboard", "AI Insights", "About"])

# --- Header ---
st.title("📈 QuantPilot: AI-Powered Stock Dashboard")

# --- Dashboard Page ---
if page == "Dashboard":
    ticker = st.text_input("Enter stock ticker (e.g., AAPL)", value="SMCI")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2025-06-19"))

    if ticker:
        try:
            data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)

            # Add indicators
            data["MA20"] = data["Close"].rolling(window=20).mean()
            data["MA50"] = data["Close"].rolling(window=50).mean()

            delta = data["Close"].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(14).mean()
            avg_loss = loss.rolling(14).mean()
            rs = avg_gain / avg_loss
            data["RSI"] = 100 - (100 / (1 + rs))

            st.subheader(f"📊 Price Chart for {ticker}")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode='lines', name="Close"))
            fig.add_trace(go.Scatter(x=data.index, y=data["MA20"], mode='lines', name="MA 20"))
            fig.add_trace(go.Scatter(x=data.index, y=data["MA50"], mode='lines', name="MA 50"))
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("📉 RSI Indicator")
            rsi_fig = go.Figure()
            rsi_fig.add_trace(go.Scatter(x=data.index, y=data["RSI"], mode='lines', name="RSI"))
            rsi_fig.update_layout(yaxis=dict(range=[0, 100]))
            st.plotly_chart(rsi_fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error fetching data: {e}")

# --- AI Suggestions Page ---
elif page == "AI Insights":
    st.subheader("🤖 AI-Powered Suggestions (Mockup)")
    st.info("This section will provide AI-generated trading insights based on technical indicators.")
    st.markdown("""
    - **Trend**: The stock is currently in a bullish trend with price above MA50.
    - **RSI Insight**: RSI approaching 70, consider watching for a potential reversal.
    - **AI Note**: Based on recent volatility, short-term resistance may be at $X.
    """)

# --- About Page ---
elif page == "About":
    st.subheader("ℹ️ About QuantPilot")
    st.markdown("""
    **QuantPilot** is a sleek, AI-powered stock dashboard that provides:
    - 📈 Interactive price charts
    - 📊 Technical indicators (MA20, MA50, RSI)
    - 🤖 AI-generated insights
    - 🚀 Simple, beautiful UI with **El Garamond** font

    Built using [Streamlit](https://streamlit.io) and powered by [yfinance](https://pypi.org/project/yfinance/).
    """)