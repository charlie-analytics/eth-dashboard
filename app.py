import streamlit as st
import yfinance as yf

st.title("Ethereum Dashboard")

# Fetch ETH data
eth = yf.download("ETH-USD", period="30d", interval="1h")

st.subheader("ETH Price Chart")
st.line_chart(eth["Close"])

# Simple RSI
delta = eth["Close"].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))

st.subheader("RSI")
st.line_chart(rsi)
