import streamlit as st
st.set_page_config(page_title="QuantPilot: All-in-One Dashboard", layout="wide")

import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- CUSTOM STYLING ---
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

st.markdown("<h1 style='text-align:center;'>📈 QuantPilot: All-in-One Dashboard</h1>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; font-size:1.2rem; margin-bottom:1.5em;'>
    Level up your investing with <b>QuantPilot</b>: analytics, interactive charts, and easy-to-understand insights.<br>
    <span style='color:#666; font-size:1rem;'>
    Get clarity on your stocks—no matter your experience level.
    </span>
</div>
""", unsafe_allow_html=True)

with st.expander("① Start Here: Select Tickers and Date Range", expanded=True):
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

st.markdown("<h2 style='margin-top:1.7em;'>② Indicator Explanations</h2>", unsafe_allow_html=True)
st.markdown("""
<ul style='font-size:1.08em;'>
<li><b>Candlestick Chart:</b> Shows price open, high, low, and close for each period.</li>
<li><b>Simple Moving Averages (MA20, MA50, MA100, MA200):</b> Averages of closing price over 20/50/100/200 periods. Show trend direction.</li>
<li><b>Exponential Moving Averages (EMA20, EMA50, EMA100, EMA200):</b> Like SMAs but react faster to recent price changes.</li>
<li><b>Daily % Change:</b> Shows daily momentum (positive = up, negative = down).</li>
<li><b>Volatility (20-day Rolling Std):</b> Measures how much price moves up/down (higher = more volatile).</li>
<li><b>Volume Bars:</b> Number of shares traded each period.</li>
<li><b>AI Suggestion:</b> Considers price vs. averages, volatility, and momentum to give you a trading insight.</li>
</ul>
""", unsafe_allow_html=True)

st.markdown("<h2 style='margin-top:2em;'>③ Stock Data & Analysis</h2>", unsafe_allow_html=True)
if st.button("Get Data & Analyze", key="getdata"):
    data = yf.download(tickers, start=start, end=end, interval=interval, group_by='ticker', auto_adjust=True)
    if data.empty:
        st.error("No data found for these tickers in the selected date range.")
    else:
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = ["_".join([str(i) for i in col if i]) for col in data.columns.values]

        for ticker in tickers:
            st.markdown(f"<h3 style='margin-top:1.5em; margin-bottom:0.4em;'>{ticker}</h3>", unsafe_allow_html=True)
            close_col = f"Close_{ticker}" if f"Close_{ticker}" in data.columns else f"{ticker}_Close"
            open_col = f"Open_{ticker}" if f"Open_{ticker}" in data.columns else f"{ticker}_Open"
            high_col = f"High_{ticker}" if f"High_{ticker}" in data.columns else f"{ticker}_High"
            low_col = f"Low_{ticker}" if f"Low_{ticker}" in data.columns else f"{ticker}_Low"
            vol_col = f"Volume_{ticker}" if f"Volume_{ticker}" in data.columns else f"{ticker}_Volume"

            if close_col not in data.columns:
                st.warning(f"No data for {ticker}.")
                continue

            df = data[[c for c in [open_col, close_col, high_col, low_col, vol_col] if c in data.columns]].copy()

            # --- Moving Averages ---
            df['MA20'] = df[close_col].rolling(window=20).mean()
            df['MA50'] = df[close_col].rolling(window=50).mean()
            df['MA100'] = df[close_col].rolling(window=100).mean()
            df['MA200'] = df[close_col].rolling(window=200).mean()
            df['EMA20'] = df[close_col].ewm(span=20, adjust=False).mean()
            df['EMA50'] = df[close_col].ewm(span=50, adjust=False).mean()
            df['EMA100'] = df[close_col].ewm(span=100, adjust=False).mean()
            df['EMA200'] = df[close_col].ewm(span=200, adjust=False).mean()
            # --- Daily % Change (Momentum) ---
            df['Daily % Change'] = df[close_col].pct_change()*100
            # --- Volatility (20-day rolling std) ---
            df['Volatility (20d)'] = df[close_col].rolling(window=20).std()

            # --- Price Chart & Indicators ---
            st.markdown("<h4>📊 Price Chart & Indicators</h4>", unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df.index, open=df[open_col], high=df[high_col], low=df[low_col], close=df[close_col],
                name='Candlestick'
            ))
            fig.add_trace(go.Scatter(
                x=df.index, y=df["MA20"], line=dict(color='blue', width=1), name="MA20"
            ))
            fig.add_trace(go.Scatter(
                x=df.index, y=df["MA50"], line=dict(color='orange', width=1), name="MA50"
            ))
            fig.add_trace(go.Scatter(
                x=df.index, y=df["MA100"], line=dict(color='gray', width=1, dash="dot"), name="MA100"
            ))
            fig.add_trace(go.Scatter(
                x=df.index, y=df["MA200"], line=dict(color='black', width=1, dash="dot"), name="MA200"
            ))
            fig.add_trace(go.Scatter(
                x=df.index, y=df["EMA20"], line=dict(color='purple', width=1, dash='dot'), name="EMA20"
            ))
            fig.add_trace(go.Scatter(
                x=df.index, y=df["EMA50"], line=dict(color='green', width=1, dash='dot'), name="EMA50"
            ))
            fig.add_trace(go.Scatter(
                x=df.index, y=df["EMA100"], line=dict(color='magenta', width=1, dash='dot'), name="EMA100"
            ))
            fig.add_trace(go.Scatter(
                x=df.index, y=df["EMA200"], line=dict(color='red', width=1, dash='dot'), name="EMA200"
            ))
            fig.update_layout(
                title=f"{ticker} Price Chart",
                yaxis_title="Price",
                xaxis_title="Date",
                xaxis_rangeslider_visible=False,
                template="plotly_white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

            # ---- Volume Chart ----
            if vol_col in df.columns:
                st.bar_chart(df[vol_col], use_container_width=True)

            # ---- Momentum Chart ----
            st.markdown("<h4>⚡️ Daily % Change (Momentum)</h4>", unsafe_allow_html=True)
            st.line_chart(df['Daily % Change'])

            # ---- Volatility Chart ----
            st.markdown("<h4>📈 Volatility (20d rolling std)</h4>", unsafe_allow_html=True)
            st.line_chart(df['Volatility (20d)'])

            # ---- Key Stats ----
            st.markdown("<h4>📋 Key Stats for this Period</h4>", unsafe_allow_html=True)
            latest_close = df[close_col].dropna().iloc[-1] if df[close_col].notna().any() else float('nan')
            latest_vol = df[vol_col].dropna().iloc[-1] if vol_col in df.columns and df[vol_col].notna().any() else float('nan')
            st.write(f"**Latest Close:** ${latest_close:.2f}")
            st.write(f"**Volume:** {latest_vol:,.0f}")
            st.write(f"**High (period):** ${df[high_col].max():.2f}" if high_col in df.columns else "")
            st.write(f"**Low (period):** ${df[low_col].min():.2f}" if low_col in df.columns else "")
            st.write(f"**Total Trading Days:** {len(df)}")
            st.write(f"**Mean Volatility (20d):** {df['Volatility (20d)'].dropna().mean():.3f}")
            st.write(f"**Mean Daily % Change:** {df['Daily % Change'].dropna().mean():.3f}%")

            st.download_button(
                label="Download data as CSV",
                data=df.to_csv().encode(),
                file_name=f"{ticker}_{start}_{end}.csv",
                mime="text/csv",
            )

            # ---- AI-Powered Trading Suggestion ----
            st.markdown("<h4>🤖 AI-Powered Trading Suggestion</h4>", unsafe_allow_html=True)
            suggestion = []
            # Trend
            if latest_close > df['MA20'].dropna().iloc[-1]:
                suggestion.append("Price is above MA20: short-term trend is bullish.")
            elif latest_close < df['MA20'].dropna().iloc[-1]:
                suggestion.append("Price is below MA20: short-term trend is cautious.")

            if latest_close > df['MA50'].dropna().iloc[-1]:
                suggestion.append("Price is above MA50: medium-term trend is bullish.")
            elif latest_close < df['MA50'].dropna().iloc[-1]:
                suggestion.append("Price is below MA50: medium-term trend is cautious.")

            if latest_close > df['MA200'].dropna().iloc[-1]:
                suggestion.append("Price is above MA200: long-term trend is bullish.")
            elif latest_close < df['MA200'].dropna().iloc[-1]:
                suggestion.append("Price is below MA200: long-term trend is cautious.")

            # Volatility
            recent_volatility = df['Volatility (20d)'].dropna().iloc[-1] if df['Volatility (20d)'].notna().any() else 0
            avg_volatility = df['Volatility (20d)'].dropna().mean() if df['Volatility (20d)'].notna().any() else 0
            if recent_volatility > 1.2 * avg_volatility:
                suggestion.append("Volatility is high: expect larger price swings.")
            elif recent_volatility < 0.8 * avg_volatility:
                suggestion.append("Volatility is low: market is calmer.")

            # Momentum
            latest_mom = df['Daily % Change'].dropna().iloc[-1] if df['Daily % Change'].notna().any() else 0
            if latest_mom > 1:
                suggestion.append("Momentum is positive: recent price increase.")
            elif latest_mom < -1:
                suggestion.append("Momentum is negative: recent price decrease.")
            else:
                suggestion.append("Momentum is neutral.")

            st.markdown(" ".join(suggestion))
            st.caption("(*These suggestions are rule-based and for educational purposes. Always research thoroughly before investing!*)")

with st.expander("About QuantPilot"):
    st.markdown("""
    <b>QuantPilot</b> empowers investors with:
    - Beautiful, interactive candlestick charts
    - Moving averages (SMA & EMA)
    - Volatility and momentum insights
    - Volume data
    - Downloadable CSVs
    - Clear, plain-English insights
    - Multi-ticker support!
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; font-family:'EB Garamond',serif; font-size:1.11rem; color:#888;">
        &copy; 2025 QuantPilot. All rights reserved.
    </div>
    """, unsafe_allow_html=True)