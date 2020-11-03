import requests
from bs4 import BeautifulSoup

URL = "http://elct.lnu.edu.ua/rozk/create_query.php"
HEADERS = {
    "user-ageng": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.310",
    "accept": "*/8"}

def get_html(url, data=None, params=None):
    if data is None:
        data = {}
    r = requests.post(url,headers=HEADERS,data=data)
    r.encoding = 'cp1251'
    return r

def get_content(html):
    soup = BeautifulSoup(html,"html.parser")
    collums_in_table = soup.find_all("table")
    # не можу зробити правильну вибірку
    print(collums_in_table)


def parse():
    data = {
        "kurs": 2,
        "stream": "П".encode("cp1251")
    }
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print("error")

parse()

