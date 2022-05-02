import http.client
import json
import report_creation
import ftplib

conn = http.client.HTTPSConnection("yh-finance.p.rapidapi.com")

headers = {
    'X-RapidAPI-Host': "yh-finance.p.rapidapi.com",
    'X-RapidAPI-Key': "ac50f0a264mshb4d50d8737b1a85p178f48jsne098af8d0093"
}

conn.request("GET", "/stock/v2/get-summary?symbol=TSLA&region=US", headers=headers)

res = conn.getresponse()
data = res.read()

json_data = json.loads(data)
# Put data in variables
title = json_data['price']['shortName']
price = json_data['price']['regularMarketOpen']['fmt']
one_day_change = json_data['price']['regularMarketChangePercent']['fmt']
one_year_change = json_data['defaultKeyStatistics']['52WeekChange']['fmt']
desc = json_data['summaryProfile']['longBusinessSummary']
market_price = json_data['price']['regularMarketPrice']['raw']
pre_market_price = json_data['price']['preMarketPrice']['raw']
difference_price = market_price - pre_market_price

# call PDF generate
report_creation.create_report(title, price, one_day_change, one_year_change, desc, difference_price)

# FTP upload
session = ftplib.FTP_TLS('merttakil.bplaced.net', 'merttakil', 'yUS89xr6XKxQhQF5')
# file to send
file = open('D:/TBZ/M122/Python/Projekt/report/report.pdf', 'rb')
# send the file
session.storbinary('STOR report.pdf', file)
# close file and FTP
file.close()
session.quit()
