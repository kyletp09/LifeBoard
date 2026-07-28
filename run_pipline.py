from aiNewsScraper import fetch_ai_news
from codingNewsScraper import fetch_coding_news 
from summarize import summarize
import db
import itertools
import json

# Deal with the case where there are no articles to be summarized

def ingest_all():
    all_news = itertools.chain(fetch_ai_news(), fetch_coding_news())
    conn = db.get_connection()
    db.insert_articles(conn, all_news)
    unsummarized = db.get_unsummarized(conn)
    print(json.dumps(unsummarized, indent=4, default=str))
    print(f'There are {len(unsummarized)} unsummarized articles.')

    print("Now Summarizing")
    for article in unsummarized:
        db.insert_summary(conn, summarize(article['Text']), article['Link'])
    print("Done!")
    print(db.current_articles(conn))

if __name__ == "__main__":
    ingest_all()
