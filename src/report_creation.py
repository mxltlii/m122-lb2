from mailmerge import MailMerge
from docx2pdf import convert
import os

reportTemplate_path = 'D:/TBZ/M122/Python/Projekt/reportTemplate/reportTemplate.docx'
reportTemplate = MailMerge(reportTemplate_path)
print(reportTemplate.get_merge_fields())


def create_report(title, price, one_day_change, one_year_change, desc, difference_price):
    reportTemplate.merge(
        Title=title,
        Price=price,
        oneDayChange=one_day_change,
        oneYearChange=one_year_change,
        differencePrice="{:.2f}".format(difference_price),
        Desc=desc)
    reportTemplate.write('D:/TBZ/M122/Python/Projekt/report/report.docx')
    convert('D:/TBZ/M122/Python/Projekt/report/report.docx', 'D:/TBZ/M122/Python/Projekt/report/report.pdf')
    os.remove('D:/TBZ/M122/Python/Projekt/report/report.docx')
