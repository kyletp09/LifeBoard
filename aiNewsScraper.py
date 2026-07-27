import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from dateutil.parser import parse
import re

def recently_posted(tag, type):
    url = tag.find('loc').text
    lastmod = parse(tag.find('lastmod').text)
    today = datetime.now(timezone.utc) 
    
    match type:
        case 'sitemap':
            is_post = bool(re.search(r'post-sitemap\d*\.xml', url)) 
            return is_post and (today - lastmod).days < 7
        case 'article':
            is_article = bool(re.search(r'^https://www\.artificialintelligence-news\.com/news/.+', url))
            return (today - lastmod).days < 7 and is_article
        case _:
            raise ValueError("recently_posted only take two types, sitemap and article")
    

response = requests.get('https://www.artificialintelligence-news.com/sitemap_index.xml')
soup = BeautifulSoup(response.text, 'xml')

sitemaplist = [
    i.find('loc').text for i in soup.find_all('sitemap')
    if recently_posted(i, 'sitemap') 
] 

total_article_list = []
for sitemap in sitemaplist:
    response = requests.get(sitemap)
    soup = BeautifulSoup(response.text, 'xml')
    sitemap_article_list = [
        i.find('loc').text for i in soup.find_all('url')
        if recently_posted(i, 'article') 
    ]
    total_article_list.extend(sitemap_article_list)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

response = requests.get('https://www.artificialintelligence-news.com/news/openai-pushes-chatgpt-into-patient-health-records/', headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

parts = []
title_div = soup.find('h1', class_ = 'elementor-heading-title elementor-size-default')
content_div= soup.find('div', class_='elementor-widget-theme-post-content')
elements = content_div.find_all(['p', 'h2', 'h3', 'h4'])
for element in elements:
    text = element.get_text(strip=True)
    if not text:
        continue
    if text.startswith('See also:') or 'AI News is powered by' in text:
        break
    parts.append(text)

article_text = '\n\n'.join(parts)
print(title_div.get_text())
