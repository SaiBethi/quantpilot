import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Optional: For technical indicators
try:
    import pandas_ta as ta
    TA_INSTALLED = True
except ImportError:
    TA_INSTALLED = False

st.set_page_config(page_title="QuantPilot: All-in-One Dashboard", layout="wide")

# ---- Global Styling: EB Garamond Everywhere ----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');
    html, body, [class*="css"], .stApp {
        font-family: 'EB Garamond', serif !important;
        background: #f4f8fb !important;
    }
    div[data-testid="stSidebar"] {
        background: #f0f3f9;
        font-family: 'EB Garamond', serif !important;
    }
    .stButton>button, .stDownloadButton>button, .stSelectbox>div {
        font-family: 'EB Garamond', serif !important;
        font-weight: 600;
        font-size: 1.1rem;
        border-radius: 10px;
        background: #fff;
        color: #23272a;
        border: 1.5px solid #e4eaf2;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        transition: background 0.16s, color 0.16s, box-shadow 0.18s;
        margin-bottom: 0.5em;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background: #ebe5dc;
        color: #111;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    h1, h2, h3, h4, h5, h6, .stMarkdown {
        font-family: 'EB Garamond', serif !important;
    }
    .block-container {
        padding-top: 1.2rem;
        padding-right: 2rem;
        padding-left: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Title & Intro ----
st.markdown("<h1 style='text-align:center;'>📈 QuantPilot: All-in-One Dashboard</h1>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; font-size:1.2rem; margin-bottom:1.5em;'>
    Level up your investing with <b>QuantPilot</b>: advanced analytics, interactive charts, and easy-to-understand insights.<br>
    <span style='color:#666; font-size:1rem;'>
    Get clarity on your stocks—no matter your experience level.
    </span>
</div>
""", unsafe_allow_html=True)

# ---- User Inputs ----
with st.expander("Start Here: Select Tickers and Date Range", expanded=True):
    tickers = [
        t for t in st.text_input(
            "Enter one or more stock tickers (comma separated, e.g., AAPL, TSLA, MSFT):",
            value="AAPL, TSLA"
        ).upper().replace(" ", "").split(",") if t
    ]
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        start = st.date_input("Start date", pd.to_datetime("2023-01-01"))
    with col2:
        end = st.date_input("End date", pd.to_datetime("today"))
    with col3:
        interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)
    st.caption("💡 You can add more tickers separated by commas!")

# ---- Technical Indicator Selection ----
with st.expander("Customize: Technical Indicators", expanded=True):
    if TA_INSTALLED:
        indicators = st.multiselect(
            "Choose which indicators to add to your charts:",
            ["RSI", "MACD", "EMA20", "SMA50", "BB", "VWAP", "ATR", "EMA100"],
            default=["RSI", "BB", "EMA20", "SMA50"]
        )
    else:
        indicators = []
        st.info("Install `pandas_ta` for more technical indicators (pip install pandas_ta).")

# ---- Explanations Section ----
st.markdown("<h2 style='margin-top:1.7em;'>📚 Indicator Explanations</h2>", unsafe_allow_html=True)
st.markdown("""
- <b>Bollinger Bands (BB Upper/Lower):</b> These bands show potential overbought (upper) and oversold (lower) zones based on volatility. When price touches the upper band, the stock may be overbought; when it touches the lower band, it may be oversold.
- <b>Moving Average 20 (MA20) / 50 (MA50):</b> These smooth out price data to show trend direction. MA20 responds faster to price changes; MA50 is slower and shows longer-term trend.
- <b>RSI (Relative Strength Index):</b> Measures momentum on a scale from 0 to 100. Above 70 means a stock might be overbought; below 30, oversold.
- <b>MACD (Moving Average Convergence Divergence):</b> Follows trends and momentum. When MACD crosses above its signal line, it can be a bullish sign; if it crosses below, bearish.
- <b>VWAP (Volume Weighted Average Price):</b> Shows the average price weighted by volume; often used by institutional traders for entries/exits.
- <b>ATR (Average True Range):</b> Measures volatility. Higher ATR means more price movement (risk).
- <b>EMA100:</b> The Exponential Moving Average over 100 periods, which reacts quickly to price and shows long-term trend.
""", unsafe_allow_html=True)

# ---- Analysis Section ----
st.markdown("<h2 style='margin-top:2em;'>🔎 Stock Data & Analysis</h2>", unsafe_allow_html=True)
if st.button("Get Data & Analyze", key="getdata"):
    for ticker in tickers:
        if not ticker:
            continue
        st.markdown(f"<h3 style='margin-top:1.5em; margin-bottom:0.4em;'>{ticker}</h3>", unsafe_allow_html=True)
        try:
            data = yf.download(ticker, start=start, end=end, interval=interval)
        except Exception as e:
            st.error(f"Error fetching {ticker}: {str(e)}")
            continue

        if not data.empty:
            # Calculate indicators
            if TA_INSTALLED:
                if "RSI" in indicators:
                    data['RSI'] = ta.rsi(data['Close'], length=14)
                if "EMA20" in indicators:
                    data['EMA20'] = ta.ema(data['Close'], length=20)
                if "SMA50" in indicators:
                    data['SMA50'] = ta.sma(data['Close'], length=50)
                if "MACD" in indicators:
                    macd = ta.macd(data['Close'])
                    data = pd.concat([data, macd], axis=1)
                if "BB" in indicators:
                    bb = ta.bbands(data['Close'])
                    data = pd.concat([data, bb], axis=1)
                if "VWAP" in indicators:
                    data['VWAP'] = ta.vwap(data['High'], data['Low'], data['Close'], data['Volume'])
                if "ATR" in indicators:
                    data['ATR'] = ta.atr(data['High'], data['Low'], data['Close'])
                if "EMA100" in indicators:
                    data['EMA100'] = ta.ema(data['Close'], length=100)
            else:
                # Minimal built-in indicators if pandas_ta is missing
                data['MA20'] = data['Close'].rolling(window=20).mean()
                data['MA50'] = data['Close'].rolling(window=50).mean()

            # ---- Chart Section ----
            st.markdown("<h4>📊 Price Chart & Indicators</h4>", unsafe_allow_html=True)
            # Only plot columns that exist and contain at least one non-NaN value
            possible_cols = ["Close", "EMA20", "SMA50", "EMA100", "VWAP", "BBL_5_2.0", "BBU_5_2.0", "MA20", "MA50"]
            chart_cols = [col for col in possible_cols if col in data.columns and data[col].notna().any()]

            if chart_cols:
                fig = px.line(data, x=data.index, y=chart_cols, title=f"{ticker} Closing Price & Indicators", labels={"value": "Price"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No valid data to plot for this ticker and timeframe.")

            # ---- RSI Chart ----
            if "RSI" in data.columns and data["RSI"].notna().any():
                st.markdown("<h4>📉 RSI (Momentum)</h4>", unsafe_allow_html=True)
                st.line_chart(data['RSI'])

            # ---- MACD Chart ----
            if "MACD_12_26_9" in data.columns and "MACDs_12_26_9" in data.columns and data["MACD_12_26_9"].notna().any():
                st.markdown("<h4>📈 MACD</h4>", unsafe_allow_html=True)
                st.line_chart(data[["MACD_12_26_9", "MACDs_12_26_9"]])

            # ---- Volatility Chart (ATR) ----
            if "ATR" in data.columns and data["ATR"].notna().any():
                st.markdown("<h4>📊 ATR (Volatility)</h4>", unsafe_allow_html=True)
                st.line_chart(data['ATR'])

            # ---- Key Stats ----
            st.markdown("<h4>📋 Key Stats for this Period</h4>", unsafe_allow_html=True)
            st.write(f"**Latest Close:** ${data['Close'].iloc[-1]:.2f}")
            st.write(f"**Volume:** {data['Volume'].iloc[-1]:,.0f}")
            st.write(f"**High (period):** ${data['High'].max():.2f}")
            st.write(f"**Low (period):** ${data['Low'].min():.2f}")
            st.write(f"**Total Trading Days:** {len(data)}")

            st.download_button(
                label="Download data as CSV",
                data=data.to_csv().encode(),
                file_name=f"{ticker}_{start}_{end}.csv",
                mime="text/csv",
            )

            # ---- Simple "AI-Powered" Trading Suggestion ----
            st.markdown("<h4>🤖 AI-Powered Trading Suggestion</h4>", unsafe_allow_html=True)
            mean_close = data['Close'].mean()
            latest_close = data['Close'].iloc[-1]
            rsi_val = data['RSI'].iloc[-1] if "RSI" in data.columns and data["RSI"].notna().any() else None
            macd_val = data['MACD_12_26_9'].iloc[-1] if "MACD_12_26_9" in data.columns and data["MACD_12_26_9"].notna().any() else None
            bb_upper = data['BBU_5_2.0'].iloc[-1] if "BBU_5_2.0" in data.columns and data["BBU_5_2.0"].notna().any() else None
            bb_lower = data['BBL_5_2.0'].iloc[-1] if "BBL_5_2.0" in data.columns and data["BBL_5_2.0"].notna().any() else None

            suggestion = []
            if latest_close > mean_close:
                suggestion.append("The current price is **above** its average—bullish trend.")
            else:
                suggestion.append("The current price is **below** its average—watch for reversals.")

            if rsi_val is not None:
                if rsi_val > 70:
                    suggestion.append("RSI suggests the stock is **overbought**. Caution: may pull back soon.")
                elif rsi_val < 30:
                    suggestion.append("RSI suggests the stock is **oversold**. There could be a rebound opportunity.")
                else:
                    suggestion.append("RSI is in a neutral range.")

            if macd_val is not None:
                if macd_val > 0:
                    suggestion.append("MACD is positive: momentum is to the upside.")
                else:
                    suggestion.append("MACD is negative: momentum leans bearish.")

            if bb_upper is not None and latest_close >= bb_upper:
                suggestion.append("Price is touching the **upper Bollinger Band** (potential overbought).")
            if bb_lower is not None and latest_close <= bb_lower:
                suggestion.append("Price is touching the **lower Bollinger Band** (potential oversold).")

            st.markdown(" ".join(suggestion))
            st.caption("(*These suggestions are rule-based and for educational purposes. Always research thoroughly before investing!*)")

        else:
            st.error("No data found. Please check the ticker or date range.")

# ---- About Section ----
with st.expander("About QuantPilot"):
    st.markdown("""
    <b>QuantPilot</b> empowers investors with:
    - Beautiful, interactive charts
    - Multiple technical indicators
    - Downloadable data
    - Clear, plain-English insights
    - Multi-ticker support!
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; font-family:'EB Garamond',serif; font-size:1.11rem; color:#888;">
        &copy; 2025 QuantPilot. All rights reserved.
    </div>
    """, unsafe_allow_html=True)