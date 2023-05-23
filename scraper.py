from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import requests
from bs4 import BeautifulSoup


HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
# response = requests.get(url, headers=HEADERS)
# soup = BeautifulSoup(response.content, 'lxml')
# # print(soup.prettify())

# First get the link that takes you to all the reviews


def read_more(url):

    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')
    cname = "a-link-emphasis a-text-bold"
    t = soup.find("a", class_=cname)
    return "https://www.amazon.in"+t["href"]


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


def increase_page_number(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Increase the 'pageNumber' parameter by 1 if it exists
    if 'pageNumber' in query_params:
        page_number = int(query_params['pageNumber'][0])
        query_params['pageNumber'] = [str(page_number + 1)]

    # Construct the modified URL
    modified_query = urlencode(query_params, doseq=True)
    modified_url = urlunparse(parsed_url._replace(query=modified_query))
    return modified_url


def get_rev_top(url):

    newlink = read_more(url)
    response = requests.get(newlink, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')
    cname = "a-size-base review-text review-text-content"
    res = []
    for i in soup.find_all("span", class_=cname):
        res.append(i.get_text())
    return res


def get_rev_recent(url):
    newlink = read_more(url)
    newlink = replace_sortby(newlink)
    response = requests.get(newlink, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')
    cname = "a-size-base review-text review-text-content"
    res = []
    for i in soup.find_all("span", class_=cname):
        res.append(i.get_text())
    return res


def get_rev(url):
    return get_rev_recent(url) + get_rev_top(url)

# Now getting the product details


def scrape_feature_bullets(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')

    feature_bullets_div = soup.find('div', id='feature-bullets')

    if feature_bullets_div:
        span_tags = feature_bullets_div.find_all('span', class_='a-list-item')
        extracted_text = [tag.get_text(strip=True) for tag in span_tags]
        return extracted_text

    return None


# print(scrape_feature_bullets(url))
# print(get_rev(url))
