import csv
import sqlite3

def download_as_csv():
    db_name = 'result.db'

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    with open('company_list.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company Name', 'Address', 'City', 'State', 'Zipcode', 'Telecom 1', 'Telecom 2', 'Telecom 3', 'Telecom 4', 'Fax 1', 'Fax 2', 'Email 1', 'Email 2', 'Website 1', 'Website 2'])

    for (company, address, city, state, zipcode, tel1, tel2, tel3, tel4, fax1, fax2, email1, email2, site1, site2) in c.execute('SELECT * from result'):

        with open('company_list.csv', 'a+', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([company, address, city, state, zipcode, tel1, tel2, tel3, tel4, fax1, fax2, email1, email2, site1, site2])
    
    conn.close()

if (__name__ == '__main__'):
    download_as_csv()