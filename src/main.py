import http.client
import os

conn = http.client.HTTPSConnection("yh-finance.p.rapidapi.com")
# Get API Key from system variable
api_key = os.environ.get('m122_yh_finance_key')

headers = {
    'X-RapidAPI-Host': "yh-finance.p.rapidapi.com",
    'X-RapidAPI-Key': api_key
    }

conn.request("GET", "/stock/v2/get-chart?interval=5m&symbol=TSLA&range=1mo&region=US", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))