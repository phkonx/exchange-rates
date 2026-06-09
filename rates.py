import requests
import json

response = requests.get("https://api.frankfurter.app/latest?from=USD&to=THB")
data = json.loads(response.text)
rate = data["rates"]["THB"]
print("statuscode is: ", response.status_code)
print("1 USD buys THB ", rate)