import streamlit as st
import yfinance as yf
import ta

st.set_page_config(page_title="Market Analyzer", page_icon="📈")

st.title("📈 রিয়েল-টাইম মার্কেট এনালাইসিস বট")

symbol = st.text_input("যেকোনো কয়েন বা স্টকের নাম লিখুন (যেমন: BTC-USD, AAPL, ETH-USD):", "BTC-USD")

if st.button("অ্যানালাইসিস করুন"):
    with st.spinner('লাইভ ডেটা লোড হচ্ছে...'):
        df = yf.download(symbol, period="1d", interval="1m", progress=False)
        
        if not df.empty:
            close_prices = df['Close'].squeeze()
            rsi = ta.momentum.rsi(close_prices, window=14).iloc[-1]
            sma20 = ta.trend.sma_indicator(close_prices, window=20).iloc[-1]
            price = close_prices.iloc[-1]

            st.metric(label="বর্তমান মূল্য", value=f"${price:.2f}")
            st.metric(label="RSI (14)", value=f"{rsi:.2f}")

            if rsi < 30 and price > sma20:
                st.success("🎯 সিগন্যাল: STRONG BUY (কেনার সুযোগ)")
            elif rsi > 70 and price < sma20:
                st.error("🚨 সিগন্যাল: STRONG SELL (বিক্রি করার সুযোগ)")
            else:
                st.info("⚖️️ সিগন্যাল: NEUTRAL (অপেক্ষা করুন)")
        else:
            st.warning("ডেটা পাওয়া যায়নি! নাম বা সিম্বল ঠিক আছে কিনা দেখুন।")
