import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="QuantPilot: Robinhood LEGEND", layout="wide")

# --- Custom EB Garamond + Robinhood legend CSS for better centering, soft shadows, white text ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');
    html, body, [class*="css"], .stApp {
        font-family: 'EB Garamond', serif !important;
        background: #0c1b2a !important;
        color: #fff !important;
    }
    .block-container {
        background: #0c1b2a !important;
        color: #fff !important;
        font-family: 'EB Garamond', serif !important;
        padding-top: 2.5rem !important;
        padding-left: 3vw !important;
        padding-right: 3vw !important;
        max-width: 1200px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    *, .stText, .stMarkdown, .stButton>button, .stDownloadButton>button, .stSelectbox>div, .stNumberInput>div>input, .stTextInput>div>input, .stDateInput>div>input, .stDataFrame, .stCheckbox>label, .stExpanderHeader {
        font-family: 'EB Garamond', serif !important;
        color: #fff !important;
        letter-spacing: 0.01em;
    }
    .stButton>button, .stDownloadButton>button {
        font-weight: 600;
        font-size: 1.09em !important;
        border-radius: 13px;
        background: #12243a !important;
        color: #fff !important;
        border: 1.5px solid #20344e;
        margin-bottom: 0.5em;
        transition: background 0.14s, color 0.14s, box-shadow 0.18s;
        box-shadow: 0 3px 10px #0004;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background: #18191d !important;
        color: #fff !important;
        box-shadow: 0 3px 18px #00c80533;
    }
    .dashboard-container {
        background: #0c1b2a !important;
        border-radius: 1.5em;
        box-shadow: 0 4px 24px #0007;
        padding: 1.4em 2.7em 2em 2.7em;
        margin-bottom: 2.5em;
        margin-left: auto;
        margin-right: auto;
        max-width: 1000px;
    }
    .price-overview {
        background: #18191d;
        border-radius: 1.2em;
        box-shadow: 0 2px 12px #0007;
        margin-bottom: 1.1em;
        padding: 1.1em 1.5em 1.2em 1.5em;
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 2.7em;
    }
    .price-kpi {
        font-size: 2.7em;
        font-weight: 700;
        letter-spacing: 0.01em;
        color: #fff;
        margin-bottom: 0.15em;
    }
    .price-chg {
        font-size: 1.23em;
        font-weight: 600;
        margin-bottom: 0.16em;
        margin-left: 0.18em;
    }
    .kpi-block {
        background: #18191d;
        border-radius: 1.1em;
        box-shadow: 0 2px 12px #0007;
        margin-bottom: 1.1em;
        padding: 1.5em 1em 1.1em 1em;
        text-align: center;
        font-size: 2.2em;
        font-weight: 700;
        color: #fff;
        letter-spacing: 0.02em;
    }
    .metrics-panel {
        margin-top: 1em;
        margin-bottom: 1.7em;
        display: flex;
        flex-direction: row;
        gap: 2.5em;
        justify-content: center;
        align-items: flex-start;
    }
    .metrics-col {
        flex: 1;
        min-width: 250px;
        max-width: 420px;
    }
    .mainchart-container {
        background: #18191d;
        border-radius: 1.2em;
        box-shadow: 0 4px 18px #0007;
        margin-bottom: 1.4em;
        padding: 1.2em 1.4em 1.2em 1.4em;
        text-align: center;
    }
    .mainchart-title {
        font-size: 1.37em;
        font-weight: 600;
        margin-bottom: 0.6em;
        color: #fff;
        font-family: 'EB Garamond', serif !important;
    }
    .ma-table-container {
        background: #18191d;
        border-radius: 1.2em;
        box-shadow: 0 2px 12px #0007;
        margin-top: 1.7em;
        margin-bottom: 1.8em;
        padding: 1.2em 1.4em;
    }
    .ma-table-title {
        font-size: 1.18em;
        font-weight: 600;
        margin-bottom: 0.5em;
        color: #fff;
        font-family: 'EB Garamond', serif !important;
    }
    .ma-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 1.13em;
        color: #fff;
    }
    .ma-table th, .ma-table td {
        padding: 0.41em 1.2em 0.41em 0.7em;
        text-align: left;
        color: #fff;
        border: none;
    }
    .ma-table th {
        font-weight: 700;
        background: #162033;
    }
    .ma-table tr:nth-child(even) td {
        background: #12243a;
    }
    .ma-table tr:nth-child(odd) td {
        background: #18191d;
    }
    .footer-row {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        margin-bottom: 0.7em;
    }
    .copyright-text {
        text-align:center;
        color:#888;
        font-size:1.12em;
        margin-top:1.7em;
        margin-bottom:0.7em;
        font-family:'EB Garamond',serif !important;
    }
    /* Responsive */
    @media (max-width: 1100px) {
        .dashboard-container {padding-left: 2vw !important; padding-right: 2vw !important;}
        .mainchart-container, .ma-table-container, .price-overview {padding-left: 0.8em !important; padding-right: 0.8em !important;}
        .metrics-panel {flex-direction: column;gap:0.7em;}
    }
    </style>
