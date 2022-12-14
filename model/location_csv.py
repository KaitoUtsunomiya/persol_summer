import csv

def main(location_list):

    f = open('CSV_files/location.csv', 'w', encoding='utf-8')
    writer = csv.writer(f)
    writer.writerow(location_list)
    f.close()