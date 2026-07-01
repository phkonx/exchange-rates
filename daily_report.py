import json
from datetime import date, timedelta

import requests
import pandas as pd

# Fetching rates for specific dates from Frankfurter
def fetch_rates(target_date, base_ccy, target_ccy):
    target_date_str = target_date.strftime("%Y-%m-%d")
    source = f"https://api.frankfurter.app/{target_date_str}?from={base_ccy}&to={target_ccy}"
    response = requests.get(source)

    if response.status_code != 200:
        print(f"Request for {target_date_str} failed: {response.status_code}")
        raise SystemExit

    try:
        data = json.loads(response.text)
    except json.JSONDecodeError:
        print(f"Error: response for {target_date_str} was not valid JSON.")
        raise

    return data

# Pulling Data - Calling function to fetch data on various dates
TARGET_BASKET="THB,EUR,SGD,CNY,HKD,MYR"
# 1. Poll once to learn the REAL latest business date — the anchor. (not necessarily today)
latest_data = fetch_rates(date.today(), base_ccy="USD", target_ccy=TARGET_BASKET)
latest_rates = latest_data["rates"]

anchor_date = date.fromisoformat(latest_data["date"])

# 2. Work backwards from the anchor (not necessarily yesterday)
previous_data = fetch_rates(anchor_date - timedelta(days=1), base_ccy="USD", target_ccy=TARGET_BASKET)
previous_rates = previous_data["rates"]

# Cleaning Data - combining rates and dates into one table
df_latest = pd.DataFrame(latest_rates.items(), columns=["currency", "rate"])
df_previous = pd.DataFrame(previous_rates.items(), columns=["currency","prev_rate"])

df = df_latest.merge(df_previous, on="currency")

df["date"] = latest_data["date"]
df["prev_date"] = previous_data["date"]

# Calculations with data - percentage changes
df["pct_change_prev_biz_day"] = (df["rate"]-df["prev_rate"])/df["prev_rate"] * 100

print(df) # printing to terminal to test code works

# Save Data - 
df.to_csv("daily_fx_report.csv", index=False)