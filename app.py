import streamlit as st
import yfinance as yf
import numpy as np

st.title("Ethereum Market Dashboard")

# Fetch ETH data
eth = yf.download("ETH-USD", period="30d", interval="1h")

price = eth["Close"]

# RSI Calculation
delta = price.diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))

# Charts
st.subheader("ETH Price")
st.line_chart(price)

st.subheader("RSI")
st.line_chart(rsi)

# SAFE SIGNAL LOGIC
st.subheader("Signal")

valid_rsi = rsi.dropna()

if len(valid_rsi) > 0:
    latest_rsi = float(valid_rsi.iloc[-1])

    if np.isnan(latest_rsi):
        st.warning("RSI not ready yet.")
    else:
        if latest_rsi > 70:
            st.error("Overbought → Pullback Risk")
        elif latest_rsi < 30:
            st.success("Oversold → Bounce Zone")
        else:
            st.info("Neutral → Trend Continuation Possible")

        st.write(f"Current RSI: {round(latest_rsi, 2)}")

else:
    st.warning("Not enough data yet.")
