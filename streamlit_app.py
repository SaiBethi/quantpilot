import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="QuantPilot: All-in-One Dashboard", layout="wide")

# --- EL Garamond & Enhanced UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');
    html, body, [class*="css"], .stApp {
        font-family: 'EB Garamond', serif !important;
        background: #f8f6f1 !important;
    }
    div[data-testid="stSidebar"], .stSidebar {
        background: #f2ede6;
        font-family: 'EB Garamond', serif !important;
    }
    .stButton>button, .stDownloadButton>button, .stSelectbox>div, .stTextInput>div>input, .stDateInput>div>input {
        font-family: 'EB Garamond', serif !important;
        font-weight: 600;
        font-size: 1.08rem !important;
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
    h1, h2, h3, h4, h5, h6 {
        font-family: 'EB Garamond', serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.01em;
    }
    .stMarkdown, .indicator-card, .ai-suggestion, .stat-table {
        font-family: 'EB Garamond', serif !important;
    }
    .block-container {
        padding-top: 1.2rem;
        padding-right: 2rem;
        padding-left: 2rem;
    }
    .indicator-card {
        background: #fff6ef;
        border-radius: 1em;
        padding: 1.1em 1.5em;
        margin: 0.7em 0 1.1em 0;
        box-shadow: 0 2px 8px rgba(200,180,140,0.07);
        border: 1.5px solid #e7dbc9;
        font-size: 1.13em;
    }
    .ai-suggestion {
        background: #f6f1e7;
        border-radius: 1em;
        padding: 1em 1.5em;
        margin: 0.7em 0 1.3em 0;
        box-shadow: 0 2px 8px rgba(190,170,130,0.09);
        border: 1.5px solid #e7dbc9;
        font-size: 1.13em;
        font-weight: 500;
        color: #5f4100;
    }
    .section-header {
        font-size: 1.75em !important;
        margin-top: 1.4em !important;
        margin-bottom: 0.6em !important;
        font-family: 'EB Garamond', serif !important;
        font-weight: 700 !important;
        color: #543600;
        letter-spacing: 0.01em;
    }
    .stat-table {
        width: 100%;
        border-collapse: collapse;
        margin: 0.7em 0 1.3em 0;
        font-size: 1.13em;
    }
    .stat-table th, .stat-table td {
        border: none;
        text-align: left;
        padding: 0.37em 1.3em 0.37em 0;
        vertical-align: middle;
        font-family: 'EB Garamond', serif !important;
    }
    .stat-table th {
        color: #805400;
        font-weight: 700;
        background: none;
    }
    .stat-table td {
        color: #39322a;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>📈 QuantPilot: All-in-One Dashboard</h1>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; font-size:1.28rem; margin-bottom:1.6em; font-family:EB Garamond,serif;'>
    Level up your investing with <b>QuantPilot</b>: analytics, interactive charts, and easy-to-understand insights.<br>
    <span style='color:#7c6f5c; font-size:1.09rem;'>
    Get clarity on your stocks—no matter your experience level.
    </span>
</div>
""", unsafe_allow_html=True)

if "data_loaded" not in st.session_state:
    st.session_state["data_loaded"] = False

with st.expander("① Start Here: Select Tickers and Date Range", expanded=True):
    st.markdown(
        "<div style='font-size:1.08em; color:#6e5a33; font-family:EB Garamond,serif;'>"
        "Enter tickers, pick your date range, and press <b>Get Data & Analyze</b>."
        "</div>",
        unsafe_allow_html=True
    )
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

if st.button("Get Data & Analyze", key="getdata"):
    st.session_state["data_loaded"] = True
    st.session_state["stock_data"] = yf.download(
        tickers, start=start, end=end, interval=interval, group_by='ticker', auto_adjust=True
    )
    st.session_state["tickers"] = tickers
    st.session_state["start"] = start
    st.session_state["end"] = end

st.markdown("<div class='indicator-card'><span class='section-header'>② Indicator Explanations</span>"
            "<ul style='font-size:1.13em; margin-top:0.5em;'>"
            "<li><b>Candlestick Chart:</b> Shows price open, high, low, and close for each period.</li>"
            "<li><b>Simple Moving Averages (MA20, MA50, MA100, MA200):</b> Averages over 20/50/100/200 periods to show trend direction.</li>"
            "<li><b>Exponential Moving Averages (EMA20, EMA50, EMA100, EMA200):</b> Like SMAs but react faster to recent price changes.</li>"
            "<li><b>Daily % Change:</b> Shows daily momentum (positive = up, negative = down).</li>"
            "<li><b>Volatility (20-day Rolling Std):</b> Measures how much price moves up/down (higher = more volatile).</li>"
            "<li><b>Volume Traded:</b> Number of shares traded each period.</li>"
            "<li><b>AI Suggestion:</b> Combines trend, volatility, and momentum for a final verdict and risk profile.</li>"
            "</ul></div>", unsafe_allow_html=True)

st.markdown("<span class='section-header'>③ Stock Data & Analysis</span>", unsafe_allow_html=True)
if st.session_state["data_loaded"]:
    data = st.session_state["stock_data"]
    tickers = st.session_state["tickers"]
    start = st.session_state["start"]
    end = st.session_state["end"]
    if data.empty:
        st.error("No data found for these tickers in the selected date range.")
        st.session_state["data_loaded"] = False
    else:
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = ["_".join([str(i) for i in col if i]) for col in data.columns.values]
        for ticker in tickers:
            st.markdown(
                f"<h3 style='margin-top:1.5em; margin-bottom:0.4em; font-family:EB Garamond,serif; color:#543600;'>{ticker}</h3>",
                unsafe_allow_html=True
            )
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

            st.markdown("<div class='indicator-card'><b>📊 Price Chart & Indicators</b></div>", unsafe_allow_html=True)
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
                x=df.index, y=df["MA100"], line=dict(color='#999', width=1, dash="dot"), name="MA100"
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
                st.markdown("<div class='indicator-card'><b>Volume Traded</b></div>", unsafe_allow_html=True)
                st.bar_chart(df[vol_col], use_container_width=True)

            # ---- Momentum Chart ----
            st.markdown("<div class='indicator-card'><b>⚡️ Daily % Change (Momentum)</b></div>", unsafe_allow_html=True)
            st.line_chart(df['Daily % Change'])

            # ---- Volatility Chart ----
            st.markdown("<div class='indicator-card'><b>📈 Volatility (20d rolling std)</b></div>", unsafe_allow_html=True)
            st.line_chart(df['Volatility (20d)'])

            # ---- Key Stats ----
            st.markdown("<div class='indicator-card'><b>📋 Key Stats for this Period</b>", unsafe_allow_html=True)
            latest_close = df[close_col].dropna().iloc[-1] if df[close_col].notna().any() else float('nan')
            latest_vol = df[vol_col].dropna().iloc[-1] if vol_col in df.columns and df[vol_col].notna().any() else float('nan')
            stat_table = f"""
            <table class="stat-table">
            <tr><th>Latest Close</th><td>${latest_close:.2f}</td></tr>
            <tr><th>Volume</th><td>{int(latest_vol):,}</td></tr>
            {"<tr><th>High (period)</th><td>${:.2f}</td></tr>".format(df[high_col].max()) if high_col in df.columns else ""}
            {"<tr><th>Low (period)</th><td>${:.2f}</td></tr>".format(df[low_col].min()) if low_col in df.columns else ""}
            <tr><th>Total Trading Days</th><td>{len(df)}</td></tr>
            <tr><th>Mean Volatility (20d)</th><td>{df['Volatility (20d)'].dropna().mean():.3f}</td></tr>
            <tr><th>Mean Daily % Change</th><td>{df['Daily % Change'].dropna().mean():.3f}%</td></tr>
            </table>
            """
            st.markdown(stat_table, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.download_button(
                label="Download data as CSV",
                data=df.to_csv().encode(),
                file_name=f"{ticker}_{start}_{end}.csv",
                mime="text/csv",
            )

            # ---- AI-Powered Trading Suggestion ----
            st.markdown("<div class='ai-suggestion'><b>🤖 AI-Powered Trading Suggestion</b><br>", unsafe_allow_html=True)
            ai_text = []
            ma_short, ma_med, ma_long = df['MA20'].dropna(), df['MA50'].dropna(), df['MA200'].dropna()
            verdict, safe_pct, risky_pct = "HOLD", 0, 0
            if not ma_short.empty and not ma_med.empty and not ma_long.empty:
                if latest_close > ma_short.iloc[-1] and latest_close > ma_med.iloc[-1] and latest_close > ma_long.iloc[-1]:
                    ai_text.append("🚀 All trends (short/medium/long-term) are bullish. Strong uptrend.")
                    verdict = "BUY"
                elif latest_close < ma_short.iloc[-1] and latest_close < ma_med.iloc[-1] and latest_close < ma_long.iloc[-1]:
                    ai_text.append("🔻 All trends are bearish. Strong downtrend.")
                    verdict = "SELL"
                elif latest_close > ma_short.iloc[-1] and latest_close > ma_med.iloc[-1]:
                    ai_text.append("↗️ Short/medium-term trend is bullish.")
                    verdict = "BUY"
                elif latest_close < ma_short.iloc[-1] and latest_close < ma_med.iloc[-1]:
                    ai_text.append("↘️ Short/medium-term trend is bearish.")
                    verdict = "SELL"
                else:
                    ai_text.append("⏸️ Mixed trends. Consider holding or waiting for clarity.")
                    verdict = "HOLD"
            # --- Volatility
            recent_volatility = df['Volatility (20d)'].dropna().iloc[-1] if df['Volatility (20d)'].notna().any() else 0
            avg_volatility = df['Volatility (20d)'].dropna().mean() if df['Volatility (20d)'].notna().any() else 0
            if recent_volatility and avg_volatility:
                if recent_volatility > 1.2 * avg_volatility:
                    ai_text.append("⚡ Volatility is HIGH: Expect major price swings.")
                elif recent_volatility < 0.8 * avg_volatility:
                    ai_text.append("🔕 Volatility is LOW: Market is calm.")
                else:
                    ai_text.append("📏 Volatility is moderate.")
            # --- Momentum
            latest_mom = df['Daily % Change'].dropna().iloc[-1] if df['Daily % Change'].notna().any() else 0
            if latest_mom > 1.5:
                ai_text.append("📈 Strong positive momentum today.")
            elif latest_mom < -1.5:
                ai_text.append("📉 Strong negative momentum today.")
            else:
                ai_text.append("🔄 Momentum is neutral.")

            # --- Final verdict logic
            if verdict == "BUY":
                safe_pct = 0.3
                risky_pct = 0.6 if recent_volatility < 1.2 * avg_volatility else 0.3
            elif verdict == "SELL":
                safe_pct = 0.3
                risky_pct = 0.7 if recent_volatility > 1.2 * avg_volatility else 0.45
            else:  # HOLD or unclear
                safe_pct = 0.1
                risky_pct = 0.2

            verdict_color = {"BUY": "#189c3a", "SELL": "#c12b2b", "HOLD": "#b29c5a"}
            st.markdown(
                f"<div style='margin-top:0.8em; font-size:1.19em; font-family:EB Garamond,serif;'><b>Final Verdict: "
                f"<span style='color:{verdict_color[verdict]}'>{verdict}</span></b></div>",
                unsafe_allow_html=True
            )

            allocation_block = ""
            if verdict == "BUY":
                capital = st.number_input("Your available capital ($):", min_value=0.0, step=100.0, key=f"capital_{ticker}")
                if capital > 0 and latest_close > 0:
                    safe_num = int((capital * safe_pct) // latest_close)
                    risky_num = int((capital * risky_pct) // latest_close)
                    allocation_block = (
                        f"<b>Safe allocation:</b> {int(safe_pct * 100)}% &rarr; <b>Buy <span style='color:#189c3a'>{safe_num}</span> shares</b><br>"
                        f"<b>Risky allocation:</b> {int(risky_pct * 100)}% &rarr; <b>Buy <span style='color:#c12b2b'>{risky_num}</span> shares</b>"
                    )
                else:
                    allocation_block = "Enter your available capital to see recommended shares to buy."
            elif verdict == "SELL":
                shares_owned = st.number_input("Your number of shares owned:", min_value=0, step=1, key=f"shares_{ticker}")
                if shares_owned > 0:
                    safe_num = int(shares_owned * safe_pct)
                    risky_num = int(shares_owned * risky_pct)
                    allocation_block = (
                        f"<b>Safe allocation:</b> {int(safe_pct * 100)}% &rarr; <b>Sell <span style='color:#189c3a'>{safe_num}</span> shares</b><br>"
                        f"<b>Risky allocation:</b> {int(risky_pct * 100)}% &rarr; <b>Sell <span style='color:#c12b2b'>{risky_num}</span> shares</b>"
                    )
                else:
                    allocation_block = "Enter your shares owned to see recommended shares to sell."
            else:  # HOLD or unclear
                shares_owned = st.number_input("Your number of shares owned:", min_value=0, step=1, key=f"shares_{ticker}")
                if shares_owned > 0:
                    safe_num = int(shares_owned * safe_pct)
                    risky_num = int(shares_owned * risky_pct)
                    allocation_block = (
                        f"<b>Safe allocation:</b> {int(safe_pct * 100)}% &rarr; <b>Hold <span style='color:#189c3a'>{shares_owned - safe_num}</span> shares</b><br>"
                        f"<b>Risky allocation:</b> {int(risky_pct * 100)}% &rarr; <b>Hold <span style='color:#c12b2b'>{shares_owned - risky_num}</span> shares</b>"
                    )
                else:
                    allocation_block = "Enter your shares owned to see recommended shares to hold."

            st.markdown(
                f"<div style='font-size:1.09em; margin-top:0.23em; font-family:EB Garamond,serif;'>{allocation_block}</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<div style='margin-top:0.7em; font-family:EB Garamond,serif;'>" + "<br>".join(ai_text) + "</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<div style='font-size:1.02em; color:#a08c64; font-family:EB Garamond,serif;'>(These suggestions are rule-based and for educational purposes. Always research thoroughly before investing!)</div>",
                unsafe_allow_html=True
            )

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