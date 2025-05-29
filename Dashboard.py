if page == "Dashboard":
    ticker = st.text_input("Enter stock ticker (e.g., AAPL)", value="SMCI").upper().strip()
    start_date = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2025-06-19"))

    if start_date > end_date:
        st.error("Error: Start Date must be before End Date.")
    elif ticker == "":
        st.warning("Please enter a stock ticker symbol.")
    else:
        try:
            data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)

            if data.empty:
                st.warning(f"No data found for ticker '{ticker}'. Try another.")
            else:
                # Calculate Moving Averages
                data["MA20"] = data["Close"].rolling(window=20).mean()
                data["MA50"] = data["Close"].rolling(window=50).mean()

                # Calculate RSI (14)
                delta = data["Close"].diff()
                gain = delta.where(delta > 0, 0)
                loss = -delta.where(delta < 0, 0)
                avg_gain = gain.rolling(14).mean()
                avg_loss = loss.rolling(14).mean()
                rs = avg_gain / avg_loss
                data["RSI"] = 100 - (100 / (1 + rs))

                st.subheader(f"📊 Price Chart for {ticker}")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode='lines', name="Close"))
                fig.add_trace(go.Scatter(x=data.index, y=data["MA20"], mode='lines', name="MA 20"))
                fig.add_trace(go.Scatter(x=data.index, y=data["MA50"], mode='lines', name="MA 50"))
                fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("📉 RSI Indicator")
                rsi_fig = go.Figure()
                rsi_fig.add_trace(go.Scatter(x=data.index, y=data["RSI"], mode='lines', name="RSI"))
                rsi_fig.update_layout(yaxis=dict(range=[0, 100]), margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(rsi_fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error fetching data: {e}")