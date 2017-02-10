from bs4 import BeautifulSoup
from datetime import timedelta
from datetime import datetime
from urllib.error import HTTPError
from urllib.error import URLError
from requests.exceptions import ConnectionError
import urllib3
import urllib
import requests
import re
import http
import pymysql
conn = pymysql.connect(
    db='company_info',
    user='root',
    passwd='vishal',
    host='localhost')
def comp2_crawling(company_id, url, company_posting_name, last_updated, new_posting_details):
    """Crawl from Second company career page.

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
        probable_positions = spobj.find_all('a', {"href" : lambda L: L and L.startswith(('hiring'))})
        for position in probable_positions:
            string_position = str(position)
            parsed_html = BeautifulSoup(string_position, 'lxml')
            position_name = parsed_html.find('h4').text
            if position_name.lower() not in company_posting_name:
                position_name = re.sub('\s+',' ',position_name)
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