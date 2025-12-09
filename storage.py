import json
import sqlite3
from typing import List

from internal_types.Quote import Quote

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            author TEXT NOT NULL,
            tags JSON,
            UNIQUE (text, author)
        )
    """)
    conn.commit()

def insert_into_db(quote: Quote) -> None:
    text = quote.text
    author = quote.author
    tags = quote.tags
    cursor.execute("INSERT OR IGNORE INTO QUOTES (text, author,tags) VALUES (?, ?, ?)",
                   (text, author, json.dumps(tags)))
    conn.commit()


def select_all():
    cursor.execute("SELECT * FROM QUOTES")
    return cursor.fetchall()


def get_filtered_items(author: str = None, tags: List[str] = None):
    sql = "SELECT * FROM quotes"
    conditions = []
    params = []

    if author:
        conditions.append("author = ?")
        params.append(author)

    if tags:
        tag_conditions = []
        for tag in tags:
            tag_conditions.append("""
                EXISTS (
                    SELECT 1 FROM json_each(quotes.tags)
                    WHERE json_each.value = ?
                )
            """)
            params.append(tag)
        conditions.append("(" + " OR ".join(tag_conditions) + ")")

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    cursor.execute(sql, params)
    return cursor.fetchall()



def select_count_all() -> int:
    cursor.execute("SELECT COUNT(*) FROM quotes")
    total = cursor.fetchone()[0]
    return total


def select_quotes_per_author() -> List[str]:
    cursor.execute("""
        SELECT author, COUNT(*)
        FROM quotes
        GROUP BY author
        ORDER BY COUNT(*) DESC
    """)
    return cursor.fetchall()


def select_quotes_per_tag() -> List[str]:
    cursor.execute("""
        SELECT json_each.value AS tag, COUNT(*) AS count
        FROM quotes, json_each(quotes.tags)
        GROUP BY json_each.value
        ORDER BY count DESC
    """)
    rows = cursor.fetchall()
    return rows