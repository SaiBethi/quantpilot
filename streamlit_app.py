import streamlit as st
st.set_page_config(page_title="QuantPilot: All-in-One Dashboard", layout="wide")

# Now your other imports and Streamlit code can go below
import yfinance as yf
import pandas as pd
import plotly.express as px
import streamlit as st

try:
    import pandas_ta as ta
    TA_INSTALLED = True
except ImportError:
    TA_INSTALLED = False

st.set_page_config(page_title="QuantPilot: All-in-One Dashboard", layout="wide")

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
    Level up your investing with <b>QuantPilot</b>: advanced analytics, interactive charts, and easy-to-understand insights.<br>
    <span style='color:#666; font-size:1rem;'>
    Get clarity on your stocks—no matter your experience level.
    </span>
</div>
""", unsafe_allow_html=True)

# ---- 1. User Inputs ----
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

# ---- 2. Indicator Selection ----
with st.expander("② Customize: Technical Indicators", expanded=True):
    if TA_INSTALLED:
        indicators = st.multiselect(
            "Choose which indicators to add to your charts:",
            ["RSI", "MACD", "EMA20", "SMA50", "BB", "VWAP", "ATR", "EMA100"],
            default=["RSI", "BB", "EMA20", "SMA50"]
        )
    else:
        indicators = []
        st.info("Install `pandas_ta` for more technical indicators (pip install pandas_ta).")

st.markdown("<h2 style='margin-top:1.7em;'>③ Indicator Explanations</h2>", unsafe_allow_html=True)
st.markdown("""
<ul style='font-size:1.08em;'>
<li><b>Bollinger Bands (BB Upper/Lower):</b> Show likely overbought (upper) and oversold (lower) price levels, based on volatility.</li>
<li><b>MA20 & MA50:</b> Moving averages that smooth price. MA20 is short-term, MA50 is longer-term.</li>
<li><b>EMA20, EMA100:</b> Like moving averages but react more quickly to price changes. EMA100 is a very long-term trendline.</li>
<li><b>RSI (Relative Strength Index):</b> Measures momentum (0-100). Over 70: overbought; under 30: oversold.</li>
<li><b>MACD (Moving Average Convergence Divergence):</b> Tracks momentum and trend shifts. Crossovers are key signals.</li>
<li><b>VWAP (Volume Weighted Average Price):</b> Average price weighted by volume; shows the “fair” market price.</li>
<li><b>ATR (Average True Range):</b> Indicates volatility (how much price moves up/down).</li>
</ul>
""", unsafe_allow_html=True)

st.markdown("<h2 style='margin-top:2em;'>④ Stock Data & Analysis</h2>", unsafe_allow_html=True)
if st.button("Get Data & Analyze", key="getdata"):
    # Download all tickers as one DataFrame (MultiIndex columns)
    data = yf.download(tickers, start=start, end=end, interval=interval, group_by='ticker', auto_adjust=True)
    if data.empty:
        st.error("No data found for these tickers in the selected date range.")
    else:
        # FLATTEN MultiIndex columns if present
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = ["_".join([str(i) for i in col if i]) for col in data.columns.values]

        for ticker in tickers:
            st.markdown(f"<h3 style='margin-top:1.5em; margin-bottom:0.4em;'>{ticker}</h3>", unsafe_allow_html=True)
            # Find columns for this ticker (e.g. Close_AAPL)
            close_col = f"Close_{ticker}" if f"Close_{ticker}" in data.columns else f"{ticker}_Close"
            high_col = f"High_{ticker}" if f"High_{ticker}" in data.columns else f"{ticker}_High"
            low_col = f"Low_{ticker}" if f"Low_{ticker}" in data.columns else f"{ticker}_Low"
            vol_col = f"Volume_{ticker}" if f"Volume_{ticker}" in data.columns else f"{ticker}_Volume"

            # If ticker not present, skip
            if close_col not in data.columns:
                st.warning(f"No data for {ticker}.")
                continue

            # Calculate indicators
            df = data[[c for c in [close_col, high_col, low_col, vol_col] if c in data.columns]].copy()
            if TA_INSTALLED:
                if "RSI" in indicators:
                    df['RSI'] = ta.rsi(df[close_col], length=14)
                if "EMA20" in indicators:
                    df['EMA20'] = ta.ema(df[close_col], length=20)
                if "SMA50" in indicators:
                    df['SMA50'] = ta.sma(df[close_col], length=50)
                if "MACD" in indicators:
                    macd = ta.macd(df[close_col])
                    for c in macd.columns:
                        df[c] = macd[c]
                if "BB" in indicators:
                    bb = ta.bbands(df[close_col])
                    for c in bb.columns:
                        df[c] = bb[c]
                if "VWAP" in indicators and all(x in df.columns for x in [high_col, low_col, close_col, vol_col]):
                    df['VWAP'] = ta.vwap(df[high_col], df[low_col], df[close_col], df[vol_col])
                if "ATR" in indicators and all(x in df.columns for x in [high_col, low_col, close_col]):
                    df['ATR'] = ta.atr(df[high_col], df[low_col], df[close_col])
                if "EMA100" in indicators:
                    df['EMA100'] = ta.ema(df[close_col], length=100)
            else:
                df['MA20'] = df[close_col].rolling(window=20).mean()
                df['MA50'] = df[close_col].rolling(window=50).mean()

            st.markdown("<h4>📊 Price Chart & Indicators</h4>", unsafe_allow_html=True)
            possible_cols = [close_col, "EMA20", "SMA50", "EMA100", "VWAP", "BBL_5_2.0", "BBU_5_2.0", "MA20", "MA50"]
            chart_cols = []
            for col in possible_cols:
                if col in df.columns and isinstance(df[col], pd.Series) and df[col].notna().any():
                    chart_cols.append(col)
            if len(chart_cols) > 0:
                fig = px.line(df, x=df.index, y=chart_cols, title=f"{ticker} Closing Price & Indicators", labels={"value": "Price"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No valid data to plot for this ticker and timeframe.")

            # ---- RSI Chart ----
            if "RSI" in df.columns and df["RSI"].notna().any():
                st.markdown("<h4>📉 RSI (Momentum)</h4>", unsafe_allow_html=True)
                st.line_chart(df['RSI'])

            # ---- MACD Chart ----
            if (
                "MACD_12_26_9" in df.columns and
                "MACDs_12_26_9" in df.columns and
                df["MACD_12_26_9"].notna().any()
            ):
                st.markdown("<h4>📈 MACD</h4>", unsafe_allow_html=True)
                st.line_chart(df[["MACD_12_26_9", "MACDs_12_26_9"]])

            # ---- ATR Chart ----
            if "ATR" in df.columns and df["ATR"].notna().any():
                st.markdown("<h4>📊 ATR (Volatility)</h4>", unsafe_allow_html=True)
                st.line_chart(df['ATR'])

            # ---- Key Stats ----
            st.markdown("<h4>📋 Key Stats for this Period</h4>", unsafe_allow_html=True)
            latest_close = df[close_col].dropna().iloc[-1] if df[close_col].notna().any() else float('nan')
            latest_vol = df[vol_col].dropna().iloc[-1] if vol_col in df.columns and df[vol_col].notna().any() else float('nan')
            st.write(f"**Latest Close:** ${latest_close:.2f}")
            st.write(f"**Volume:** {latest_vol:,.0f}")
            st.write(f"**High (period):** ${df[high_col].max():.2f}" if high_col in df.columns else "")
            st.write(f"**Low (period):** ${df[low_col].min():.2f}" if low_col in df.columns else "")
            st.write(f"**Total Trading Days:** {len(df)}")

            st.download_button(
                label="Download data as CSV",
                data=df.to_csv().encode(),
                file_name=f"{ticker}_{start}_{end}.csv",
                mime="text/csv",
            )

            # ---- AI-Powered Trading Suggestion ----
            st.markdown("<h4>🤖 AI-Powered Trading Suggestion</h4>", unsafe_allow_html=True)
            mean_close = df[close_col].mean()
            rsi_val = df['RSI'].dropna().iloc[-1] if "RSI" in df.columns and df['RSI'].notna().any() else None
            macd_val = df['MACD_12_26_9'].dropna().iloc[-1] if "MACD_12_26_9" in df.columns and df['MACD_12_26_9'].notna().any() else None
            bb_upper = df['BBU_5_2.0'].dropna().iloc[-1] if "BBU_5_2.0" in df.columns and df['BBU_5_2.0'].notna().any() else None
            bb_lower = df['BBL_5_2.0'].dropna().iloc[-1] if "BBL_5_2.0" in df.columns and df['BBL_5_2.0'].notna().any() else None

            suggestion = []
            if latest_close > mean_close:
                suggestion.append("The current price is **above** its average—bullish trend.")
            elif latest_close < mean_close:
                suggestion.append("The current price is **below** its average—watch for reversals.")

            if rsi_val is not None and not pd.isna(rsi_val):
                if rsi_val > 70:
                    suggestion.append("RSI suggests the stock is **overbought**. Caution: may pull back soon.")
                elif rsi_val < 30:
                    suggestion.append("RSI suggests the stock is **oversold**. There could be a rebound opportunity.")
                else:
                    suggestion.append("RSI is in a neutral range.")

            if macd_val is not None and not pd.isna(macd_val):
                if macd_val > 0:
                    suggestion.append("MACD is positive: momentum is to the upside.")
                else:
                    suggestion.append("MACD is negative: momentum leans bearish.")

            if bb_upper is not None and not pd.isna(bb_upper) and latest_close >= bb_upper:
                suggestion.append("Price is touching the **upper Bollinger Band** (potential overbought).")
            if bb_lower is not None and not pd.isna(bb_lower) and latest_close <= bb_lower:
                suggestion.append("Price is touching the **lower Bollinger Band** (potential oversold).")

            st.markdown(" ".join(suggestion))
            st.caption("(*These suggestions are rule-based and for educational purposes. Always research thoroughly before investing!*)")

with st.expander("About QuantPilot"):
    st.markdown("""
    <b>QuantPilot</b> empowers investors with:
    - Beautiful, interactive charts
    - Multiple technical indicators
    - Downloadable data
    - Clear, plain-English insights
    - Multi-ticker support!
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; font-family:'EB Garamond',serif; font-size:1.11rem; color:#888;">
        &copy; 2025 QuantPilot. All rights reserved.
    </div>
    """, unsafe_allow_html=True)