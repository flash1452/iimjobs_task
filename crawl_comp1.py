from bs4 import BeautifulSoup
from datetime import timedelta
from datetime import datetime
from urllib.error import HTTPError
from urllib.error import URLError
from requests.exceptions import ConnectionError
import urllib3
import urllib
import requests
import http
import pymysql
conn = pymysql.connect(
    db='company_info',
    user='root',
    passwd='vishal',
    host='localhost')
def comp1_crawling(company_id, url, company_posting_name, last_updated, new_posting_details):
    """Crawl from first company.

    Keyword arguments:
    company_id -- the company_id of first company
    url -- the url to scrape from
    company_posting_name -- array of posts already in db
    last_updated -- last updated time from db
    new_posting_details -- array conatining info about the new postings that are not in db
    """
    global conn
    try:
        url_to_crawl = requests.get(url, verify = False, timeout = 30)
        crawled_data = url_to_crawl.text
        spobj = BeautifulSoup(crawled_data, "lxml")
        probable_positions = spobj.find_all('div', {"class" : "heading-main-top"})
        for position in probable_positions:
            position_name = position.text
            if position_name.lower() not in company_posting_name:
                position_name = position_name.replace(u'\xa0', u' ')
                if position_name != '':
                    new_posting_details[position_name.lower()] = (datetime.now() - last_updated) / timedelta(minutes=1)
        print (new_posting_details)
    except HTTPError as e:
        logs = open('log.txt', 'a')
        logs.write('HTTP Error: ' + str(e.code))
    except URLError as e:
        logs = open('log.txt', 'a')
        logs.write('URL Error: ' + e.reason)
    except ConnectionError as e:
        logs = open('log.txt', 'a')
        logs.write('Connection Error:')
    except http.client.HTTPException as e:
        logs = open('log.txt', 'a')
        logs.write('BAD STATUS LINE:')





# cur = conn.cursor()
                    # cur.execute("""INSERT INTO posting_details(posting_name) VALUES(%s)""", (position_name.replace(u'\u2013', '-').encode('latin-1')))
                    # posting_id = conn.insert_id()
                    # print(type(posting_id))
                    # cur.execute('INSERT INTO comp_posting_relation(company_id, posting_id) VALUES(%d, %d)', (company_id, posting_id))
                    # cur.execute('UPDATE company_postings SET postings_number = postings_number + 1 WHERE id = %d' % company_id)