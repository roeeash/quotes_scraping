from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, BackgroundTasks

from extractor import extract_quote_data_from_page_range
from internal_types.Quote import Quote
from storage import create_table, insert_into_db


@asynccontextmanager
async def lifespan(app: FastAPI):
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