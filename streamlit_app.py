import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import asyncio
from transformers import pipeline  # For sentiment analysis
from fpdf import FPDF  # For PDF reports
from datetime import datetime

# Configuration
st.set_page_config(
    page_title="QuantPilot: Robinhood LEGEND",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Constants
MAX_TICKERS = 5  # Limit API calls
CACHE_TTL = 3600  # 1 hour cache

# --- CSS & UI Setup ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;600&family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"], .stApp {
        background: #0c1b2a !important;
        color: #e0e0e0 !important;
        font-family: 'EB Garamond', 'Inter', serif !important;
    }
    .block-container {
        padding-top: 0.5rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        background: #0c1b2a !important;
    }
    .rh-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.6em 2em 0.6em 1.5em;
        background: #0c1b2a;
        border-bottom: 1.5px solid #12243a;
        box-shadow: 0 2px 8px #0003;
        margin-bottom: 0.1em;
    }
    .logo-text { color: #00c805; font-size: 1.64em; font-weight: 700; letter-spacing:0.04em;}
    .stat-card {
        background: #12243a;
        border-radius: 0.9em;
        box-shadow: 0 2px 8px #0003;
        padding: 1.1em 1em 0.8em 1em;
        text-align: center;
        margin-bottom: 0.9em;
        border: 1.5px solid #1b2f44;
        transition: transform 0.13s, box-shadow 0.16s;
    }
    @media (max-width: 600px) {
        .stat-card { padding: 0.8em; margin-bottom: 0.6em; }
        .stPlotlyChart { height: 200px !important; }
    }
    </style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
async def fetch_ticker(ticker, start, end, interval):
    """Async fetch for a single ticker"""
    try:
        data = yf.download(ticker, start=start, end=end, interval=interval, progress=False)
        return ticker, data
    except Exception as e:
        st.error(f"Error fetching {ticker}: {str(e)}")
        return ticker, None

@st.cache_data(ttl=CACHE_TTL, show_spinner="Fetching market data...")
async def get_data(tickers, start, end, interval):
    """Async fetch all tickers with caching"""
    tasks = [fetch_ticker(t, start, end, interval) for t in tickers[:MAX_TICKERS]]
    results = await asyncio.gather(*tasks)
    return {ticker: data for ticker, data in results if data is not None}

def calculate_technical_indicators(df, ticker):
    """Calculate all technical indicators for a dataframe"""
    close_col = f"Close_{ticker}" if f"Close_{ticker}" in df.columns else "Close"
    
    if close_col not in df.columns:
        return None

    df = df.copy()
    df['MA20'] = df[close_col].rolling(window=20).mean()
    df['MA50'] = df[close_col].rolling(window=50).mean()
    df['MA200'] = df[close_col].rolling(window=200).mean()
    df['Daily_Return'] = df[close_col].pct_change()
    df['Volatility'] = df[close_col].rolling(window=20).std()
    df['RSI'] = rsi(df[close_col])
    df['MACD'], df['MACD_Signal'], _ = macd(df[close_col])
    df['Sharpe'] = sharpe_ratio(df['Daily_Return'].dropna())
    return df

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line, signal_line, macd_line - signal_line

def sharpe_ratio(returns, risk_free=0):
    if len(returns) < 2:
        return 0
    return (returns.mean() - risk_free) / returns.std()

# --- Main App ---
def main():
    # Navigation Bar
    st.markdown("""
    <div class="rh-navbar">
        <div style="display:flex;align-items:center;gap:0.42em;">
            <svg width="36" height="36" fill="#00c805"><polygon points="17,6 29,30 5,30" /></svg>
            <span class="logo-text">QuantPilot</span>
        </div>
        <div class="avatar" title="Profile">
            <svg width="24" height="24" fill="#e0e0e0"><circle cx="12" cy="8" r="4"/><ellipse cx="12" cy="17" rx="7" ry="5"/></svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Input Form
    with st.form("stock_form"):
        col1, col2 = st.columns(2)
        with col1:
            tickers = st.text_input("Tickers (comma separated)", "AAPL, MSFT")
            start_date = st.date_input("Start date", pd.to_datetime("2023-01-01"))
        with col2:
            end_date = st.date_input("End date", pd.to_datetime("today"))
            interval = st.selectbox("Interval", ["1d", "1wk", "1mo"])
        
        if st.form_submit_button("Analyze", type="primary"):
            st.session_state["tickers"] = [t.strip().upper() for t in tickers.split(",") if t.strip()]
            st.session_state["start"] = start_date
            st.session_state["end"] = end_date
            st.session_state["interval"] = interval
            st.experimental_rerun()

    if "tickers" not in st.session_state:
        st.stop()

    # Load data with progress
    with st.spinner("Fetching market data..."):
        data_dict = asyncio.run(get_data(
            st.session_state["tickers"],
            st.session_state["start"],
            st.session_state["end"],
            st.session_state["interval"]
        ))

    if not data_dict:
        st.error("No valid data found. Check your ticker symbols.")
        st.stop()

    # Display each ticker's analysis
    for ticker, data in data_dict.items():
        with st.expander(f"📊 {ticker} Analysis", expanded=True):
            df = calculate_technical_indicators(data, ticker)
            if df is None:
                st.warning(f"No close price data for {ticker}")
                continue

            # Visualization
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Price'
            ))
            fig.update_layout(
                title=f"{ticker} Price",
                xaxis_rangeslider_visible=False,
                template="plotly_dark",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Price", f"${df['Close'].iloc[-1]:.2f}")
            with col2:
                change = df['Close'].iloc[-1] - df['Close'].iloc[-2]
                st.metric("Daily Change", f"{change:.2f}", delta=f"{change/df['Close'].iloc[-2]:.2%}")
            with col3:
                st.metric("RSI (14)", f"{df['RSI'].iloc[-1]:.1f}")

            # Technical Charts
            st.subheader("Technical Indicators")
            tab1, tab2, tab3 = st.tabs(["RSI", "MACD", "Volatility"])
            with tab1:
                st.line_chart(df['RSI'])
            with tab2:
                st.line_chart(df[['MACD', 'MACD_Signal']])
            with tab3:
                st.area_chart(df['Volatility'])

            # AI Recommendation
            st.subheader("AI Trading Recommendation")
            generate_recommendation(df, ticker)

            # Export
            if st.button(f"Generate PDF Report for {ticker}"):
                generate_pdf_report(df, ticker)

def generate_recommendation(df, ticker):
    """Generate AI-powered trading recommendation"""
    # Simple rule-based recommendation
    last_close = df['Close'].iloc[-1]
    ma20 = df['MA20'].iloc[-1]
    ma50 = df['MA50'].iloc[-1]
    rsi_val = df['RSI'].iloc[-1]

    if (last_close > ma20) and (last_close > ma50):
        verdict = "BUY"
        color = "#00c805"
        reason = "Price above both 20-day and 50-day moving averages"
    elif (last_close < ma20) and (last_close < ma50):
        verdict = "SELL"
        color = "#ff4c4c"
        reason = "Price below both 20-day and 50-day moving averages"
    else:
        verdict = "HOLD"
        color = "#ffe48a"
        reason = "Mixed signals"

    # Add RSI consideration
    if rsi_val > 70:
        reason += " (Overbought RSI)"
    elif rsi_val < 30:
        reason += " (Oversold RSI)"

    st.markdown(f"""
    <div style="background:#1a1a1a;padding:1em;border-radius:10px;border-left:4px solid {color}">
        <h3 style="color:{color};">{verdict}</h3>
        <p>{reason}</p>
    </div>
    """, unsafe_allow_html=True)

def generate_pdf_report(df, ticker):
    """Generate PDF report for a ticker"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"QuantPilot Report: {ticker}", ln=1)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=1)
    
    # Add basic metrics
    pdf.cell(200, 10, txt=f"Current Price: ${df['Close'].iloc[-1]:.2f}", ln=1)
    pdf.cell(200, 10, txt=f"RSI (14): {df['RSI'].iloc[-1]:.1f}", ln=1)
    
    # Save to bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    
    # Download button
    st.download_button(
        label="Download PDF Report",
        data=pdf_bytes,
        file_name=f"{ticker}_report.pdf",
        mime="application/pdf"
    )

if __name__ == "__main__":
    main()