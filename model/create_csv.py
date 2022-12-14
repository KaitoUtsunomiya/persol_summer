import csv
import datetime

def main(len, day):
    year,month,Day = map(int, day.split('-'))
    date = datetime.date(year, month, Day)
    date.isoweekday()
    
    if len == '1日':
        header = ['年', '月', '日', '曜日', '時間']
        body = []
        for i in range(10):
            body.append([year, month, Day, date.isoweekday(), i+11])
    
    elif len == '1週間':
        header = ['年', '月', '日', '曜日']
        body = []
        td = datetime.timedelta(days=1)
        for i in range(7):
            body.append([date.year, date.month, date.day, date.isoweekday()])
            date = date + td
    
    else:
        header = ['年', '月', '日', '曜日']
        body = []
        td = datetime.timedelta(days=1)
        for i in range(30):
            body.append([date.year, date.month, date.day, date.isoweekday()])
            date = date + td

    with open('CSV_files/sample.csv', 'w') as f:

        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(body)

        f.close()