import requests
import sqlite3
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timezone, timedelta
import html
from ollama import chat, ChatResponse

def summarize(article: str):
    system_prompt = "You are an article text summarizer that summarizes the latest articles in a continous paragraph of 100 words or less. Make sure add the latest innovations from the article in thes summarization"
    user_prompt =  f'Please summarize this article: {article}'

    response: ChatResponse = chat(model='granite4.1:8b', messages=[
        {
            'role': 'system',
            'content': system_prompt
        },
        {
            'role': 'user',
            'content': user_prompt,
        },
    ] )

    return response['message']['content']


def clean_html(raw_html: str):
    soup = BeautifulSoup(raw_html, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    text = html.unescape(text)
    return text

con = sqlite3.connect('articles.db')
cur = con.cursor()

response = requests.get('https://news.mit.edu/topic/mitmachine-learning-rss.xml')
soup = BeautifulSoup(response.text, 'xml')
item_list = soup.find_all('item')

data_entries = [
    (
        item.title.text,
        parse(item.pubDate.text).isoformat(),
        item.link.text,
        clean_html(item.find('content:encoded').text)
    )
    for item in item_list[:10]
]
    
cur.execute("""SELECT name 
               FROM sqlite_master
               WHERE type='table'
               AND name='articles';""")

if cur.fetchone():
    cur.executemany("""INSERT INTO articles VALUES(?, ?, ?, ?, NULL)
                       ON CONFLICT (Link) DO NOTHING""", data_entries)
    con.commit()
else:
    cur.execute("""CREATE TABLE articles(Title Text,
                                         Pub_Date TIMESTAMP,
                                         Link UNIQUE, Text Text,
                                         Summary Text)""")
    cur.executemany("""INSERT INTO articles VALUES(?, ?, ?, ?, NULL)
                       ON CONFLICT (Link) DO NOTHING""", data_entries)
    con.commit()

unsummarized_articles = cur.execute("""SELECT Link, Text, Pub_Date
                                       FROM articles
                                       WHERE Pub_Date >= DATE('now', '-7 days')
                                             AND Summary is NULL""").fetchall()

if unsummarized_articles:
    for Link, Text, Pub_Date in unsummarized_articles:
        summarized_article = summarize(Text)
        cur.execute("UPDATE articles SET Summary = (?) WHERE Link = (?)", (summarized_article, Link))
        con.commit()
    print(f"We summarized {len(unsummarized)} articles")
else:
    print("There are no articles to summarize")

"""
recent_articles = cur.execute("SELECT Summary FROM articles WHERE Pub_Date >= DATE('now', '-7 days')").fetchall()

for summary, in recent_articles:
    print(summary, '\n')
"""
    
con.close()
