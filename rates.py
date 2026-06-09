import requests

response = requests.get("https://api.frankfurter.app/latest?from=USD&to=THB")
print("statuscode is: ", response.status_code)
print("the data is ", response.text)