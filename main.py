import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Optional: For technical indicators
try:
    import pandas_ta as ta
    TA_INSTALLED = True
except ImportError:
    TA_INSTALLED = False

st.set_page_config(page_title="QuantPilot All-in-One", layout="wide")

# ---- Custom Font and Styling ----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'EB Garamond', serif !important;
        background: #f4f8fb !important;
    }
    div[data-testid="stSidebar"] {
        background: #f0f3f9;
        font-family: 'EB Garamond', serif !important;
    }
    .stButton>button, .stDownloadButton>button {
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
    .block-container {
        padding-top: 1.2rem;
        padding-right: 2rem;
        padding-left: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 QuantPilot: All-in-One Dashboard")

st.markdown(
    "<div style='font-size:1.5rem; font-family:EB Garamond,serif; margin-bottom:0.7em; text-align:center;'>"
    "Level up your investing with <b>QuantPilot</b>: advanced analytics, real-time visualizations, and actionable insights.<br>"
    "Transform complexity into clarity and make every decision count—no matter your experience level."
    "</div>",
    unsafe_allow_html=True
)

# --- User selects multiple tickers and date range
with st.expander("Stock Data & Analysis", expanded=True):
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

    indicators = []
    if TA_INSTALLED:
        indicators = st.multiselect(
            "Technical Indicators (add to chart)",
            ["RSI", "MACD", "EMA20", "SMA50"],
            default=["RSI"]
        )
    else:
        st.info("Install `pandas_ta` to unlock technical indicators (pip install pandas_ta).")

    if st.button("Get Data & Analyze", key="getdata"):
        for ticker in tickers:
            if not ticker:
                continue
            st.header(f"Stock: {ticker}")

            try:
                data = yf.download(ticker, start=start, end=end, interval=interval)
            except Exception as e:
                st.error(f"Error fetching {ticker}: {str(e)}")
                continue

            if not data.empty:
                # Calculate indicators if pandas_ta is installed
                if TA_INSTALLED:
                    if "RSI" in indicators:
                        data['RSI'] = ta.rsi(data['Close'], length=14)
                    if "EMA20" in indicators:
                        data['EMA20'] = ta.ema(data['Close'], length=20)
                    if "SMA50" in indicators:
                        data['SMA50'] = ta.sma(data['Close'], length=50)
                    if "MACD" in indicators:
                        macd = ta.macd(data['Close'])
                        data = pd.concat([data, macd], axis=1)
                # Chart
                fig = px.line(data, x=data.index, y=["Close"], title=f"{ticker} Closing Price", labels={"value": "Price"})
                # Add indicators to plotly chart if present
                if TA_INSTALLED:
                    for ind in indicators:
                        if ind in data.columns:
                            fig.add_scatter(x=data.index, y=data[ind], mode="lines", name=ind)
                        if ind == "MACD" and "MACD_12_26_9" in data.columns:
                            fig.add_scatter(x=data.index, y=data["MACD_12_26_9"], mode="lines", name="MACD")

                st.plotly_chart(fig, use_container_width=True)

                # Show metrics
                st.subheader("Key Stats")
                st.write(f"**Latest Close:** ${data['Close'].iloc[-1]:.2f}")
                st.write(f"**Volume:** {data['Volume'].iloc[-1]:,.0f}")
                st.write(f"**High (period):** ${data['High'].max():.2f}")
                st.write(f"**Low (period):** ${data['Low'].min():.2f}")
                st.write(f"**Total Trading Days:** {len(data)}")

                # Download CSV
                csv = data.to_csv().encode()
                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name=f"{ticker}_{start}_{end}.csv",
                    mime="text/csv",
                )

                # --- AI Advice Section (simple logic)
                st.subheader("🤖 AI Advice")
                mean_close = data['Close'].mean()
                latest_close = data['Close'].iloc[-1]
                rsi_val = data['RSI'].iloc[-1] if TA_INSTALLED and "RSI" in data.columns else None

                advice = []
                if latest_close > mean_close:
                    advice.append("The stock is trading **above** its average for this period.")
                else:
                    advice.append("The stock is trading **below** its average for this period.")
                if rsi_val is not None:
                    if rsi_val > 70:
                        advice.append("RSI suggests the stock is **overbought**. Be cautious.")
                    elif rsi_val < 30:
                        advice.append("RSI suggests the stock is **oversold**. Could be an opportunity.")
                    else:
                        advice.append("RSI is in a neutral range.")

                st.markdown(" ".join(advice))
                st.caption("(*AI advice is a simple rule-based demo. Install OpenAI for enhanced AI insights!*)")

            else:
                st.error("No data found. Please check the ticker or date range.")

with st.expander("About QuantPilot"):
    st.markdown("""
    **QuantPilot** empowers investors with:
    - Advanced analytics and interactive, real-time charts.
    - Technical indicators.
    - Clean, readable, and beautiful design.
    - Downloadable data for your own research.
    - Multi-ticker support!
    """)
    st.markdown("""
    <div style="text-align:center; font-family:'EB Garamond',serif; font-size:1.11rem; color:#888;">
        &copy; 2025 QuantPilot. All rights reserved.
    </div>
    """, unsafe_allow_html=True)