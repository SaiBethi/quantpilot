import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="QuantPilot: Robinhood-Legend Style", layout="wide")

# --- Style for Robinhood-like UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');
    html, body, [class*="css"], .stApp { font-family: 'EB Garamond', serif !important; background: #101114 !important; color: #f9f9f9 !important;}
    .block-container { background: #101114 !important; color: #fff !important; }
    .summary-bar {
        display: flex;
        flex-wrap: wrap;
        align-items: flex-end;
        justify-content:space-between;
        background: #18191d;
        border-radius: 1.1em;
        box-shadow: 0 2px 10px #0002;
        padding: 0.7em 2em 0.5em 2em;
        margin-bottom: 1.1em;
        font-family: 'EB Garamond', serif !important;
    }
    .summary-main {
        display: flex;
        flex-direction: column;
        flex: 1 1 250px;
    }
    .summary-ticker {
        font-size: 2.0em;
        font-weight: 700;
        color: #1db954;
        letter-spacing: 0.01em;
    }
    .summary-price {
        font-size: 1.2em;
        font-weight: 600;
        margin-top: -0.3em;
        color: #eee;
    }
    .summary-change-pos { color: #1db954; font-weight:600;}
    .summary-change-neg { color: #ff4c4c; font-weight:600;}
    .summary-vol { font-size: 0.95em; color:#aaa;}
    .summary-suggestion {
        font-size:1.15em; margin-top:0.3em; font-weight:600;
        border-radius:0.7em;padding:0.2em 0.8em; background:#151917; display:inline-block;
    }
    .suggestion-buy { color:#13f87c;background:rgba(30,160,80,0.13);}
    .suggestion-sell { color:#ff4c4c;background:rgba(180,40,40,0.09);}
    .suggestion-hold { color:#ffe48a;background:rgba(150,130,30,0.11);}
    .factor-row {display:flex;flex-wrap:wrap;gap:1.1em;margin-bottom:1.1em;}
    .factor-card {
        flex:1 1 170px; background:#171821; border-radius:0.9em; padding:0.75em 1.1em; 
        box-shadow:0 2px 8px #0002; border-left:5px solid #222; font-size:1.09em; 
        min-width:145px; max-width:260px;
    }
    .factor-title { font-size:0.95em; font-weight:600; color:#1db954;}
    .factor-value { font-size:1.3em; font-weight:700; margin-top:0.07em;}
    .factor-desc { font-size:0.95em; color:#aaa; margin-top:0.13em;}
    .legend-list {font-size:1.07em;}
    </style>
""", unsafe_allow_html=True)

# --- HEADER summary bar ---
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
st.title("") # For spacing

# --- Inputs ---
col0, col1, col2, col3 = st.columns([1.7,1.2,1.2,1.2])
with col0:
    ticker = st.text_input("Stock Ticker", value="AAPL", max_chars=8)
with col1:
    capital = st.number_input("Your Investment ($)", min_value=0.0, value=1000.0, step=100.0)
with col2:
    interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)
with col3:
    simulate = st.checkbox("Simulate future growth?", value=False)
    years = 5
    if simulate:
        years = st.slider("Years", 1, 30, 5, 1)

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

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

def pct_fmt(val):
    v = safe_number(val)
    if v == "-":
        return "-"
    return f"{v:+.2f}%"

if st.button("Show Analysis", type="primary"):
    period = f"{years+1}y" if simulate else "9mo"
    df = yf.download(ticker, period=period, interval=interval, auto_adjust=True)
    if df.empty or len(df) < 30:
        st.error("No data found or not enough data for analysis.")
    else:
        # ---- Compute indicators
        df["MA20"] = df["Close"].rolling(20).mean()
        df["MA50"] = df["Close"].rolling(50).mean()
        df["MA200"] = df["Close"].rolling(200).mean()
        df["%chg"] = df["Close"].pct_change()*100
        df["Volatility"] = df["Close"].rolling(20).std()
        df["Momentum"] = df["%chg"].rolling(5).mean()
        df["Volume"] = df["Volume"]

        last = df.iloc[[-1]].squeeze()
        safe_close = safe_fmt(last["Close"])
        safe_chg = safe_number(last["%chg"])
        safe_vol = safe_number(last["Volume"])
        safe_MA20 = safe_fmt(last["MA20"])
        safe_MA50 = safe_fmt(last["MA50"])
        safe_MA200 = safe_fmt(last["MA200"])

        start_price = safe_number(df["Close"].iloc[0])
        end_price = safe_number(df["Close"].iloc[-1])
        total_return = ((end_price - start_price) / start_price) if start_price not in ["-", 0] else 0
        avg_annual_return = ((end_price/start_price)**(1/years))-1 if simulate and years > 0 and start_price not in ["-", 0] else 0

        # --- AI suggestion (BUY/SELL/HOLD) ---
        suggestion = "HOLD"
        sugg_color_class = "suggestion-hold"
        if safe_number(last["Close"]) != "-" and safe_number(last["MA20"]) != "-" and safe_number(last["MA50"]) != "-":
            if safe_number(last["Close"]) > safe_number(last["MA20"]) > safe_number(last["MA50"]):
                suggestion = "BUY"
                sugg_color_class = "suggestion-buy"
            elif safe_number(last["Close"]) < safe_number(last["MA20"]) < safe_number(last["MA50"]):
                suggestion = "SELL"
                sugg_color_class = "suggestion-sell"

        # --- SUMMARY BAR (Robinhood style) ---
        chg_color_cls = "summary-change-pos" if safe_chg != "-" and safe_chg > 0 else "summary-change-neg"
        st.markdown(f"""
        <div class="summary-bar">
          <div class="summary-main">
            <span class="summary-ticker">{ticker.upper()}</span>
            <span class="summary-price">{safe_close} <span class="{chg_color_cls}">({pct_fmt(last['%chg'])})</span></span>
            <span class="summary-vol">Volume: {int(safe_vol) if safe_vol!='-' else '-'}</span>
          </div>
          <div class="summary-suggestion {sugg_color_class}"><b>{suggestion}</b> (AI Signal)</div>
        </div>
        """, unsafe_allow_html=True)

        # --- FACTOR CARDS ---
        st.markdown("""
        <div class="factor-row">
            <div class="factor-card">
                <div class="factor-title">📈 Candle</div>
                <div class="factor-value">{price}</div>
                <div class="factor-desc">Last price</div>
            </div>
            <div class="factor-card">
                <div class="factor-title">📊 20d MA</div>
                <div class="factor-value">{ma20}</div>
                <div class="factor-desc">Short trend</div>
            </div>
            <div class="factor-card">
                <div class="factor-title">📊 50d MA</div>
                <div class="factor-value">{ma50}</div>
                <div class="factor-desc">Mid trend</div>
            </div>
            <div class="factor-card">
                <div class="factor-title">📊 200d MA</div>
                <div class="factor-value">{ma200}</div>
                <div class="factor-desc">Long trend</div>
            </div>
            <div class="factor-card">
                <div class="factor-title">⚡ % Chg</div>
                <div class="factor-value">{chg}</div>
                <div class="factor-desc">Today move</div>
            </div>
            <div class="factor-card">
                <div class="factor-title">🌪 Volatility</div>
                <div class="factor-value">{vol}</div>
                <div class="factor-desc">20d stddev</div>
            </div>
            <div class="factor-card">
                <div class="factor-title">🔊 Volume</div>
                <div class="factor-value">{volume}</div>
                <div class="factor-desc">Latest</div>
            </div>
        </div>
        """.format(
            price=safe_close,
            ma20=safe_MA20,
            ma50=safe_MA50,
            ma200=safe_MA200,
            chg=pct_fmt(last["%chg"]),
            vol=f"{safe_number(last['Volatility']):.2f}" if safe_number(last['Volatility']) != "-" else "-",
            volume=f"{int(safe_vol):,}" if safe_vol != "-" else "-"
        ), unsafe_allow_html=True)

        # --- CHART ---
        chart = go.Figure()
        chart.add_trace(go.Candlestick(
            x=df.index,
            open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"],
            name="Candle",
            increasing_line_color="#1db954", decreasing_line_color="#ff4c4c"
        ))
        chart.add_trace(go.Scatter(x=df.index, y=df["MA20"], mode="lines", name="MA20", line=dict(color="#fff", dash="dot", width=1)))
        chart.add_trace(go.Scatter(x=df.index, y=df["MA50"], mode="lines", name="MA50", line=dict(color="#1db954", dash="dash", width=1)))
        chart.add_trace(go.Scatter(x=df.index, y=df["MA200"], mode="lines", name="MA200", line=dict(color="#f0b400", width=1)))
        chart.update_layout(
            template="plotly_dark",
            margin=dict(l=0,r=0,t=18,b=16),
            height=340,
            yaxis=dict(title="Price"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11)),
            font=dict(family="EB Garamond,serif"),
        )
        st.plotly_chart(chart, use_container_width=True)

        # --- AI Suggestion and projection ---
        st.markdown(f"<div class='ai-suggestion'><b>🤖 AI Suggestion</b><br>", unsafe_allow_html=True)
        st.markdown(f"<b>Signal:</b> <span style='color:#1db954;'>{suggestion}</span>", unsafe_allow_html=True)
        if simulate:
            if avg_annual_return == 0 or avg_annual_return == "-":
                st.markdown("<span style='color:#ff4c4c;'>Not enough data for projection.</span>", unsafe_allow_html=True)
            else:
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

# --- LEGEND (hidden by default) ---
with st.expander("🟢 What do the factors mean?"):
    st.markdown("""
    <ul class="legend-list">
      <li>📈 <b>Candle</b>: Day's price movement (open, high, low, close)</li>
      <li>📊 <b>MAs</b>: Moving Averages (trend: 20, 50, 200 days)</li>
      <li>⚡ <b>% Chg</b>: Momentum (today's % move)</li>
      <li>🌪 <b>Volatility</b>: How much price moves (risk, 20d standard deviation)</li>
      <li>🔊 <b>Volume</b>: Trading Activity</li>
      <li>🤖 <b>AI</b>: Smart suggestion</li>
    </ul>
    """, unsafe_allow_html=True)

# --- ABOUT ---
st.markdown("""
<div style='font-family: "EB Garamond", serif; font-size: 1.41em; color: #1db954; margin-top: 1.4em; margin-bottom: 1.1em; letter-spacing: 0.01em; text-shadow: 0 2px 12px #000;'>
    <b>About QuantPilot</b>
</div>
<div style='font-family: "EB Garamond", serif; font-size: 1.13em; color: #fff; margin-bottom: 0.9em;'>
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