""", unsafe_allow_html=True)

# --- Data Download/Processing ---
def fetch_data(ticker, start, end, interval):
    return yf.download(ticker, start=start, end=end, interval=interval, auto_adjust=True)

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

# --- DASHBOARD ---
with st.container():
    st.markdown("<div class='dashboard-container'>", unsafe_allow_html=True)

    # --- [1] Price Overview (top-left) ---
    ticker = "AAPL"
    start = "2023-01-01"
    end = pd.to_datetime("today").strftime("%Y-%m-%d")
    interval = "1d"
    df = fetch_data(ticker, start, end, interval)
    if df.empty:
        st.error("No data found for AAPL.")
        st.stop()

    # Calculate metrics
    cur_price = df["Close"].dropna().iloc[-1]
    prev_price = df["Close"].dropna().iloc[-2] if len(df["Close"].dropna()) > 1 else cur_price
    pct_chg = ((cur_price - prev_price) / prev_price) * 100 if prev_price != 0 else 0
    pct_color = "#fff"
    spark_df = df["Close"].dropna().tail(30)
    spark_fig = go.Figure(go.Scatter(
        y=spark_df, mode="lines", line=dict(color="#fff", width=2), hoverinfo="skip"
    ))
    spark_fig.update_layout(height=54, width=160, margin=dict(l=0, r=0, t=0, b=0), showlegend=False, xaxis=dict(visible=False), yaxis=dict(visible=False), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

    st.markdown("<div class='price-overview'>", unsafe_allow_html=True)
    left_col, right_col = st.columns([3,2])
    with left_col:
        st.markdown(f"<div class='price-kpi'>${cur_price:,.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='price-chg'>{pct_chg:+.2f}% today</div>", unsafe_allow_html=True)
    with right_col:
        st.plotly_chart(spark_fig, use_container_width=False)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- [2] Main Chart (center, wide) ---
    st.markdown("<div class='mainchart-container'>", unsafe_allow_html=True)
    st.markdown("<div class='mainchart-title'>AAPL Candlestick Chart • Last 1Y</div>", unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"],
        name='Candlestick', increasing_line_color="#00c805", decreasing_line_color="#ff4c4c"
    ))
    # Overlaid MAs
    for ma, col in [("MA20", "#fff"), ("MA50", "#bbb"), ("MA100", "#00c805"), ("MA200", "#888")]:
        df[ma] = df["Close"].rolling(int(ma[2:])).mean()
        fig.add_trace(go.Scatter(
            x=df.index, y=df[ma], mode="lines", name=ma, line=dict(width=2, color=col, dash="dot")
        ))
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, t=18, b=2),
        height=440,
        showlegend=True,
        plot_bgcolor="#18191d",
        paper_bgcolor="#18191d",
        yaxis=dict(title="Price", color="#fff"),
        xaxis=dict(title="", color="#fff"),
        legend=dict(font=dict(size=13, color="#fff"), orientation="h", yanchor="bottom", y=1.03, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Volume bar (below main chart)
    vol_fig = go.Figure(go.Bar(
        x=df.index, y=df["Volume"],
        marker=dict(color="#00c805", opacity=0.35),
        name="Volume"
    ))
    vol_fig.update_layout(
        height=110, margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="#18191d",
        paper_bgcolor="#18191d",
        showlegend=False,
        yaxis=dict(title="Volume", color="#fff"),
        xaxis=dict(title="", color="#fff")
    )
    st.plotly_chart(vol_fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- [3] Metrics Panel (2-column grid below chart) ---
    st.markdown("<div class='metrics-panel'>", unsafe_allow_html=True)
    left_col, right_col = st.columns(2, gap="large")

    # Left: Drawdown, Volatility, Sharpe
    with left_col:
        drawdown_series = (df["Close"] - df["Close"].cummax()) / df["Close"].cummax()
        dd_fig = go.Figure(go.Scatter(
            x=df.index, y=drawdown_series, line=dict(color="#fff", width=2), fill="tozeroy", fillcolor="rgba(255,255,255,0.07)"
        ))
        dd_fig.update_layout(height=120, margin=dict(l=0, r=0, t=0, b=0),
                             plot_bgcolor="#18191d", paper_bgcolor="#18191d", showlegend=False,
                             yaxis=dict(title="Drawdown", color="#fff"), xaxis=dict(visible=False))
        st.markdown("<div class='stat-label'>Drawdown</div>", unsafe_allow_html=True)
        st.plotly_chart(dd_fig, use_container_width=True)
        # Volatility
        vol20 = df["Close"].rolling(20).std()
        vol_fig2 = go.Figure(go.Scatter(
            x=df.index, y=vol20, line=dict(color="#fff", width=2)
        ))
        vol_fig2.update_layout(height=120, margin=dict(l=0, r=0, t=0, b=0),
                              plot_bgcolor="#18191d", paper_bgcolor="#18191d", showlegend=False,
                              yaxis=dict(title="Volatility (20d)", color="#fff"), xaxis=dict(visible=False))
        st.markdown("<div class='stat-label'>Volatility (20d)</div>", unsafe_allow_html=True)
        st.plotly_chart(vol_fig2, use_container_width=True)
        # Sharpe
        returns = df["Close"].pct_change().dropna()
        sharpe = sharpe_ratio(returns)
        st.markdown(f"<div class='kpi-block'>Sharpe Ratio<br><span style='font-size:1.7em;'>{sharpe if sharpe != '-' else '—'}</span></div>", unsafe_allow_html=True)

    # Right: RSI, MACD, OBV
    with right_col:
        st.markdown("<div class='stat-label'>RSI (14d)</div>", unsafe_allow_html=True)
        df["RSI"] = rsi(df["Close"])
        rsi_fig = go.Figure(go.Scatter(
            x=df.index, y=df["RSI"], line=dict(color="#fff", width=2)
        ))
        rsi_fig.update_layout(height=120, margin=dict(l=0, r=0, t=0, b=0),
                              plot_bgcolor="#18191d", paper_bgcolor="#18191d", showlegend=False,
                              yaxis=dict(title="RSI", color="#fff", range=[0,100]), xaxis=dict(visible=False))
        st.plotly_chart(rsi_fig, use_container_width=True)

        st.markdown("<div class='stat-label'>MACD</div>", unsafe_allow_html=True)
        macd_line, signal_line, macd_hist = macd(df["Close"])
        macd_fig = go.Figure()
        macd_fig.add_trace(go.Scatter(x=df.index, y=macd_line, name="MACD", line=dict(color="#fff")))
        macd_fig.add_trace(go.Scatter(x=df.index, y=signal_line, name="Signal", line=dict(color="#bbb")))
        macd_fig.add_trace(go.Bar(x=df.index, y=macd_hist, name="Histogram", marker_color="#00c805", opacity=0.38))
        macd_fig.update_layout(height=120, margin=dict(l=0, r=0, t=0, b=0),
                              plot_bgcolor="#18191d", paper_bgcolor="#18191d", showlegend=False,
                              yaxis=dict(title="", color="#fff"), xaxis=dict(visible=False))
        st.plotly_chart(macd_fig, use_container_width=True)

        st.markdown("<div class='stat-label'>OBV</div>", unsafe_allow_html=True)
        df["OBV"] = obv(df["Close"], df["Volume"])
        obv_fig = go.Figure(go.Scatter(
            x=df.index, y=df["OBV"], line=dict(color="#fff", width=2)
        ))
        obv_fig.update_layout(height=120, margin=dict(l=0, r=0, t=0, b=0),
                              plot_bgcolor="#18191d", paper_bgcolor="#18191d", showlegend=False,
                              yaxis=dict(title="OBV", color="#fff"), xaxis=dict(visible=False))
        st.plotly_chart(obv_fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- [4] Moving Averages Table (bottom full-width) ---
    st.markdown("<div class='ma-table-container'>", unsafe_allow_html=True)
    st.markdown("<div class='ma-table-title'>Moving Averages Table</div>", unsafe_allow_html=True)
    ma_table = pd.DataFrame({
        "Date": df.index[-15:],
        "Close": df["Close"].tail(15).map(lambda x: f"${x:,.2f}"),
        "MA20": df["MA20"].tail(15).map(lambda x: f"${x:,.2f}" if pd.notnull(x) else "—"),
        "MA50": df["MA50"].tail(15).map(lambda x: f"${x:,.2f}" if pd.notnull(x) else "—"),
        "MA100": df["MA100"].tail(15).map(lambda x: f"${x:,.2f}" if pd.notnull(x) else "—"),
        "MA200": df["MA200"].tail(15).map(lambda x: f"${x:,.2f}" if pd.notnull(x) else "—"),
    }).set_index("Date")
    st.markdown('<table class="ma-table"><thead><tr><th>Date</th><th>Close</th><th>MA20</th><th>MA50</th><th>MA100</th><th>MA200</th></tr></thead><tbody>' +
        "".join([
            f"<tr><td>{idx.strftime('%Y-%m-%d')}</td>"
            + "".join([f"<td>{v}</td>" for v in row])
            + "</tr>"
            for idx, row in ma_table.iterrows()
        ]) +
        '</tbody></table>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- [5] Footer: Download CSV, copyright (right aligned) ---
    st.markdown("<div class='footer-row'>", unsafe_allow_html=True)
    st.download_button(
        label="Download CSV",
        data=df.to_csv().encode(),
        file_name=f"AAPL_{start}_{end}.csv",
        mime="text/csv",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""<div class="copyright-text">
    &copy; 2025 QuantPilot. All rights reserved.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)