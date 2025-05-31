import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="QuantPilot: Robinhood-Legend Style", layout="wide")

# --- EB Garamond & Robinhood-inspired Dark UI with crisp white input labels ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');
    html, body, [class*="css"], .stApp {
        font-family: 'EB Garamond', serif !important;
        background: #101114 !important;
        color: #f9f9f9 !important;
    }
    .block-container {
        background: #101114 !important;
        padding-top: 0.2rem !important;
        padding-right: 2.5vw;
        padding-left: 2.5vw;
        color: #fff !important;
    }
    div[data-testid="stSidebar"], .stSidebar {
        background: #181818;
        font-family: 'EB Garamond', serif !important;
        color: #fff !important;
    }
    /* All input labels and text white, with modern feel */
    label, .stTextInput label, .stNumberInput label, .stDateInput label, .stSelectbox label, .st-expanderHeader {
        color: #fff !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 1.09em !important;
    }
    .stTextInput>div>input, .stNumberInput>div>input, .stDateInput>div>input {
        background: #18191d !important;
        color: #fff !important;
        border: 1.5px solid #393e46 !important;
        font-family: 'EB Garamond', serif !important;
    }
    .stSelectbox>div {
        background: #18191d !important;
        color: #fff !important;
        border: 1.5px solid #393e46 !important;
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
        font-size: 1.09rem !important;
        border-radius: 13px;
        background: #1c1d21 !important;
        color: #fff !important;
        border: 1.5px solid #393e46;
        box-shadow: 0 2px 8px rgba(0,0,0,0.18);
        transition: background 0.16s, color 0.16s, box-shadow 0.18s;
        margin-bottom: 0.5em;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background: #21242b !important;
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
        background: #18191d !important;
        border-radius: 1em;
        padding: 0.65em 1.1em;
        margin: 0.3em 0 0.7em 0;
        box-shadow: 0 2px 8px rgba(20,20,20,0.23);
        border: 1.5px solid #1db954;
        font-size: 1.09em;
        color: #fff !important;
    }
    .ai-suggestion {
        background: #131416 !important;
        border-radius: 1em;
        padding: 0.85em 1.1em;
        margin: 0.5em 0 1em 0;
        box-shadow: 0 2px 8px rgba(40,40,40,0.19);
        border: 1.5px solid #1db954;
        font-size: 1.13em;
        font-weight: 500;
        color: #fff !important;
    }
    .section-header {
        font-size: 1.35em !important;
        margin-top: 0.5em !important;
        margin-bottom: 0.3em !important;
        font-family: 'EB Garamond', serif !important;
        font-weight: 700 !important;
        color: #1db954 !important;
        letter-spacing: 0.01em;
    }
    .stat-table {
        width: 100%;
        border-collapse: collapse;
        margin: 0.2em 0 0.7em 0;
        font-size: 1em;
        color: #fff !important;
    }
    .stat-table th, .stat-table td {
        border: none;
        text-align: left;
        padding: 0.21em 0.8em 0.21em 0;
        vertical-align: middle;
        font-family: 'EB Garamond', serif !important;
        color: #fff !important;
    }
    .stat-table th {
        color: #1db954 !important;
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
    </style>
""", unsafe_allow_html=True)

# --- Modern Robinhood-Style Topbar ---
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

# --- Compact, fun indicator legend (Robinhood style) ---
st.markdown("""
<div class='indicator-card' style="margin-bottom:0.5em;">
    <div class='section-header'>Quick Legend</div>
    <div style="display:flex;flex-wrap:wrap;gap:1.0em;">
      <span>📈 <b>Candle</b> = Day's price move</span>
      <span>📊 <b>MAs</b> = Trend (20, 50, 100, 200)</span>
      <span>⚡ <b>% Chg</b> = Momentum</span>
      <span>🌪 <b>Volatility</b> = Risk</span>
      <span>🔊 <b>Volume</b> = Activity</span>
      <span>🤖 <b>AI</b> = Smart suggestion</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Input: Ticker, Capital, and Date Range, as a "dashboard" ---
dashboard_cols = st.columns([2, 2, 2, 2])
with dashboard_cols[0]:
    ticker = st.text_input("Stock Ticker", value="AAPL", max_chars=8)
with dashboard_cols[1]:
    capital = st.number_input("Your Investment ($)", min_value=0.0, value=1000.0, step=100.0)
with dashboard_cols[2]:
    interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)
with dashboard_cols[3]:
    years = st.number_input("Years to Simulate", min_value=1, max_value=30, value=5, step=1)

st.divider()

