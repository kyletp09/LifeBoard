import sqlite3

def get_connection():
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row
    conn.execute("""
                    CREATE TABLE IF NOT EXISTS articles(
                    Title TEXT NOT NULL,
                    Pub_date TIMESTAMP NOT NULL,
                    Link TEXT UNIQUE NOT NULL,
                    Text TEXT NOT NULL,
                    Summary Text
                    )
                 """
                 )  

    return conn

def insert_articles(conn, articles):
    conn.executemany("""
                    INSERT INTO articles values(
                    :Title,
                    :Pub_date,
                    :Link,
                    :Text,
                    Null
                    ) 
                    ON CONFLICT (Link) DO NOTHING
                    """, articles)
    conn.commit()

def get_unsummarized(conn):
    unsummarized_articles = conn.execute("""SELECT Link, Text, Pub_Date
                                           FROM articles
                                           WHERE Pub_Date >= DATE('now', '-7 days')
                                                 AND Summary is NULL""").fetchall()
    return [dict(i) for i in unsummarized_articles]

def insert_summary(conn, summary, link):
    conn.execute("""
                    UPDATE articles
                    SET Summary = (?)
                    WHERE Link = (?)
                 """, (summary, link))
    conn.commit()

def current_articles(conn):
    articles = conn.execute("""SELECT Summary, Link 
                               FROM articles
                               WHERE Pub_Date >= DATE('now', '-7 days')
                                     AND Summary is NOT NULL""").fetchall()
    return [dict(i) for i in articles]

if __name__ == "__main__":
    from datetime import datetime

    test_data = {
        'Title': "Kyle's Test Data",
        'Pub_date': datetime(2026, 7, 27).isoformat(),
        'Link': 'https://www.google.com',
        'Text': 'Kyle is the best programmer ever'
    }

    conn = get_connection()

    print(get_unsummarized(conn))
