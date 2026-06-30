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

#Calling function to fetch data on various dates
# 1. Poll once to learn the REAL latest business date — the anchor. (not necessarily today)
latest_data = fetch_rates(date.today(), base_ccy="USD", target_ccy="THB")

anchor_date = date.fromisoformat(latest_data["date"])

# 2. Work backwards from the anchor (not necessarily yesterday)
previous_data = fetch_rates(anchor_date - timedelta(days=1), base_ccy="USD", target_ccy="THB")


print(latest_data)
print(previous_data)