import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timezone, timedelta
import html

def _clean_html(raw_html: str):
    soup = BeautifulSoup(raw_html, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    text = html.unescape(text)
    return text

def fetch_coding_news():
    response = requests.get('https://news.mit.edu/topic/mitmachine-learning-rss.xml')
    soup = BeautifulSoup(response.text, 'xml')
    item_list = soup.find_all('item')

    data_entries = [
        {
            'Title': item.title.text,
            'Pub_date': parse(item.pubDate.text).isoformat(),
            'Link': item.link.text,
            'Text': _clean_html(item.find('content:encoded').text)
        }
        for item in item_list[:10]
    ]

    return data_entries

if __name__ == "__main__":
    import json
    print(json.dumps(fetch_coding_news(), indent=4, default=str))
