import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="QuantPilot: Robinhood LEGEND", layout="wide")

# --- Robinhood/Legend-Style Enhanced CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;600;700&family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"], .stApp {
        background: #0c1b2a !important;
        color: #e0e0e0 !important;
        font-family: 'EB Garamond', 'Inter', serif !important;
    }
    .block-container {
        background: #0c1b2a !important;
        color: #e0e0e0 !important;
    }
    label, .stTextInput label, .stNumberInput label, .stDateInput label, .stSelectbox label, .st-expanderHeader, .stCheckbox>label {
        color: #e0e0e0 !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 1.07em !important;
    }
    .stTextInput>div>input, .stNumberInput>div>input, .stDateInput>div>input, .stSelectbox>div, .stTextArea textarea {
        background: #162033 !important;
        color: #fff !important;
        border: 1.5px solid #20344e !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 1.09em !important;
    }
    .stTextInput>div>input::placeholder {
        color: #7db5a8 !important;
        opacity: 1 !important;
        font-family: 'EB Garamond', serif !important;
    }
    .stButton>button, .stDownloadButton>button {
        font-family: 'EB Garamond', serif !important;
        font-weight: 600;
        font-size: 1.08em !important;
        border-radius: 11px;
        background: #12243a !important;
        color: #fff !important;
        border: 1.5px solid #20344e;
        margin-bottom: 0.5em;
        transition: background 0.14s, color 0.14s, box-shadow 0.18s;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background: #00c805 !important;
        color: #0c1b2a !important;
        box-shadow: 0 3px 12px #00c80522;
    }
    .rh-legend-header {
        font-family: 'EB Garamond', serif !important;
        background: #18191d;
        border-radius: 1.2em;
        margin-top: 0.8em;
        margin-bottom: 1.2em;
        padding: 0.6em 0 0.4em 0;
        color: #fff;
        box-shadow: 0 2px 10px #0002;
        text-align: center;
        font-size: 2.15em;
        letter-spacing: 0.01em;
        font-weight: 800;
    }
    .rh-quick-legend {
        font-family: 'EB Garamond', serif !important;
        font-size: 1.11em;
        color: #ffd700;
        text-align: center;
        margin-bottom: 0.6em;
    }
    .indicator-card, .stat-card, .ai-suggestion {
        font-family: 'EB Garamond', serif !important;
        border-radius: 1em;
        box-shadow: 0 2px 8px #0003;
        margin-bottom: 1.1em;
        border: 1.5px solid #20344e;
    }
    .indicator-card {
        background: #18191d !important;
        padding: 1em 1.4em;
        font-size: 1.14em;
        color: #e0e0e0 !important;
    }
    .stat-card {
        background: #12243a !important;
        padding: 1.1em 1em 0.8em 1em;
        text-align: center;
        margin-bottom: 0.9em;
    }
    .stat-label { color: #7db5a8; font-weight: 600; font-size:1em;}
    .stat-value { color: #e0e0e0; font-size:1.32em; font-weight: 700;}
    .ai-suggestion {
        background: #1a1a1a !important;
        border: 1.5px solid #00c805;
        font-size: 1.16em;
        font-weight: 500;
        padding: 1.2em 1.5em;
        margin: 0.7em 0 1.3em 0;
        color: #fff !important;
    }
    .section-header {
        font-size: 1.55em !important;
        margin-top: 1em !important;
        margin-bottom: 0.6em !important;
        font-family: 'EB Garamond', serif !important;
        font-weight: 700 !important;
        color: #fff !important;
        letter-spacing: 0.01em;
    }
    .stat-table {
        width: 100%;
        border-collapse: collapse;
        margin: 0.5em 0 1.1em 0;
        font-size: 1.13em;
        color: #fff !important;
        font-family: 'EB Garamond', serif !important;
    }
    .stat-table th, .stat-table td {
        border: none;
        text-align: left;
        padding: 0.27em 1em 0.27em 0;
        vertical-align: middle;
        color: #fff !important;
        font-family: 'EB Garamond', serif !important;
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
        font-size:1.12em;
        margin-top:2.5em;
        margin-bottom:1em;
        font-family:'EB Garamond',serif !important;
    }
    @media (max-width: 900px) {
        .block-container, .main {padding-left: 1.1em !important;}
        .rh-legend-header {font-size: 1.18em;}
        .indicator-card, .stat-card, .ai-suggestion {padding: 0.7em 0.6em;}
    }
    </style>
""", unsafe_allow_html=True)

# --- Robinhood LEGEND Header ---
st.markdown("""
<div class="rh-legend-header">
    <b>QuantPilot</b>
    <span style="color:#00c805;font-size:0.85em;font-weight:700;"> LEGEND</span>
</div>
""", unsafe_allow_html=True)

# --- Quick Legend (EB Garamond, one sentence, professional) ---
with st.expander("📖 Quick Chart/Factor Legend"):
    st.markdown("""
    <div class="rh-quick-legend">
        📈 Candle: Price moves &nbsp;•&nbsp; 📊 MAs: Trend lines &nbsp;•&nbsp; ⚡ % Chg: Daily momentum &nbsp;•&nbsp; 🌪 Volatility: Risk &nbsp;•&nbsp; 🔊 Volume: Trading activity &nbsp;•&nbsp; 🤖 AI: Smart suggestion.
    </div>
    <ul class="el-garamond" style="font-size:1.07em;margin-top:1em;color:#fff;">
        <li><b>📈 Candle:</b> Shows daily price action.</li>
        <li><b>📊 MAs:</b> 20/50/100/200-day moving averages for trend.</li>
        <li><b>⚡ % Chg:</b> Daily price momentum.</li>
        <li><b>🌪 Volatility:</b> 20-day standard deviation (risk/swing).</li>
        <li><b>🔊 Volume:</b> Trading activity.</li>
        <li><b>🤖 AI:</b> Signal and allocation suggestion.</li>
        <li><b>RSI:</b> Relative Strength Index (overbought/oversold).</li>
        <li><b>MACD:</b> Trend change detection.</li>
        <li><b>OBV:</b> On-Balance Volume.</li>
        <li><b>Sharpe:</b> Risk-adjusted performance.</li>
        <li><b>Drawdown:</b> Loss from peak.</li>
    </ul>
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
        years = st.slider("Years to Simulate", 1, 100, 5, 1)
with colc2:
    capital = st.number_input("Your available capital ($):", min_value=0.0, step=100.0, value=1000.0)
    shares_owned = st.number_input("Your number of shares owned:", min_value=0, step=1, value=0)

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

def sharpe_ratio(returns, risk_free=0):
    mean_ret = returns.mean()
    std_ret = returns.std()
    if std_ret == 0 or np.isnan(std_ret): return "-"
    return (mean_ret - risk_free) / std_ret

def drawdown(close):
    roll_max = close.cummax()
    dd = (close - roll_max)/roll_max
    return dd

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
            df['RSI'] = rsi(df[close_col])
            macd_line, signal_line, macd_hist = macd(df[close_col])
            df['MACD'] = macd_line
            df['MACD_Signal'] = signal_line
            df['MACD_Hist'] = macd_hist
            df['OBV'] = obv(df[close_col], df[vol_col])
            df['Sharpe'] = sharpe_ratio(df[close_col].pct_change().dropna())
            df['Drawdown'] = drawdown(df[close_col])

            # --- 5-wide grid for a data-rich Robinhood feel ---
            c1, c2, c3, c4, c5 = st.columns(5)
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
                st.markdown("<div class='stat-card'><div class='stat-label'>Drawdown</div>", unsafe_allow_html=True)
                st.line_chart(df['Drawdown'], use_container_width=True)
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
                st.markdown("<div class='stat-card'><div class='stat-label'>Sharpe Ratio</div>", unsafe_allow_html=True)
                st.line_chart(pd.Series([df['Sharpe'].iloc[0]]*len(df), index=df.index), use_container_width=True)
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
            with c5:
                st.markdown("<div class='stat-card'><div class='stat-label'>Moving Avg. Table</div>", unsafe_allow_html=True)
                st.dataframe(df[[close_col, 'MA20','MA50','MA100','MA200','EMA20','EMA50','EMA100','EMA200']].tail(15), use_container_width=True, height=300)

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
                <tr><th>Sharpe Ratio</th><td>{df['Sharpe'].iloc[0] if df['Sharpe'].iloc[0] != '-' else '-'}</td></tr>
                <tr><th>Max Drawdown</th><td>{df['Drawdown'].min():.2%}</td></tr>
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

                if verdict == "BUY":
                    safe_pct = 0.3
                    risky_pct = 0.6 if recent_volatility < 1.2 * avg_volatility else 0.3
                elif verdict == "SELL":
                    safe_pct = 0.3
                    risky_pct = 0.7 if recent_volatility > 1.2 * avg_volatility else 0.45
                else:
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
                else:
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

with st.expander("About QuantPilot"):
    st.markdown("""
    <div class='el-garamond' style='font-size:1.17em;color:#fff;'>
    QuantPilot empowers investors with:
    <ul style="margin-top:0.3em; margin-bottom:0.8em; font-size:1.09em;">
        <li>Beautiful, interactive candlestick charts</li>
        <li>Moving averages (SMA &amp; EMA)</li>
        <li>Volatility and momentum insights</li>
        <li>Volume data and OBV</li>
        <li>Sharpe ratio and drawdown analysis</li>
        <li>Downloadable CSVs</li>
        <li>Clear, plain-English insights</li>
        <li>Multi-ticker support!</li>
        <li>Responsive, fintech-inspired UI</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""<div class="copyright-text el-garamond">
&copy; 2025 QuantPilot. All rights reserved.
</div>""", unsafe_allow_html=True)