from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv


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
        res.append(i.get_text().strip())
    return res


def get_rev_recent(url):
    newlink = read_more(url)
    newlink = replace_sortby(newlink)
    response = requests.get(newlink, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')
    cname = "a-size-base review-text review-text-content"
    res = []
    for i in soup.find_all("span", class_=cname):
        res.append(i.get_text().strip())
    return res


def get_rev(url):
    review =  get_rev_recent(url) + get_rev_top(url)
    review = '\n'.join(review)
    return review

# Now getting the product details


def get_product_review(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')

    feature_bullets_div = soup.find('div', id='feature-bullets')

    if feature_bullets_div:
        span_tags = feature_bullets_div.find_all('span', class_='a-list-item')
        extracted_text = [tag.get_text(strip=True) for tag in span_tags]
        return extracted_text

    return None

url = 'https://www.amazon.in/ASUS-i5-10300H-Graphics-Windows-FX506LH-HN258W/dp/B09RMTMBSM/?_encoding=UTF8&pd_rd_w=0CKN2&content-id=amzn1.sym.82b4a24f-081c-4d15-959c-ef13a1d3fa4e&pf_rd_p=82b4a24f-081c-4d15-959c-ef13a1d3fa4e&pf_rd_r=JFSP5WAGMQ83F0M2SYD8&pd_rd_wg=2iEa5&pd_rd_r=6533d67c-b623-44cd-aa60-771653889630&ref_=pd_gw_ci_mcx_mr_hp_atf_m&th=1'
url = 'https://www.amazon.in/Adidas-CBLACK-FTWWHT-Running-EW2449_8/dp/B08FZTYZZJ/ref=pd_ci_mcx_mh_mcx_views_0?pd_rd_w=3CeYO&content-id=amzn1.sym.7c947cdc-0249-4ded-881f-f826efe2df4c&pf_rd_p=7c947cdc-0249-4ded-881f-f826efe2df4c&pf_rd_r=M7QXMBS60VBR7B9FBQ4C&pd_rd_wg=7TJCv&pd_rd_r=b6099f22-cc29-4ade-9f57-59fa5797644b&pd_rd_i=B08FZTYZZJ&th=1&psc=1'
url = 'https://www.amazon.in/Bendon-Publishing-Little-Pony-Magic/dp/B00A1AJX16/ref=sr_1_2?keywords=my+little+pony&qid=1684826176&sr=8-2'
print(get_rev(url))


load_dotenv()
API_KEY = os.getenv("API_TOKEN")


def summarizer(url):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

    def query(payload):
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))

    inputs = get_rev(url)

    data = query(
        {
            "inputs": inputs,
            "parameters": {"do_sample": False},
        }
    )
    
    print(data)


def question_answerer(url):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
    def query(payload):
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))
    data = query(
        {
            "inputs": {
                "question": "What's my name?",
                "context": "My name is Clara and I live in Berkeley.",
            }
        }
    )