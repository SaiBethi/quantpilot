if ticker:
    data = yf.download(ticker, start=start_date, end=end_date)

    if data.empty:
        st.error("No data found. Please check the ticker symbol or date range.")
    else:
        # Add moving averages only if 'Close' exists
        if 'Close' in data.columns:
            data['MA20'] = data['Close'].rolling(window=20).mean()
            data['MA50'] = data['Close'].rolling(window=50).mean()

            # Only show chart if columns exist
            available_columns = [col for col in ['Close', 'MA20', 'MA50'] if col in data.columns]
            
            st.subheader(f"Price chart for {ticker}")
            if available_columns:
                st.line_chart(data[available_columns])
            else:
                st.warning("Not enough data to compute moving averages yet.")
        else:
            st.error("'Close' column missing from stock data.")