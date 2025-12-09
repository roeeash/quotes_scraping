import json
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, BackgroundTasks, Query

from extractor import extract_quote_data_from_page_range
from internal_types.Quote import Quote
from storage import create_table, insert_into_db, select_all, get_filtered_items, select_quotes_per_author, \
    select_quotes_per_tag


@asynccontextmanager
async def lifespan(application: FastAPI):
    create_table()
    yield


app = FastAPI(lifespan=lifespan)

def scrape_and_store(first_page: int, last_page: int):
    try:
        quotes: List[Quote] = extract_quote_data_from_page_range(first_page, last_page)
        for quote in quotes:
            insert_into_db(quote)
        return {"status": "scraped successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/collect-data/{first_page}/{last_page}")
def collect_data(first_page: int, last_page: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(scrape_and_store, first_page, last_page)
    return {"status": "scraping started"}


@app.get("/all-quotes")
def get_all_quotes():
    try:
        quotes = select_all()
        return {"quotes": quotes}
    except Exception as e:
        return {"error": str(e)}


@app.get("/get-quotes")
def get_quotes(author: Optional[str] = None, tags: Optional[List[str]] = Query(None)):
    try:
        quotes = get_filtered_items(author=author, tags=tags)
        return {"quotes": quotes}
    except Exception as e:
        return {"error": str(e)}


@app.get("/get-quotes-per-author")
def get_quotes_per_author():
    try:
        quotes = select_quotes_per_author()
        return {"quotes": quotes}
    except Exception as e:
        return {"error": str(e)}


@app.get("/get-quotes-per-author")
def get_quotes_per_tag():
    try:
        quotes = select_quotes_per_tag()
        return {"quotes": quotes}
    except Exception as e:
        return {"error": str(e)}

