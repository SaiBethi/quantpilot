import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="QuantPilot: All-in-One Dashboard", layout="wide")

# --- Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;600;700&display=swap');
    html, body, [class*="css"], .stApp {
        font-family: 'EB Garamond', serif !important;
        background: #111 !important;
        color: #fff !important;
    }
    .block-container {
        background: #111 !important;
        color: #fff !important;
    }
    label, .stTextInput label, .stNumberInput label, .stDateInput label, .stSelectbox label, .st-expanderHeader {
        color: #fff !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 1.04em !important;
    }
    .stTextInput>div>input, .stNumberInput>div>input, .stDateInput>div>input {
        background: #222 !important;
        color: #fff !important;
        border: 1.5px solid #444 !important;
        font-family: 'EB Garamond', serif !important;
    }
    .stSelectbox>div {
        background: #222 !important;
        color: #fff !important;
        border: 1.5px solid #444 !important;
        font-family: 'EB Garamond', serif !important;
    }
    .stTextInput>div>input::placeholder {
        color: #bbb !important;
        opacity: 1 !important;
        font-family: 'EB Garamond', serif !important;
    }
    .stButton>button, .stDownloadButton>button {
        font-family: 'EB Garamond', serif !important;
        font-weight: 600;
        font-size: 1.08rem !important;
        border-radius: 10px;
        background: #222 !important;
        color: #fff !important;
        border: 1.5px solid #444;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background: #333 !important;
        color: #fff !important;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'EB Garamond', serif !important;
        font-weight: 700 !important;
        color: #fff !important;
    }
    .stMarkdown, .indicator-card, .ai-suggestion, .stat-table {
        font-family: 'EB Garamond', serif !important;
        color: #fff !important;
    }
    .indicator-card {
        background: #191919 !important;
        border-radius: 1em;
        padding: 1.1em 1.5em;
        margin: 0.7em 0 1.1em 0;
        box-shadow: 0 2px 8px rgba(20,20,20,0.23);
        border: 1.5px solid #333;
        font-size: 1.13em;
        color: #fff !important;
    }
    .ai-suggestion {
        background: #1a1a1a !important;
        border-radius: 1em;
        padding: 1em 1.5em;
        margin: 0.7em 0 1.3em 0;
        box-shadow: 0 2px 8px rgba(40,40,40,0.19);
        border: 1.5px solid #333;
        font-size: 1.13em;
        font-weight: 500;
        color: #fff !important;
    }
    .section-header {
        font-size: 1.75em !important;
        margin-top: 1.1em !important;
        margin-bottom: 0.6em !important;
        font-family: 'EB Garamond', serif !important;
        font-weight: 700 !important;
        color: #fff !important;
        letter-spacing: 0.01em;
    }
    .stat-table {
        width: 100%;
        border-collapse: collapse;
        margin: 0.7em 0 1.3em 0;
        font-size: 1.13em;
        color: #fff !important;
    }
    .stat-table th, .stat-table td {
        border: none;
        text-align: left;
        padding: 0.37em 1.3em 0.37em 0;
        vertical-align: middle;
        font-family: 'EB Garamond', serif !important;
        color: #fff !important;
    }
    .stat-table th {
        color: #ffdc8f !important;
        font-weight: 700;
        background: none;
    }
    .stat-table td {
        color: #fff !important;
    }
    .project-text {
        color: #fff !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 1.13em !important;
    }
    .copyright-text {
        text-align:center;
        color:#888;
        font-size:0.99em;
        margin-top:2.5em;
        font-family:'EB Garamond',serif !important;
    }
    .el-garamond {
        font-family:'EB Garamond',serif !important;
        color:#fff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- QuantPilot LEGEND header ---
st.markdown("""
<div style='
    font-family:EB Garamond,serif;
    background:#18191d;
    border-radius:18px;
    margin-top:0.75em;
    margin-bottom:1.2em;
    padding:0.6em 0 0.4em 0;
    color:#fff;
    box-shadow:0 2px 10px #0002;
    text-align:center;
    font-size:2.1em;
    letter-spacing:0.02em;'>
    <b>QuantPilot</b>
    <span style="color:#1db954;font-size:0.85em;font-weight:600;"> LEGEND</span>
</div>
""", unsafe_allow_html=True)

# --- Quick Legend (El Garamond, one sentence) ---
with st.expander("📖 Quick Chart/Factor Legend"):
    st.markdown("""
    <div style="font-family:'EB Garamond',serif;font-size:1.12em;color:#ffd700;">
        📈 Candle: Shows price moves; 📊 MAs: Trend lines; ⚡ % Chg: Daily momentum; 🌪 Volatility: Risk; 🔊 Volume: Trading activity; 🤖 AI: Smart suggestion.
    </div>
    """, unsafe_allow_html=True)

# --- Data input expander ---
if "data_loaded" not in st.session_state:
    st.session_state["data_loaded"] = False

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

if st.button("Get Data & Analyze", key="getdata"):
    st.session_state["data_loaded"] = True
    st.session_state["stock_data"] = yf.download(
        tickers, start=start, end=end, interval=interval, group_by='ticker', auto_adjust=True
    )
    st.session_state["tickers"] = tickers
    st.session_state["start"] = start
    st.session_state["end"] = end
    st.session_state["interval"] = interval

# --- Simulation and capital/shares entry ---
st.markdown("<span class='section-header'>② Options</span>", unsafe_allow_html=True)
colc1, colc2 = st.columns([1,1])
with colc1:
    simulate = st.checkbox("Simulate future growth/projection?", value=False)
    years = 5
    if simulate:
        years = st.slider("Years to Simulate", 1, 30, 5, 1)
with colc2:
    capital = st.number_input("Your available capital ($):", min_value=0.0, step=100.0, value=1000.0)
    shares_owned = st.number_input("Your number of shares owned:", min_value=0, step=1, value=0)

def safe_number(val):
    """Return a float if val is a Series or single value, else '-' for NaN or errors."""
    try:
        if isinstance(val, pd.Series):
            val = val.iloc[0]
        if pd.isnull(val):
            return "-"
        return float(val)
    except Exception:
        return "-"

def safe_fmt(val, prefix="$"):
    v = safe_number(val)
    if v == "-":
        return "-"
    return f"{prefix}{v:,.2f}"

st.markdown("<span class='section-header'>③ Stock Data & Analysis</span>", unsafe_allow_html=True)
if st.session_state["data_loaded"]:
    data = st.session_state["stock_data"]
    tickers = st.session_state["tickers"]
    start = st.session_state["start"]
    end = st.session_state["end"]
    interval = st.session_state["interval"]
    if data.empty:
        st.error("No data found for these tickers in the selected date range.")
        st.session_state["data_loaded"] = False
    else:
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = ["_".join([str(i) for i in col if i]) for col in data.columns.values]
        for ticker in tickers:
            st.markdown(
                f"<h3 style='margin-top:1.2em; margin-bottom:0.4em; font-family:EB Garamond,serif; color:#fff;'>{ticker}</h3>",
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
            df['MA20'] = df[close_col].rolling(window=20).mean()
            df['MA50'] = df[close_col].rolling(window=50).mean()
            df['MA100'] = df[close_col].rolling(window=100).mean()
            df['MA200'] = df[close_col].rolling(window=200).mean()
            df['EMA20'] = df[close_col].ewm(span=20, adjust=False).mean()
            df['EMA50'] = df[close_col].ewm(span=50, adjust=False).mean()
            df['EMA100'] = df[close_col].ewm(span=100, adjust=False).mean()
            df['EMA200'] = df[close_col].ewm(span=200, adjust=False).mean()
            df['Daily % Change'] = df[close_col].pct_change()*100
            df['Volatility (20d)'] = df[close_col].rolling(window=20).std()

            # --- Split graphs in a 2x2 grid ---
            gcol1, gcol2 = st.columns([2.2, 1.8], gap="large")
            with gcol1:
                # Top left: Price Chart & Indicators
                st.markdown("<div class='indicator-card'><b>📊 Price Chart & Indicators</b></div>", unsafe_allow_html=True)
                fig = go.Figure()
                fig.add_trace(go.Candlestick(
                    x=df.index, open=df[open_col], high=df[high_col], low=df[low_col], close=df[close_col],
                    name='Candlestick'
                ))
                fig.add_trace(go.Scatter(
                    x=df.index, y=df["MA20"], line=dict(color='cyan', width=1), name="MA20"
                ))
                fig.add_trace(go.Scatter(
                    x=df.index, y=df["MA50"], line=dict(color='#ffb700', width=1), name="MA50"
                ))
                fig.add_trace(go.Scatter(
                    x=df.index, y=df["MA100"], line=dict(color='#aaa', width=1, dash="dot"), name="MA100"
                ))
                fig.add_trace(go.Scatter(
                    x=df.index, y=df["MA200"], line=dict(color='#fff', width=1, dash="dot"), name="MA200"
                ))
                fig.add_trace(go.Scatter(
                    x=df.index, y=df["EMA20"], line=dict(color='#f0c0ff', width=1, dash='dot'), name="EMA20"
                ))
                fig.add_trace(go.Scatter(
                    x=df.index, y=df["EMA50"], line=dict(color='#1aff8e', width=1, dash='dot'), name="EMA50"
                ))
                fig.add_trace(go.Scatter(
                    x=df.index, y=df["EMA100"], line=dict(color='#e38eff', width=1, dash='dot'), name="EMA100"
                ))
                fig.add_trace(go.Scatter(
                    x=df.index, y=df["EMA200"], line=dict(color='#ff7676', width=1, dash='dot'), name="EMA200"
                ))
                fig.update_layout(
                    margin=dict(l=0, r=0, t=18, b=16),
                    height=320,
                    yaxis_title="Price",
                    xaxis_title="Date",
                    xaxis_rangeslider_visible=False,
                    template="plotly_dark",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)

                # Bottom left: Daily Change Momentum
                st.markdown("<div class='indicator-card'><b>⚡️ Daily % Change (Momentum)</b></div>", unsafe_allow_html=True)
                st.line_chart(df['Daily % Change'], use_container_width=True)

                # Key Stats
                st.markdown("<div class='indicator-card'><b>📋 Key Stats for this Period</b>", unsafe_allow_html=True)
                last_row = df.dropna(subset=[close_col]).iloc[-1]
                stat_table = f"""
                <table class="stat-table">
                <tr><th>Latest Close</th><td>${last_row[close_col]:.2f}</td></tr>
                <tr><th>Volume</th><td>{int(last_row[vol_col]):,}</td></tr>
                {"<tr><th>High (period)</th><td>${:.2f}</td></tr>".format(df[high_col].max()) if high_col in df.columns else ""}
                {"<tr><th>Low (period)</th><td>${:.2f}</td></tr>".format(df[low_col].min()) if low_col in df.columns else ""}
                <tr><th>Total Trading Days</th><td>{len(df)}</td></tr>
                <tr><th>Mean Volatility (20d)</th><td>{df['Volatility (20d)'].dropna().mean():.3f}</td></tr>
                <tr><th>Mean Daily % Change</th><td>{df['Daily % Change'].dropna().mean():.3f}%</td></tr>
                </table>
                """
                st.markdown(stat_table, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with gcol2:
                # Top right: Volume Traded
                st.markdown("<div class='indicator-card'><b>🔊 Volume Traded</b></div>", unsafe_allow_html=True)
                st.bar_chart(df[vol_col], use_container_width=True)

                # Bottom right: Volatility
                st.markdown("<div class='indicator-card'><b>📈 Volatility (20d rolling std)</b></div>", unsafe_allow_html=True)
                st.line_chart(df['Volatility (20d)'], use_container_width=True)

                # --- AI-Powered Trading Suggestion & Investment Projection ---
                st.markdown("<div class='ai-suggestion'><b>🤖 AI-Powered Trading Suggestion</b><br>", unsafe_allow_html=True)
                ai_text = []
                ma_short, ma_med, ma_long = df['MA20'].dropna(), df['MA50'].dropna(), df['MA200'].dropna()
                verdict, safe_pct, risky_pct = "HOLD", 0, 0
                latest_close = last_row[close_col]
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
                recent_volatility = last_row['Volatility (20d)']
                avg_volatility = df['Volatility (20d)'].dropna().mean()
                if recent_volatility and avg_volatility:
                    if recent_volatility > 1.2 * avg_volatility:
                        ai_text.append("⚡ Volatility is HIGH: Expect major price swings.")
                    elif recent_volatility < 0.8 * avg_volatility:
                        ai_text.append("🔕 Volatility is LOW: Market is calm.")
                    else:
                        ai_text.append("📏 Volatility is moderate.")
                # --- Momentum
                latest_mom = last_row['Daily % Change']
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

                verdict_color = {"BUY": "#9cffae", "SELL": "#ff8686", "HOLD": "#ffe48a"}
                st.markdown(
                    f"<div style='margin-top:0.8em; font-size:1.19em; font-family:EB Garamond,serif;'><b>Final Verdict: "
                    f"<span style='color:{verdict_color[verdict]}'>{verdict}</span></b></div>",
                    unsafe_allow_html=True
                )

                # --- Capital/shares allocation ---
                min_capital = max(100, latest_close) * 2  # at least two shares
                capital_help = f"(Recommended: Enter at least ${min_capital:.2f} for meaningful allocation. Each share ≈ ${latest_close:.2f})"
                shares_help = f"(Recommended: Enter at least 2 shares for visible allocation. Each share ≈ ${latest_close:.2f})"

                allocation_block = ""
                if verdict == "BUY":
                    st.markdown(
                        f"<span style='font-family:EB Garamond,serif; font-size:1.02em; margin-bottom:0.1em; display:block; color:#fff;'>{capital_help}</span>",
                        unsafe_allow_html=True
                    )
                    if capital >= latest_close * 2:
                        safe_num = int((capital * safe_pct) // latest_close)
                        risky_num = int((capital * risky_pct) // latest_close)
                        allocation_block = (
                            f"<b>Safe allocation:</b> {int(safe_pct * 100)}% &rarr; <b>Buy <span style='color:#9cffae'>{safe_num}</span> shares</b><br>"
                            f"<b>Risky allocation:</b> {int(risky_pct * 100)}% &rarr; <b>Buy <span style='color:#ff8686'>{risky_num}</span> shares</b>"
                        )
                    else:
                        allocation_block = f"Enter at least ${min_capital:.2f} capital to see recommended shares to buy."
                elif verdict == "SELL":
                    st.markdown(
                        f"<span style='font-family:EB Garamond,serif; font-size:1.02em; margin-bottom:0.1em; display:block; color:#fff;'>{shares_help}</span>",
                        unsafe_allow_html=True
                    )
                    if shares_owned >= 2:
                        safe_num = int(shares_owned * safe_pct)
                        risky_num = int(shares_owned * risky_pct)
                        allocation_block = (
                            f"<b>Safe allocation:</b> {int(safe_pct * 100)}% &rarr; <b>Sell <span style='color:#9cffae'>{safe_num}</span> shares</b><br>"
                            f"<b>Risky allocation:</b> {int(risky_pct * 100)}% &rarr; <b>Sell <span style='color:#ff8686'>{risky_num}</span> shares</b>"
                        )
                    else:
                        allocation_block = f"Enter at least 2 shares owned to see recommended shares to sell."
                else:  # HOLD or unclear
                    st.markdown(
                        f"<span style='font-family:EB Garamond,serif; font-size:1.02em; margin-bottom:0.1em; display:block; color:#fff;'>{shares_help}</span>",
                        unsafe_allow_html=True
                    )
                    if shares_owned >= 2:
                        safe_num = int(shares_owned * safe_pct)
                        risky_num = int(shares_owned * risky_pct)
                        allocation_block = (
                            f"<b>Safe allocation:</b> {int(safe_pct * 100)}% &rarr; <b>Hold <span style='color:#9cffae'>{shares_owned - safe_num}</span> shares</b><br>"
                            f"<b>Risky allocation:</b> {int(risky_pct * 100)}% &rarr; <b>Hold <span style='color:#ff8686'>{shares_owned - risky_num}</span> shares</b>"
                        )
                    else:
                        allocation_block = f"Enter at least 2 shares owned to see recommended shares to hold."

                st.markdown(
                    f"<div style='font-size:1.09em; margin-top:0.23em; font-family:EB Garamond,serif; color:#fff;'>{allocation_block}</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    "<div style='margin-top:0.7em; font-family:EB Garamond,serif; color:#fff;'>" + "<br>".join(ai_text) + "</div>",
                    unsafe_allow_html=True
                )

                # --- Optional investment simulation ---
                if simulate:
                    st.markdown(
                        "<div class='project-text' style='font-size:1.07em; margin-top:0.8em;'><b>Investment Projection:</b></div>",
                        unsafe_allow_html=True
                    )
                    n = years
                    first_price = df[close_col].dropna().iloc[0]
                    last_price = df[close_col].dropna().iloc[-1]
                    cagr = (last_price / first_price) ** (1 / max(n,1)) - 1
                    projected = capital * ((1 + cagr) ** n)
                    st.markdown(
                        f"<div class='project-text' style='font-size:1.15em; color:#fff;'>"
                        f"If you'd invested ${capital:,.2f} for <b>{n} years</b>: <span style='color:#9cffae; font-size:1.25em;'>${projected:,.2f}</span></div>"
                        f"<div class='project-text' style='font-size:0.97em; color:#bbb;'>"
                        f"Projection uses CAGR from historical price. Past performance ≠ future results."
                        f"</div>",
                        unsafe_allow_html=True
                    )

                st.markdown(
                    "<div style='font-size:1.02em; color:#ffd700; font-family:EB Garamond,serif;'>(These suggestions are rule-based and for educational purposes. Always research thoroughly before investing!)</div>",
                    unsafe_allow_html=True
                )

with st.expander("About QuantPilot"):
    st.markdown("""
    <div style='font-family:"EB Garamond",serif;font-size:1.17em;color:#fff;'>
    QuantPilot empowers investors with:
    <ul style="margin-top:0.3em; margin-bottom:0.8em; font-size:1.09em;">
        <li>Beautiful, interactive candlestick charts</li>
        <li>Moving averages (SMA &amp; EMA)</li>
        <li>Volatility and momentum insights</li>
        <li>Volume data</li>
        <li>Downloadable CSVs</li>
        <li>Clear, plain-English insights</li>
        <li>Multi-ticker support!</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""<div class="copyright-text">
&copy; 2025 QuantPilot. All rights reserved.
</div>""", unsafe_allow_html=True)