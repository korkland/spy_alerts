import yfinance as yf
import requests
import os

# These will be pulled from GitHub Secrets for security
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending message: {e}")

# Download data
data = yf.download("SPY", period="10d", interval="1d")
c = data["Close"].squeeze()

# Check for 3 red days in a row (requires 4 data points to compare)
three_red = False
if len(c) >= 4:
    three_red = (
        c.iat[-1] < c.iat[-2] and
        c.iat[-2] < c.iat[-3] and
        c.iat[-3] < c.iat[-4]
    )

if three_red:
    send("🚨 SPY: 3 red days in a row (Market Close)")
else:
    print("Conditions not met. No alert sent.")
