import requests
from lxml import html
from uszipcode import SearchEngine
import sqlite3

# search = SearchEngine(simple_zipcode=True)
# zipcode = search.by_zipcode("10001")
# zipcode.to_dict()

# Company Name
# Address 
# City
# State
# Zip code
# Telephone 1
# Telephone 2
# Telephone 3
# Telephone 4
# Fax 1
# Fax 2
# Email 1
# Email 2
# Website 1
# Website 2


# Address: 3611 Valley Centre Drive, Suite 300 San Diego, 92130
# Tel: (858) 558-2871
# Fax: (303) 999-3799
# Email: info@acadia-pharm.com
# Website: www.acadia-pharm.com


url = 'https://www.pharmapproach.com/list-of-pharmaceutical-companies-in-united-states-of-america/'

db_name = 'result.db'
table_name = 'result'

def init_db():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("CREATE TABLE if not exists '{}' (company, address, city, state, zipcode, tel1, tel2, tel3, tel4, fax1, fax2, email1, email2, site1, site2)".format(table_name))

    conn.commit()
    conn.close()


def store_to_db(info):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("INSERT INTO '{}' VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)".format(table_name), (
        info.get('company') or '',
        info.get('address') or '',
        info.get('city') or '',
        info.get('state') or '',
        info.get('zipcode') or '',
        info.get('tel1') or '',
        info.get('tel2') or '',
        info.get('tel3') or '',
        info.get('tel4') or '',
        info.get('fax1') or '',
        info.get('fax2') or '',
        info.get('email1') or '',
        info.get('email2') or '',
        info.get('site1') or '',
        info.get('site1') or '',
    ))

    conn.commit()
    conn.close()


def start_scraping():
    search = SearchEngine(simple_zipcode=True)
    
    response = requests.get(url)
    page = html.fromstring(response.text)

    company_info_elements = page.xpath('//article//h3')

    for element in company_info_elements:
        name = element.xpath('./span/text()')
        info = element.xpath('./following-sibling::p[1]/text()')
        web_sites =  element.xpath('./following-sibling::p[1]//a/@href')

        info_record = {
            'company': name[0],
        }

        index = 1
        for site in web_sites:
            info_record['site' + str(index)] = site
            index += 1


        for sub_info in info:
            adjusted_info = ''.join([x for x in sub_info if not x in '\t\r\v\f\n'])

            if adjusted_info.startswith('Address'):
                address = adjusted_info

                zip_code_section = address.split(',')[-1].strip()
                zip_code = ''.join([x for x in zip_code_section if x in '1234567890'])[:5]
                
                zipcode = search.by_zipcode(zip_code)
                detailed_info = zipcode.to_dict()

                city = detailed_info.get('major_city')
                state = detailed_info.get('state')

                info_record['address'] = address
                info_record['zipcode'] = zip_code
                info_record['state'] = state
                info_record['city'] = city

            elif adjusted_info.startswith('Tel'):
                telephones = adjusted_info[4:].split(',')
                
                index = 1
                for telephone in telephones:
                    info_record['tel' + str(index)] = telephone.strip()
                    index += 1

            elif adjusted_info.startswith('Fax'):
                faxes =  adjusted_info[4:].split(',')

                index = 1
                for fax in faxes:
                    info_record['fax' + str(index)] = fax.strip()


            elif adjusted_info.startswith('Email'):
                emails =  adjusted_info[6:].split(',')

                index = 1
                for email in emails:
                    info_record['email' + str(index)] = email.strip()

        print(info_record)
        store_to_db(info_record)



if __name__ == '__main__':
    init_db()
    start_scraping()
