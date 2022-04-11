import http.client
import json
import pandas as pd
from fpdf import FPDF

conn = http.client.HTTPSConnection("yh-finance.p.rapidapi.com")

headers = {
    'X-RapidAPI-Host': "yh-finance.p.rapidapi.com",
    'X-RapidAPI-Key': "ac50f0a264mshb4d50d8737b1a85p178f48jsne098af8d0093"
    }

conn.request("GET", "/stock/v2/get-summary?symbol=TSLA&region=US", headers=headers)

res = conn.getresponse()
data = res.read()

jsonData = json.loads(data)

#df = pd.read_json(data.decode("utf-8"))
#df.info()

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size = 20)
pdf.cell(200, 10, txt = jsonData['price']['shortName'], ln = 1, align = 'C')
pdf.set_font("Arial", size = 14)
pdf.cell(200, 10, txt = "Preis: " + jsonData['price']['regularMarketOpen']['fmt'], ln = 2, align = 'L')

pdf.output("test.pdf")
