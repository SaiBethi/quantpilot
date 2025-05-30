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

# Optional: For AI chat (OpenAI)
try:
    import openai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

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

# ---- Sidebar for Navigation & AI Coach ----
with st.sidebar:
    st.markdown(
        "<h2 style='font-family: \"EB Garamond\", serif; color:#191c24;'>🧑‍💼 AI Investment Coach</h2>",
        unsafe_allow_html=True
    )
    st.caption("Ask your AI coach anything about investing, stocks, or your portfolio.")

    if AI_AVAILABLE:
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        user_input = st.text_area("Ask your coach:", key="ai_input")
        if st.button("Ask AI"):
            if user_input.strip():
                with st.spinner("AI Coach is thinking..."):
                    # You need to set your OpenAI API key for this to work.
                    # Example: openai.api_key = st.secrets["OPENAI_API_KEY"]
                    try:
                        openai.api_key = st.secrets["OPENAI_API_KEY"]
                        messages = [{"role": "system", "content": "You are a helpful investment AI coach. Give clear, concise, and actionable advice."}]
                        for msg in st.session_state.chat_history:
                            messages.append({"role": msg["role"], "content": msg["content"]})
                        messages.append({"role": "user", "content": user_input})
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=messages,
                            max_tokens=256,
                            temperature=0.1
                        )
                        ai_reply = response.choices[0].message.content
                        st.session_state.chat_history.append({"role": "user", "content": user_input})
                        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                    except Exception as ex:
                        ai_reply = f"AI error: {ex}"
                        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
            else:
                ai_reply = "Please enter your question."
                st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})

        # Display chat history
        for msg in st.session_state.chat_history[-8:]:
            if msg["role"] == "user":
                st.markdown(f"<div style='color:#1946d2; margin-bottom:0.3em; font-weight:bold;'>You:</div>"
                            f"<div style='background:#e4eafc; border-radius:8px; padding:0.7em; margin-bottom:0.8em;'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color:#191c24; margin-bottom:0.3em; font-weight:bold;'>AI:</div>"
                            f"<div style='background:#fff; border-radius:8px; padding:0.7em; margin-bottom:0.8em;'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.info("Install OpenAI (`pip install openai`) and set your API key in Streamlit secrets for AI chat.")

st.markdown(
    "<div style='font-size:1.5rem; font-family:EB Garamond,serif; margin-bottom:0.7em; text-align:center;'>"
    "Level up your investing with <b>QuantPilot</b>: AI-powered analytics, real-time visualizations, and actionable insights.<br>"
    "Transform complexity into clarity and make every decision count—no matter your experience level."
    "</div>",
    unsafe_allow_html=True
)

# --- User selects multiple tickers and date range
with st.expander("Stock Data & Analysis", expanded=True):
    tickers = st.text_input(
        "Enter one or more stock tickers (comma separated, e.g., AAPL, TSLA, MSFT):",
        value="AAPL, TSLA"
    ).upper().replace(" ", "").split(",")

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
                st.write(f"**Latest Close:** ${data['Close'][-1]:.2f}")
                st.write(f"**Volume:** {data['Volume'][-1]:,.0f}")
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

                # --- AI Advice Section (dummy logic, replace with your AI)
                st.subheader("🤖 AI Advice")
                mean_close = data['Close'].mean()
                latest_close = data['Close'][-1]
                rsi_val = data['RSI'][-1] if TA_INSTALLED and "RSI" in data.columns else None

                advice = []
                if latest_close > mean_close:
                    advice.append("The stock is trading **above** its average for this period.")
                else:
                    advice.append("The stock is trading **below** its average for this period.")
                if rsi_val:
                    if rsi_val > 70:
                        advice.append("RSI suggests the stock is **overbought**. Be cautious.")
                    elif rsi_val < 30:
                        advice.append("RSI suggests the stock is **oversold**. Could be an opportunity.")
                    else:
                        advice.append("RSI is in a neutral range.")

                st.markdown(" ".join(advice))
                st.caption("(*AI advice is a simple demo. Integrate OpenAI for enhanced insights!*)")

                # Placeholder for OpenAI integration:
                if AI_AVAILABLE and st.checkbox("Get AI-powered summary", key=f"ai_summary_{ticker}"):
                    prompt = (f"Give me a concise, data-driven investment summary for stock {ticker} "
                              f"with recent data: {data.tail(30).to_string()}")
                    try:
                        openai.api_key = st.secrets["OPENAI_API_KEY"]
                        messages = [
                            {"role": "system", "content": "You are a professional investment assistant. Summarize the investment outlook."},
                            {"role": "user", "content": prompt}
                        ]
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=messages,
                            max_tokens=256,
                            temperature=0.1
                        )
                        st.success("AI Coach says:\n\n" + response.choices[0].message.content)
                    except Exception as ex:
                        st.error(f"AI error: {ex}")

            else:
                st.error("No data found. Please check the ticker or date range.")

with st.expander("About QuantPilot"):
    st.markdown("""
    **QuantPilot** empowers investors with:
    - Advanced analytics and interactive, real-time charts.
    - AI-powered advice and technical indicators.
    - Clean, readable, and beautiful design.
    - Downloadable data for your own research.
    - Multi-ticker support and the ability to chat with an AI investment coach!
    """)
    st.markdown("""
    <div style="text-align:center; font-family:'EB Garamond',serif; font-size:1.11rem; color:#888;">
        &copy; 2025 QuantPilot. All rights reserved.
    </div>
    """, unsafe_allow_html=True)