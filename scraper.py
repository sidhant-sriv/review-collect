# import module
import requests
from bs4 import BeautifulSoup

url = input()
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.content, 'lxml')
# print(soup.prettify())

#First get the link that takes you to all the reviews
def read_more():

    cname = "a-link-emphasis a-text-bold"
    t = soup.find("a", class_=cname)
    return "https://www.amazon.in"+t["href"]
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def replace_sortby(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Replace the 'sortby' parameter with 'sortBy' and set its value to 'recent'
    query_params['sortBy'] = ['recent']
    query_params.pop('sortby', None)

    # Construct the modified URL
    modified_query = urlencode(query_params, doseq=True)
    modified_url = urlunparse(parsed_url._replace(query=modified_query))
    return modified_url

def get_rev_top():
    newlink = read_more()
    response = requests.get(newlink, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')
    cname = "a-size-base review-text review-text-content"
    res = []
    for i in soup.find_all("span", class_=cname):
        res.append(i.get_text())
    return res
def get_rev_recent():
    newlink = read_more()
    newlink = replace_sortby(newlink)
    response = requests.get(newlink, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')
    cname = "a-size-base review-text review-text-content"
    res = []
    for i in soup.find_all("span", class_=cname):
        res.append(i.get_text())
    return res
def get_rev():
    return get_rev_recent() + get_rev_top()
print(len(get_rev()))


