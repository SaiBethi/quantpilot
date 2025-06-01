import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="QuantPilot: Robinhood LEGEND", layout="wide")

# Custom CSS for Robinhood/fintech look
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
    h1, h2, h3, h4, h5, h6, .stMarkdown, .indicator-card, .ai-suggestion, .stat-table, .copyright-text, .el-garamond {
        font-family: 'EB Garamond', serif !important;
        color: #e0e0e0 !important;
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
    .rh-search {
        background: rgba(18,36,58,0.75);
        border-radius: 1.2em;
        border: 1.5px solid #20344e;
        padding: 0.35em 1em;
        font-size: 1.08em;
        color: #e0e0e0;
        width: 270px;
        font-family: 'EB Garamond',serif;
    }
    .rh-sidebar {
        background: #091522;
        min-width: 74px;
        max-width: 74px;
        height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 2.6em;
        border-right: 1.5px solid #12243a;
        position: fixed;
        z-index: 11;
        top: 0;
        left: 0;
    }
    .rh-nav-icon {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.18em;
        margin: 1.2em 0;
        cursor: pointer;
        border-left: 4px solid transparent;
        padding-left: 0.6em;
        transition: all 0.19s;
    }
    .rh-nav-icon.active, .rh-nav-icon:hover {
        border-color: #00c805;
        background: #13243a;
    }
    .rh-nav-label {
        font-size: 0.92em;
        color: #e0e0e0;
        font-family: 'EB Garamond',serif;
        margin-top: 0.09em;
    }
    .avatar {
        width: 38px; height: 38px;
        border-radius: 50%;
        background: linear-gradient(135deg,#00c805 0%,#0c1b2a 100%);
        display: flex; align-items: center; justify-content: center;
        border: 2px solid #12243a;
        transition: box-shadow 0.20s;
    }
    .avatar:hover { box-shadow: 0 0 0 3px #00c80544; }
    .stat-card {
        background: #12243a;
        border-radius: 0.9em;
        box-shadow: 0 2px 8px #0003;
        padding: 1.1em 1em 0.8em 1em;
        text-align: center;
        margin-bottom: 0.9em;
        border: 1.5px solid #1b2f44;
        transition: transform 0.13s, box-shadow 0.16s;
        font-family: 'EB Garamond',serif;
    }
    .stat-card:hover { transform: translateY(-4px) scale(1.025); box-shadow: 0 6px 18px #00c80522; }
    .stat-label { color: #7db5a8; font-weight: 600; font-size:1em;}
    .stat-value { color: #e0e0e0; font-size:1.32em; font-weight: 700;}
    ::placeholder { color: #7db5a8 !important; opacity: 1 !important; }
    </style>
""", unsafe_allow_html=True)

# --- Navbar ---
st.markdown("""
<div class="rh-navbar">
    <div style="display:flex;align-items:center;gap:0.42em;">
        <svg width="36" height="36" fill="#00c805" style="margin-right:0.21em;"><polygon points="17,6 29,30 5,30" /></svg>
        <span class="logo-text">QuantPilot</span>
    </div>
    <input class="rh-search" placeholder="Search stocks or tickers"/>
    <div class="avatar" title="Profile">
        <svg width="24" height="24" fill="#e0e0e0"><circle cx="12" cy="8" r="4"/><ellipse cx="12" cy="17" rx="7" ry="5"/></svg>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar (left fixed, icons) ---
sidebar_icons = [
    ("Home", "M3 12L12 4l9 8v8a2 2 0 0 1-2 2h-2a2 2 0 0 1-2-2v-4H9v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-8z"),
    ("Portfolio", "M3 7h18v13a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7z"),
    ("Cash", "M4 6h16v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6z"),
    ("Markets", "M4 17V7h3v10H4zm6 0V3h3v14h-3zm6 0v-7h3v7h-3z"),
    ("News", "M3 6h18v12a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6z")
]
st.markdown('<div class="rh-sidebar">' + "".join([
    f'''<div class="rh-nav-icon{' active' if i==0 else ''}"><svg width="24" height="24" fill="none" style="margin-bottom:0.12em;"><path d="{icon}" stroke="#e0e0e0" stroke-width="2"/></svg>
    <span class="rh-nav-label">{label}</span></div>''' for i, (label, icon) in enumerate(sidebar_icons)
]) + '</div>', unsafe_allow_html=True)

# Use columns to offset sidebar for main content
st.markdown('<div style="margin-left:74px;padding-top:2.7em"></div>', unsafe_allow_html=True)

# --- MAIN CONTENT ---
# --- Stock selection UI ---
if "analyze" not in st.session_state or not st.session_state["analyze"]:
    with st.form("stock_select_form", clear_on_submit=False):
        st.markdown("<h2 style='font-size:1.32em;color:#00c805;'>Choose stocks & your dashboard options</h2>", unsafe_allow_html=True)
        tickers = st.text_input("Enter stock tickers (comma separated, e.g. AAPL, TSLA, MSFT)", value="AAPL, TSLA")
        start = st.date_input("Start date", pd.to_datetime("2023-01-01"))
        end = st.date_input("End date", pd.to_datetime("today"))
        interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)
        col1, col2 = st.columns([1,1])
        with col1:
            simulate = st.checkbox("Simulate future growth/projection?")
        with col2:
            years = st.slider("Years to Simulate", 1, 100, 30, 1)
        capital = st.number_input("Your available capital ($):", min_value=0.0, step=100.0, value=1000.0)
        shares_owned = st.number_input("Your number of shares owned:", min_value=0, step=1, value=0)
        st.markdown("""
        <div class="el-garamond" style="font-size:1.12em; color:#ffd700; margin:0.8em 0 0.2em 0; text-align:center;">
            Your dashboard will visualize price, trend, momentum, risk, volume, and AI insights for your selected stocks.
        </div>
        """, unsafe_allow_html=True)
        submit = st.form_submit_button("Get Data & Analyze", type="primary")
    if submit:
        st.session_state["analyze"] = True
        st.session_state["tickers"] = [s.strip().upper() for s in tickers.split(",") if s.strip()]
        st.session_state["start"] = start
        st.session_state["end"] = end
        st.session_state["interval"] = interval
        st.session_state["simulate"] = simulate
        st.session_state["years"] = years
        st.session_state["capital"] = capital
        st.session_state["shares_owned"] = shares_owned
        st.experimental_rerun()
    st.stop()

tickers = st.session_state["tickers"]
start = st.session_state["start"]
end = st.session_state["end"]
interval = st.session_state["interval"]
simulate = st.session_state["simulate"]
years = st.session_state["years"]
capital = st.session_state["capital"]
shares_owned = st.session_state["shares_owned"]

@st.cache_data(show_spinner=True)
def get_data(tickers, start, end, interval):
    return yf.download(tickers, start=start, end=end, interval=interval, group_by="ticker", auto_adjust=True)

data = get_data(tickers, start, end, interval)

def safe_number(val):
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

def rsi(series, period=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    avg_gain = up.rolling(window=period, min_periods=period).mean()
    avg_loss = down.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def obv(close, volume):
    direction = np.sign(close.diff()).fillna(0)
    return (volume * direction).cumsum()

# --- Top Movers Bar ---
def get_top_movers(data, tickers):
    movers = []
    for ticker in tickers:
        close_col = f"Close_{ticker}" if f"Close_{ticker}" in data.columns else f"{ticker}_Close"
        if close_col in data.columns and data[close_col].notna().sum() > 1:
            last = data[close_col].dropna().iloc[-1]
            prev = data[close_col].dropna().iloc[-2]
            pct = ((last - prev) / prev) * 100
            movers.append((ticker, pct, last))
    return sorted(movers, key=lambda x: -abs(x[1]))  # abs for biggest swings

top_movers = get_top_movers(data, tickers)
if top_movers:
    st.markdown("""
    <div class="el-garamond" style='background:#191919;padding:0.57em 1.1em 0.6em 1.1em;margin-bottom:1em;border-radius:1em;border:1.5px solid #222;font-size:1.13em;box-shadow:0 2px 8px #0002;display:flex;flex-wrap:wrap;gap:1.4em;'>
        <span style='color:#ffd700;font-weight:600;'>Top Movers Today:</span>
    """, unsafe_allow_html=True)
    for ticker, pct, last in top_movers:
        color = "#00c805" if pct > 0 else "#ff4c4c"
        st.markdown(
            f"<span style='margin-right:1.7em;'><b>{ticker}</b>: <span style='color:{color};'>{last:.2f} ({pct:+.2f}%)</span></span>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# --- Dashboard Grid for Each Stock ---
if isinstance(data.columns, pd.MultiIndex):
    data.columns = ["_".join([str(i) for i in col if i]) for col in data.columns.values]

for ticker in tickers:
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
    df['RSI'] = rsi(df[close_col])
    macd_line, signal_line, macd_hist = macd(df[close_col])
    df['MACD'] = macd_line
    df['MACD_Signal'] = signal_line
    df['MACD_Hist'] = macd_hist
    df['OBV'] = obv(df[close_col], df[vol_col])

    st.markdown(f"<div class='el-garamond' style='font-size:1.22em;margin-top:1.1em;margin-bottom:0.4em;'><b>{ticker}</b> — <span style='color:#ffd700;'>Market Analysis</span></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='stat-card'><div class='stat-label'>Price (Candlestick)</div>", unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index, open=df[open_col], high=df[high_col], low=df[low_col], close=df[close_col],
            name='Candlestick'
        ))
        for m,col in [("MA20",'cyan'),("MA50",'#00c805'),("MA100",'#aaa'),("MA200",'#fff')]:
            fig.add_trace(go.Scatter(x=df.index, y=df[m], name=m, line=dict(color=col, width=1, dash="dot")))
        fig.update_layout(margin=dict(l=0,r=0,t=10,b=10),height=180,template="plotly_dark",showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='stat-card'><div class='stat-label'>Volume</div>", unsafe_allow_html=True)
        st.bar_chart(df[vol_col], use_container_width=True)
        st.markdown("<div class='stat-card'><div class='stat-label'>RSI (14d)</div>", unsafe_allow_html=True)
        st.line_chart(df['RSI'], use_container_width=True)
    with c3:
        st.markdown("<div class='stat-card'><div class='stat-label'>Daily % Change</div>", unsafe_allow_html=True)
        st.line_chart(df['Daily % Change'], use_container_width=True)
        st.markdown("<div class='stat-card'><div class='stat-label'>Volatility (20d)</div>", unsafe_allow_html=True)
        st.line_chart(df['Volatility (20d)'], use_container_width=True)
    with c4:
        st.markdown("<div class='stat-card'><div class='stat-label'>MACD</div>", unsafe_allow_html=True)
        mfig = go.Figure()
        mfig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name="MACD", line=dict(color="#00c805")))
        mfig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], name="Signal", line=dict(color="#e0e0e0")))
        mfig.add_trace(go.Bar(x=df.index, y=df['MACD_Hist'], name="Histogram", marker_color="#aaf"))
        mfig.update_layout(template="plotly_dark",margin=dict(l=0,r=0,t=8,b=8),height=120,showlegend=False)
        st.plotly_chart(mfig, use_container_width=True)
        st.markdown("<div class='stat-card'><div class='stat-label'>OBV (On-Balance Volume)</div>", unsafe_allow_html=True)
        st.line_chart(df['OBV'], use_container_width=True)

    # --- Key Stats + AI Suggestion Split ---
    left, right = st.columns([1.5, 1.5], gap="large")
    with left:
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
        st.download_button(
            label="Download data as CSV",
            data=df.to_csv().encode(),
            file_name=f"{ticker}_{start}_{end}.csv",
            mime="text/csv",
        )

    with right:
        st.markdown("<div class='ai-suggestion'><b>🤖 AI-Powered Trading Suggestion</b></div>", unsafe_allow_html=True)
        ai_text = []
        ma_short, ma_med, ma_long = df['MA20'].dropna(), df['MA50'].dropna(), df['MA200'].dropna()
        verdict, safe_pct, risky_pct = "HOLD", 0, 0
        latest_close = df[close_col].dropna().iloc[-1]
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
        recent_volatility = df['Volatility (20d)'].dropna().iloc[-1]
        avg_volatility = df['Volatility (20d)'].dropna().mean()
        if recent_volatility and avg_volatility:
            if recent_volatility > 1.2 * avg_volatility:
                ai_text.append("⚡ Volatility is HIGH: Expect major price swings.")
            elif recent_volatility < 0.8 * avg_volatility:
                ai_text.append("🔕 Volatility is LOW: Market is calm.")
            else:
                ai_text.append("📏 Volatility is moderate.")
        latest_mom = df['Daily % Change'].dropna().iloc[-1]
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

        verdict_color = {"BUY": "#00c805", "SELL": "#ff4c4c", "HOLD": "#ffe48a"}
        st.markdown(
            f"<div class='el-garamond' style='margin-top:0.8em; font-size:1.19em;'><b>Final Verdict: "
            f"<span style='color:{verdict_color[verdict]}'>{verdict}</span></b></div>",
            unsafe_allow_html=True
        )

        min_capital = max(100, latest_close) * 2
        capital_help = f"(Recommended: Enter at least ${min_capital:.2f}. Each share ≈ ${latest_close:.2f})"
        shares_help = f"(Recommended: Enter at least 2 shares. Each share ≈ ${latest_close:.2f})"

        allocation_block = ""
        if verdict == "BUY":
            st.markdown(
                f"<span class='el-garamond' style='font-size:1.02em; margin-bottom:0.1em; display:block; color:#fff;'>{capital_help}</span>",
                unsafe_allow_html=True
            )
            if capital >= latest_close * 2:
                safe_num = int((capital * safe_pct) // latest_close)
                risky_num = int((capital * risky_pct) // latest_close)
                allocation_block = (
                    f"<b>Safe allocation:</b> {int(safe_pct * 100)}% – <b>Buy <span style='color:#00c805'>{safe_num}</span> shares</b><br>"
                    f"<b>Risky allocation:</b> {int(risky_pct * 100)}% – <b>Buy <span style='color:#ff4c4c'>{risky_num}</span> shares</b>"
                )
            else:
                allocation_block = f"Enter at least ${min_capital:.2f} capital to see recommended shares to buy."
        elif verdict == "SELL":
            st.markdown(
                f"<span class='el-garamond' style='font-size:1.02em; margin-bottom:0.1em; display:block; color:#fff;'>{shares_help}</span>",
                unsafe_allow_html=True
            )
            if shares_owned >= 2:
                safe_num = int(shares_owned * safe_pct)
                risky_num = int(shares_owned * risky_pct)
                allocation_block = (
                    f"<b>Safe allocation:</b> {int(safe_pct * 100)}% – <b>Sell <span style='color:#00c805'>{safe_num}</span> shares</b><br>"
                    f"<b>Risky allocation:</b> {int(risky_pct * 100)}% – <b>Sell <span style='color:#ff4c4c'>{risky_num}</span> shares</b>"
                )
            else:
                allocation_block = f"Enter at least 2 shares owned to see recommended shares to sell."
        else:  # HOLD or unclear
            st.markdown(
                f"<span class='el-garamond' style='font-size:1.02em; margin-bottom:0.1em; display:block; color:#fff;'>{shares_help}</span>",
                unsafe_allow_html=True
            )
            if shares_owned >= 2:
                safe_num = int(shares_owned * safe_pct)
                risky_num = int(shares_owned * risky_pct)
                allocation_block = (
                    f"<b>Safe allocation:</b> {int(safe_pct * 100)}% – <b>Hold <span style='color:#00c805'>{shares_owned - safe_num}</span> shares</b><br>"
                    f"<b>Risky allocation:</b> {int(risky_pct * 100)}% – <b>Hold <span style='color:#ff4c4c'>{shares_owned - risky_num}</span> shares</b>"
                )
            else:
                allocation_block = f"Enter at least 2 shares owned to see recommended shares to hold."

        st.markdown(
            f"<div class='el-garamond' style='font-size:1.09em; margin-top:0.23em; color:#fff;'>{allocation_block}</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div class='el-garamond' style='margin-top:0.7em; color:#fff;'>" + "<br>".join(ai_text) + "</div>",
            unsafe_allow_html=True
        )

        if simulate:
            st.markdown(
                "<div class='el-garamond project-text' style='font-size:1.07em; margin-top:0.8em;'><b>Investment Projection:</b></div>",
                unsafe_allow_html=True
            )
            n = years
            first_price = df[close_col].dropna().iloc[0]
            last_price = df[close_col].dropna().iloc[-1]
            cagr = (last_price / first_price) ** (1 / max(n,1)) - 1
            projected = capital * ((1 + cagr) ** n)
            st.markdown(
                f"<div class='el-garamond project-text' style='font-size:1.15em; color:#fff;'>"
                f"If you'd invested ${capital:,.2f} for <b>{n} years</b>: <span style='color:#00c805; font-size:1.25em;'>${projected:,.2f}</span></div>"
                f"<div class='el-garamond project-text' style='font-size:0.97em; color:#bbb;'>"
                f"Projection uses CAGR from historical price. Past performance ≠ future results."
                f"</div>",
                unsafe_allow_html=True
            )
        st.markdown(
            "<div class='el-garamond' style='font-size:1.02em; color:#ffd700;'>(These suggestions are rule-based and for educational purposes. Always research thoroughly before investing!)</div>",
            unsafe_allow_html=True
        )

st.markdown("""<div class="copyright-text el-garamond">
&copy; 2025 QuantPilot. All rights reserved.
</div>""", unsafe_allow_html=True)