# --- Robinhood-style card: key info + chart side by side
if st.button("Go!", type="primary"):
    df = yf.download(ticker, period=f"{years+1}y", interval=interval, auto_adjust=True)
    if df.empty:
        st.error("No data found.")
    else:
        # --- Compute indicators
        df["MA20"] = df["Close"].rolling(20).mean()
        df["MA50"] = df["Close"].rolling(50).mean()
        df["MA200"] = df["Close"].rolling(200).mean()
        df["%chg"] = df["Close"].pct_change()*100
        df["Volatility"] = df["Close"].rolling(20).std()
        df["Momentum"] = df["%chg"].rolling(5).mean()
        df["Volume"] = df["Volume"]

        last = df.iloc[-1]
        start_price = df["Close"].iloc[0]
        end_price = df["Close"].iloc[-1]
        total_return = (end_price - start_price) / start_price
        avg_annual_return = ((end_price/start_price)**(1/years))-1 if years > 0 else 0

        # --- Robinhood-style summary card
        st.markdown(f"""
        <div style='display:flex;align-items:flex-end;gap:2.5em;margin-bottom:1.2em;flex-wrap:wrap;'>
          <div style='background:#18191d;border-radius:1.2em;padding:1.1em 1.5em;box-shadow:0 2px 8px #0003;border:1.5px solid #1db954;min-width:275px;'>
            <span style='font-size:2.15em;font-weight:700;color:#1db954;'>{ticker.upper()}</span><br>
            <span style='font-size:1.1em;'>${last["Close"]:.2f} <span style="color:{'#1db954' if last['%chg']>0 else '#ff4c4c'};">({last['%chg']:+.2f}%)</span></span><br>
            <span style='font-size:0.98em;color:#aaa;'>Vol: {int(last['Volume']):,}</span>
          </div>
          <div style='background:#18191d;border-radius:1.2em;padding:1.1em 1.5em;box-shadow:0 2px 8px #0003;border:1.5px solid #222;min-width:210px;'>
            <b>Total Return:</b> <span style="color:{'#1db954' if total_return>=0 else '#ff4c4c'};">{total_return*100:+.1f}%</span><br>
            <b>Avg/Year:</b> <span style="color:{'#1db954' if avg_annual_return>=0 else '#ff4c4c'};">{avg_annual_return*100:+.1f}%</span><br>
            <b>Volatility:</b> <span>{df['Volatility'].dropna().mean():.2f}</span>
          </div>
          <div style='background:#18191d;border-radius:1.2em;padding:1.1em 1.5em;box-shadow:0 2px 8px #0003;border:1.5px solid #222;min-width:210px;'>
            <b>20d MA:</b> ${last["MA20"]:.2f}<br>
            <b>50d MA:</b> ${last["MA50"]:.2f}<br>
            <b>200d MA:</b> ${last["MA200"]:.2f}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # --- Chart, minimal but interactive
        chart = go.Figure()
        chart.add_trace(go.Scattergl(x=df.index, y=df["Close"], mode="lines", name="Close", line=dict(color="#1db954", width=2.2)))
        chart.add_trace(go.Scattergl(x=df.index, y=df["MA20"], mode="lines", name="MA20", line=dict(color="#fff", dash="dot", width=1)))
        chart.add_trace(go.Bar(x=df.index, y=df["Volume"]/df["Volume"].max()*df["Close"].max()*0.15, name="Volume", marker_color="#393e46", opacity=0.4, yaxis="y2"))
        chart.update_layout(
            template="plotly_dark",
            margin=dict(l=0,r=0,t=18,b=16),
            height=320,
            yaxis=dict(title="Price"),
            yaxis2=dict(overlaying="y", side="right", showgrid=False, visible=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11)),
            font=dict(family="EB Garamond,serif"),
        )
        st.plotly_chart(chart, use_container_width=True)

        # --- AI Suggestion Card + Investment Projection ---
        st.markdown(f"<div class='ai-suggestion'><b>🤖 AI Suggestion & Projection</b><br>", unsafe_allow_html=True)
        suggestion = "HOLD"
        color = "#ffe48a"
        if last["Close"] > last["MA20"] > last["MA50"]:
            suggestion = "BUY"
            color = "#1db954"
        elif last["Close"] < last["MA20"] < last["MA50"]:
            suggestion = "SELL"
            color = "#ff4c4c"
        st.markdown(f"<b>Signal:</b> <span style='color:{color}'>{suggestion}</span>", unsafe_allow_html=True)

        # Projected future value (using geometric mean of annual returns)
        future_val = capital * ((1 + avg_annual_return) ** years)
        st.markdown(f"""
        <div style="margin-top:0.65em;font-size:1.09em;">
            <b>If you invest <span style='color:#1db954;'>${capital:,.2f}</span> now and hold for <span style='color:#1db954;'>{years} years</span> at the avg return rate:</b><br>
            <span style='font-size:1.25em;color:#ffe48a;'><b>Your money could become: ${future_val:,.2f}</b></span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div style='font-size:0.99em;color:#bbb;margin-top:0.65em;'>
                *This is a simple prediction using past average returns. Markets can change—invest thoughtfully!*
            </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style='
    font-family: "EB Garamond", serif; 
    font-size: 1.41em; 
    color: #1db954; 
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