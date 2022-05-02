import http.client
import json
import report_creation
import ftplib
import smtplib
import os

# import the corresponding modules
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

port = 2525
smtp_server = "smtp.mailtrap.io"
login = "11ca66c05c39ed" # paste your login generated by Mailtrap
password = "1d5b428f74f3bb" # paste your password generated by Mailtrap

subject = "An example of boarding pass"
sender_email = "mailtrap@example.com"
receiver_email = "new@example.com"

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Add body to email
body = "Hallo Test! \n\nHiermit sende ich dir den Report zur Tesla Aktie. \n\nLG Mert"
message.attach(MIMEText(body, "plain"))

filename = "D:/TBZ/M122/Python/Projekt/report/report.pdf"
# Open PDF file in binary mode

# We assume that the file is in the directory where you run your Python script from
with open(filename, "rb") as attachment:
    # The content type "application/octet-stream" means that a MIME attachment is a binary file
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode to base64
encoders.encode_base64(part)

# Add header
part.add_header(
    "Content-Disposition",
    "attachment; filename= {report.pdf}",
)

# Add attachment to your message and convert it to string
message.attach(part)
text = message.as_string()

# send your email
with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
    server.login(login, password)
    server.sendmail(
        sender_email, receiver_email, text
    )
print('E-Mail Sent')
os.remove('D:/TBZ/M122/Python/Projekt/report/report.pdf')