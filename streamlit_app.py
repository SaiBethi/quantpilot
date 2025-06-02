import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

st.set_page_config(page_title="QuantPilot: Robinhood LEGEND", layout="wide")

# --- Global Style: El Garamond, dark, soft shadows, responsive ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');
html, body, .stApp, [class*="css"] {
    font-family: 'EB Garamond', serif !important;
    background: #0c1b2a !important;
    color: #fff !important;
}
.block-container {
    background: #0c1b2a !important;
    color: #fff !important;
    padding-top: 2.5rem !important;
    padding-left: 2vw !important;
    padding-right: 2vw !important;
    max-width: 1250px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}
.stTextInput input,
.stNumberInput input {
    background: #111 !important;
    color: #fff !important;
    border-radius: 0.6em !important;
    border: 1.5px solid #333 !important;
    box-shadow: 0 2px 8px #0006 !important;
    font-size: 1.09em !important;
    font-family: 'EB Garamond', serif !important;
}
.stSelectbox [data-baseweb="select"], .stSelectbox [data-baseweb="select"] * {
    background: #111 !important;
    color: #fff !important;
    font-family: 'EB Garamond', serif !important;
}
[role="listbox"], [data-baseweb="menu"], [data-baseweb="popover"],
[role="option"], [data-baseweb="option"] {
    background: #111 !important;
    color: #fff !important;
}
.stButton>button, .stDownloadButton>button {
    font-weight: 600;
    font-size: 1.09em !important;
    border-radius: 13px;
    background: #12243a !important;
    color: #fff !important;
    border: 1.5px solid #20344e;
    margin-bottom: 0.5em;
    box-shadow: 0 3px 10px #0004;
    transition: background 0.14s, color 0.14s, box-shadow 0.18s;
}
.stButton>button:hover, .stDownloadButton>button:hover {
    background: #18191d !important;
    color: #fff !important;
    box-shadow: 0 3px 18px #00c80533;
}
.rh-card, .metrics-panel, .ma-table, .footer-card {
    background: #18191d !important;
    border-radius: 1.2em;
    box-shadow: 0 2px 18px #0006;
    padding: 1.2em 1em;
    margin-bottom: 1.1em;
}
.rh-spark {
    background: #112 !important;
    border-radius: 1.1em;
    box-shadow: 0 1px 4px #0006;
    padding: 0.7em 0.8em 0.5em 0.8em;
    margin-bottom: 0.5em;
}
.rh-title {
    font-size: 2.1em;
    font-weight: 800;
    color: #fff !important;
    letter-spacing: 0.01em;
    text-align: center;
    margin-bottom: 0.7em;
}
.rh-metric-label {
    font-size: 1.1em;
    font-weight: 700;
    color: #fff;
    opacity: 0.75;
}
.rh-metric-value {
    font-size: 2em;
    font-weight: 800;
    color: #fff;
    margin-bottom: 0.1em;
}
.rh-kpi {
    background: #111 !important;
    border-radius: 1em;
    box-shadow: 0 1px 4px #0006;
    padding: 1em 1.2em;
    margin-bottom: 0.8em;
    text-align: center;
}
.rh-green { color: #00c805 !important; }
.rh-red { color: #ff4c4c !important; }
.ma-table table {
    width: 100%;
    border-collapse: collapse;
    font-size: 1.13em;
    margin-bottom: 0.2em;
}
.ma-table th, .ma-table td {
    padding: 0.55em 1.1em;
    border: none;
}
.ma-table th {
    background: #222;
    color: #fff;
    font-weight: 700;
    text-align: left;
}
.ma-table tr:nth-child(even) td {
    background: #151c2a;
}
.ma-table tr:nth-child(odd) td {
    background: #18191d;
}
.ma-table td {
    color: #fff;
}
@media (max-width: 900px) {
    .block-container {padding-left: 0.5em !important; padding-right: 0.5em !important;}
    .rh-title {font-size: 1.2em;}
    .rh-card, .metrics-panel, .ma-table, .footer-card {padding: 0.7em 0.4em;}
}
</style>
""", unsafe_allow_html=True)

# --- DATA ---
TICKER = "AAPL"
# --- UI: Input Bar (top) ---
col1, col2, col3 = st.columns([1,1,1])
with col1:
    start_str = st.text_input("Start date (YYYY-MM-DD):", value="2023-01-01")
with col2:
    end_str = st.text_input("End date (YYYY-MM-DD):", value=datetime.today().strftime("%Y-%m-%d"))
with col3:
    interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)

try:
    start = pd.to_datetime(start_str).strftime("%Y-%m-%d")
    end = pd.to_datetime(end_str).strftime("%Y-%m-%d")
    data = yf.download(TICKER, start=start, end=end, interval=interval, auto_adjust=True)
    if data.empty:
        st.warning("No data found for AAPL in that range and interval.")
        st.stop()
except Exception:
    st.warning("Please enter valid dates in YYYY-MM-DD format.")
    st.stop()

# --- Calculate Metrics ---
data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA50'] = data['Close'].rolling(window=50).mean()
data['MA100'] = data['Close'].rolling(window=100).mean()
data['MA200'] = data['Close'].rolling(window=200).mean()
data['Daily % Change'] = data['Close'].pct_change()*100
data['Volatility (20d)'] = data['Close'].rolling(window=20).std()
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
data['RSI'] = rsi(data['Close'])
macd_line, signal_line, macd_hist = macd(data['Close'])
data['MACD'] = macd_line
data['MACD_Signal'] = signal_line
data['MACD_Hist'] = macd_hist
data['OBV'] = obv(data['Close'], data['Volume'])
data['Sharpe'] = sharpe_ratio(data['Close'].pct_change().dropna())
data['Drawdown'] = drawdown(data['Close'])

# --- [1] Price Overview (top-left) ---
st.markdown('<div class="rh-title">AAPL Stock Dashboard</div>', unsafe_allow_html=True)
overview = st.container()
with overview:
    price = data['Close'].iloc[-1]
    prev = data['Close'].iloc[-2] if len(data) > 1 else price
    pct = (price - prev) / prev * 100 if prev != 0 else 0
    col_left, col_mid, col_right = st.columns([1.3,2,1])
    with col_left:
        st.markdown('<div class="rh-card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="rh-metric-label">Current Price</div>
        <div class="rh-metric-value">{price:.2f} USD</div>
        <div class="rh-metric-label">Daily %</div>
        <div class="rh-metric-value {'rh-green' if pct>=0 else 'rh-red'}">{pct:+.2f}%</div>
        """, unsafe_allow_html=True)
        # Sparkline
        spark = go.Figure()
        spark.add_trace(go.Scatter(y=data['Close'].tail(30), mode="lines", line=dict(color="#00c805", width=2), name="Price"))
        spark.update_layout(margin=dict(l=0,r=0,t=0,b=0),height=50,template="plotly_dark",xaxis=dict(visible=False),yaxis=dict(visible=False))
        st.plotly_chart(spark, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_mid:
        pass  # Intentional: main chart fills below

# --- [2] Main Chart: Large Candlestick + Volume ---
st.markdown('<div style="display:flex; flex-direction:column; align-items:center;">', unsafe_allow_html=True)
main_chart = go.Figure()
main_chart.add_trace(go.Candlestick(
    x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
    name='Candlestick', increasing_line_color="#00c805", decreasing_line_color="#ff4c4c"
))
for m, col in [("MA20", "cyan"), ("MA50", "#00c805"), ("MA100", "#aaa"), ("MA200", "#fff")]:
    main_chart.add_trace(go.Scatter(x=data.index, y=data[m], name=m, line=dict(color=col, width=1, dash="dot")))
main_chart.update_layout(
    margin=dict(l=10,r=10,t=18,b=10),
    template="plotly_dark",
    height=480,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(family="EB Garamond, serif", size=13)),
)
st.plotly_chart(main_chart, use_container_width=True)
# Volume chart below, matching style
vol_fig = go.Figure()
vol_fig.add_trace(go.Bar(x=data.index, y=data['Volume'], marker_color="#444", name="Volume"))
vol_fig.update_layout(
    margin=dict(l=10, r=10, t=8, b=10),
    template="plotly_dark",
    height=90,
    showlegend=False,
    xaxis=dict(visible=False),
    yaxis=dict(title="Volume", tickfont=dict(size=12, family="EB Garamond, serif"))
)
st.plotly_chart(vol_fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- [3] Metrics Panel: Responsive 2-Col Grid ---
metrics_panel = st.container()
with metrics_panel:
    st.markdown('<div class="metrics-panel">', unsafe_allow_html=True)
    col_left, col_right = st.columns(2)
    # Left Column
    with col_left:
        st.markdown('<div class="rh-card">', unsafe_allow_html=True)
        st.markdown('<b>Drawdown</b>', unsafe_allow_html=True)
        st.line_chart(data['Drawdown'], use_container_width=True)
        st.markdown('<b>Volatility (20d)</b>', unsafe_allow_html=True)
        st.line_chart(data['Volatility (20d)'], use_container_width=True)
        st.markdown('<div class="rh-kpi">', unsafe_allow_html=True)
        st.markdown(f"<div class='rh-metric-label'>Sharpe Ratio</div><div class='rh-metric-value'>{data['Sharpe'] if data['Sharpe'] != '-' else '-'}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    # Right Column
    with col_right:
        st.markdown('<div class="rh-card">', unsafe_allow_html=True)
        st.markdown('<b>RSI (14d)</b>', unsafe_allow_html=True)
        st.line_chart(data['RSI'], use_container_width=True)
        st.markdown('<b>MACD</b>', unsafe_allow_html=True)
        mfig = go.Figure()
        mfig.add_trace(go.Scatter(x=data.index, y=data['MACD'], name="MACD", line=dict(color="#00c805", width=2)))
        mfig.add_trace(go.Scatter(x=data.index, y=data['MACD_Signal'], name="Signal", line=dict(color="#e0e0e0", width=1)))
        mfig.add_trace(go.Bar(x=data.index, y=data['MACD_Hist'], name="Histogram", marker_color="#aaf", opacity=0.35))
        mfig.update_layout(template="plotly_dark",margin=dict(l=0,r=0,t=8,b=8),height=140,showlegend=False)
        st.plotly_chart(mfig, use_container_width=True)
        st.markdown('<b>OBV</b>', unsafe_allow_html=True)
        st.line_chart(data['OBV'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- [4] Moving Averages Table (bottom, full-width) ---
st.markdown('<div class="ma-table rh-card">', unsafe_allow_html=True)
st.markdown("<b>Moving Averages Table</b>", unsafe_allow_html=True)
ma_df = data[['Close', 'MA20', 'MA50', 'MA100', 'MA200']].tail(15).copy()
ma_df.index = ma_df.index.strftime('%Y-%m-%d')
st.markdown(
    ma_df.style
        .set_table_styles([{"selector": "th", "props": [("background", "#222"), ("color", "#fff")]}])
        .apply(lambda x: ['background: #151c2a' if i%2==0 else 'background: #18191d' for i in range(len(x))], axis=1)
        .format(precision=2)
        .to_html(), 
    unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- [5] Footer: Download CSV button bottom-right ---
footer = st.container()
with footer:
    st.markdown('<div class="footer-card" style="display:flex; justify-content:flex-end;">', unsafe_allow_html=True)
    st.download_button(
        label="Download data as CSV",
        data=data.to_csv().encode(),
        file_name=f"AAPL_{start}_{end}.csv",
        mime="text/csv",
        key="download-csv"
    )
    st.markdown('</div>', unsafe_allow_html=True)