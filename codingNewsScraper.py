import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timezone, timedelta

response = requests.get('https://news.mit.edu/topic/mitmachine-learning-rss.xml')
soup = BeautifulSoup(response.text, 'xml')

item_list = soup.find_all('item')

publication_date = [i.pubDate.text for i in item_list]
today = datetime.now(timezone.utc)

# print(publication_date[:5])

difference = today - parse(publication_date[0])

if difference < timedelta(days=7):
    print("YAY!")
