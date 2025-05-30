import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="QuantPilot: All-in-One Dashboard", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');
    html, body, [class*="css"], .stApp {
        font-family: 'EB Garamond', serif !important;
        background: #f4f8fb !important;
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
    Level up your investing with <b>QuantPilot</b>: beautiful charts and easy-to-understand insights.<br>
    <span style='color:#666; font-size:1rem;'>
    Get clarity on your stocks—no matter your experience level.
    </span>
</div>
""", unsafe_allow_html=True)

# ---- User Inputs ----
with st.expander("① Select Tickers and Date Range", expanded=True):
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

st.markdown("<h2 style='margin-top:1.5em;'>② What the Chart Shows</h2>", unsafe_allow_html=True)
st.markdown("""
<ul style='font-size:1.08em;'>
<li><b>Candlestick Chart:</b> Shows price open, high, low, and close for each period.</li>
<li><b>20-day & 50-day Moving Averages:</b> Simple moving averages that help show the price trend.</li>
<li><b>Volume Bars:</b> Shows the number of shares traded in each period.</li>
</ul>
""", unsafe_allow_html=True)

st.markdown("<h2 style='margin-top:2em;'>③ Stock Data & Analysis</h2>", unsafe_allow_html=True)
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
            close_col = f"Close_{ticker}" if f"Close_{ticker}" in data.columns else f"{ticker}_Close"
            open_col = f"Open_{ticker}" if f"Open_{ticker}" in data.columns else f"{ticker}_Open"
            high_col = f"High_{ticker}" if f"High_{ticker}" in data.columns else f"{ticker}_High"
            low_col = f"Low_{ticker}" if f"Low_{ticker}" in data.columns else f"{ticker}_Low"
            vol_col = f"Volume_{ticker}" if f"Volume_{ticker}" in data.columns else f"{ticker}_Volume"

            # If ticker not present, skip
            if close_col not in data.columns:
                st.warning(f"No data for {ticker}.")
                continue

            # Compute moving averages
            df = data[[c for c in [open_col, close_col, high_col, low_col, vol_col] if c in data.columns]].copy()
            df['MA20'] = df[close_col].rolling(window=20).mean()
            df['MA50'] = df[close_col].rolling(window=50).mean()

            # --- Price Chart ---
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
            fig.update_layout(
                title=f"{ticker} Price Chart",
                yaxis_title="Price",
                xaxis_title="Date",
                xaxis_rangeslider_visible=False,
                template="plotly_white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

            # --- Volume Chart ---
            if vol_col in df.columns:
                st.bar_chart(df[vol_col], use_container_width=True)

            # --- Key Stats ---
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

            st.markdown(
                f"[View {ticker} on Yahoo Finance](https://finance.yahoo.com/quote/{ticker})",
                unsafe_allow_html=True
            )

with st.expander("About QuantPilot"):
    st.markdown("""
    <b>QuantPilot</b> empowers investors with:<br>
    - Beautiful, interactive candlestick charts<br>
    - 20-day & 50-day moving averages<br>
    - Volume data<br>
    - Downloadable CSVs<br>
    - Multi-ticker support!<br>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; font-family:'EB Garamond',serif; font-size:1.11rem; color:#888;">
        &copy; 2025 QuantPilot. All rights reserved.
    </div>
    """, unsafe_allow_html=True)