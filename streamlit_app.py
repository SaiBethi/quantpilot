import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="QuantPilot: All-in-One Dashboard", layout="wide")

# --- EB Garamond & Dark BG UI with white inputs and labels ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');
    html, body, [class*="css"], .stApp {
        font-family: 'EB Garamond', serif !important;
        background: #111 !important;
        color: #fff !important;
    }
    .block-container {
        background: #111 !important;
        padding-top: 0.2rem !important;
        padding-right: 2rem;
        padding-left: 2rem;
        color: #fff !important;
    }
    div[data-testid="stSidebar"], .stSidebar {
        background: #181818;
        font-family: 'EB Garamond', serif !important;
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
    .stButton>button, .stDownloadButton>button, .stSelectbox>div, .stTextInput>div>input, .stDateInput>div>input {
        font-family: 'EB Garamond', serif !important;
        font-weight: 600;
        font-size: 1.08rem !important;
        border-radius: 10px;
        background: #222 !important;
        color: #fff !important;
        border: 1.5px solid #444;
        box-shadow: 0 2px 5px rgba(0,0,0,0.18);
        transition: background 0.16s, color 0.16s, box-shadow 0.18s;
        margin-bottom: 0.5em;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background: #333 !important;
        color: #fff !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.35);
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'EB Garamond', serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.01em;
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
    header[data-testid="stHeader"] {
        background: rgba(0,0,0,0) !important;
        height: 0 !important;
        min-height: 0 !important;
        visibility: hidden;
        display: none;
    }
    .fun-legend {
        font-size:1.07em;
        color:#ffd700;
        margin-bottom:0.2em;
    }
    </style>
""", unsafe_allow_html=True)

# Title and subtitle
st.markdown("""
<h1 style='text-align:center; font-size:2.1rem; margin-bottom:0.45em; margin-top:0.1em; color:#fff; font-family:EB Garamond,serif; font-weight:700;'>
📈 QuantPilot: All-in-One Dashboard
</h1>
<div style='text-align:center; font-size:1.11rem; margin-bottom:1.1em; color:#eee; font-family:EB Garamond,serif;'>
    Analytics, interactive charts, and easy-to-understand insights.<br>
    <span style='font-size:1.00rem;'>Clarity for your stocks—no matter your experience level.</span>
</div>
""", unsafe_allow_html=True)

# --- Toggleable fun legend ---
with st.expander("📖 Quick Chart/Factor Legend (what do these mean?)"):
    st.markdown("""
    <div class="fun-legend">
    📈 Candle: Day's price movement<br>
    📊 MAs: Trend (20, 50, 100, 200)<br>
    ⚡ % Chg: Momentum<br>
    🌪 Volatility: Risk<br>
    🔊 Volume: Trading Activity<br>
    🤖 AI: Smart suggestion
    </div>
    """, unsafe_allow_html=True)

if "data_loaded" not in st.session_state:
    st.session_state["data_loaded"] = False

# --- Simulation option ---
simulate = st.checkbox("Simulate future growth/projection?", value=False)
years = 5
if simulate:
    years = st.slider("Years to Simulate", 1, 30, 5, 1)

with st.expander("① Start Here: Select Tickers and Date Range", expanded=True):
    st.markdown(
        "<div style='font-size:1.08em; color:#ffd700; font-family:EB Garamond,serif;'>"
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
    st.session_state["interval"] = interval

st.markdown("<div class='indicator-card'><span class='section-header'>② Indicator Explanations</span><span style='font-size:1.04em;color:#ffd700;'>Hover over icons for quick info. Click above for the full legend!</span></div>", unsafe_allow_html=True)

st.markdown("<span class='section-header'>③ Stock Data & Analysis</span>", unsafe_allow_html=True)

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
                f"<h3 style='margin-top:1.5em; margin-bottom:0.4em; font-family:EB Garamond,serif; color:#fff;'>{ticker}</h3>",
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

            # --- Stat/legend bar just below ticker ---
            last = df.dropna(subset=[close_col])
            if last.empty:
                st.warning("Not enough data to display stats for this ticker.")
                continue
            last_row = last.iloc[-1]
            st.markdown(
                f"""
                <div style="display:flex;gap:1.8em;flex-wrap:wrap;margin-bottom:0.7em;">
                    <div style="min-width:130px;"><span title="Last price" style="color:#ffd700;">📈</span> <b>Price:</b> {safe_fmt(last_row[close_col])}</div>
                    <div style="min-width:130px;"><span title="20-day moving average" style="color:#ffb700;">📊</span> <b>MA20:</b> {safe_fmt(last_row['MA20'])}</div>
                    <div style="min-width:130px;"><span title="50-day moving average" style="color:#ff71ce;">📊</span> <b>MA50:</b> {safe_fmt(last_row['MA50'])}</div>
                    <div style="min-width:130px;"><span title="200-day moving average" style="color:#1affd5;">📊</span> <b>MA200:</b> {safe_fmt(last_row['MA200'])}</div>
                    <div style="min-width:130px;"><span title="Momentum" style="color:#e9ff70;">⚡</span> <b>% Chg:</b> {last_row['Daily % Change']:+.2f}%</div>
                    <div style="min-width:130px;"><span title="Volatility" style="color:#70d6ff;">🌪</span> <b>Vol:</b> {last_row['Volatility (20d)']:.2f}</div>
                    <div style="min-width:130px;"><span title="Volume" style="color:#fff;">🔊</span> <b>Volume:</b> {int(last_row[vol_col]):,}</div>
                </div>
                """, unsafe_allow_html=True
            )

            # --- Chart ---
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
                title=f"{ticker} Price Chart",
                yaxis_title="Price",
                xaxis_title="Date",
                xaxis_rangeslider_visible=False,
                template="plotly_dark",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

            # ---- AI-Powered Trading Suggestion ----
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

            # --- Optional investment simulation ---
            if simulate:
                st.markdown("<div style='font-size:1.07em; font-family:EB Garamond,serif; margin-top:0.8em; color:#ffd700;'><b>Investment Projection:</b></div>", unsafe_allow_html=True)
                # Use CAGR based on price history
                n = years
                first_price = df[close_col].dropna().iloc[0]
                last_price = df[close_col].dropna().iloc[-1]
                cagr = (last_price / first_price) ** (1 / max(n,1)) - 1
                projected = 1000 * ((1 + cagr) ** n)  # for $1000 investment
                st.markdown(
                    f"<div style='font-size:1.15em; color:#fff;'>"
                    f"If you'd invested $1,000 for <b>{n} years</b>: <span style='color:#9cffae; font-size:1.25em;'>${projected:,.2f}</span></div>"
                    f"<div style='font-size:0.97em; color:#bbb;'>"
                    f"Projection uses CAGR from historical price. Past performance ≠ future results."
                    f"</div>",
                    unsafe_allow_html=True
                )

            st.markdown(
                "<div style='margin-top:0.7em; font-family:EB Garamond,serif; color:#fff;'>" + "<br>".join(ai_text) + "</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<div style='font-size:1.02em; color:#ffd700; font-family:EB Garamond,serif;'>(These suggestions are rule-based and for educational purposes. Always research thoroughly before investing!)</div>",
                unsafe_allow_html=True
            )

st.markdown("""
<div style='
    font-family: "EB Garamond", serif; 
    font-size: 1.41em; 
    color: #ffd700; 
    margin-top: 1.4em; 
    margin-bottom: 1.1em; 
    letter-spacing: 0.01em;
    text-shadow: 0 2px 12px #000;
'>
    <b>About QuantPilot</b>
</div>
<div style='
    font-family: "EB Garamond", serif; 
    font-size: 1.13em;
    color: #fff;
    margin-bottom: 0.9em;
'>
    QuantPilot empowers investors with:<br><br>
    <ul style="margin-top:0.2em; margin-bottom:0.5em; font-size:1.09em;">
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