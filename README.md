Project Documentation
====================

1. Design Choices
-----------------

System Structure
----------------
- Extractor module (`extractor.py`)
  - Contains function to scrape quotes from https://quotes.toscrape.com.
  - `extract_quote_data_from_page_range(first_page, last_page, driver=None)` scrapes a range of pages, 
  and gets the following for each item:
  - Quote text 
  - Author name 
  - List of tags 
- Supports passing a `webdriver.Chrome` instance to enable headless testing.

- Storage module (`storage.py`)
  - Uses SQLite in-memory database (or optionally file-based).
  - Functions: `create_table()`, `insert_into_db()`, `select_all()`, `get_filtered_items()`, `select_count_all()`, `select_quotes_per_author()`, `select_quotes_per_tag()`.
  - Tags are stored as JSON arrays for flexible filtering.

- API module (`main.py`)
  - FastAPI application exposing endpoints:
    - `/collect-data/{first_page}/{last_page}` — triggers scraping in a background task.
    - `/all-quotes` — returns all stored quotes.
    - `/get-quotes` — filters quotes by query parameters `author` and `tags`.
  - Lifecycle (`lifespan`) ensures the database table is created when the app starts.

Design Approach
---------------
- Headless Selenium for scraping: avoids opening a browser during automated runs or tests.
- BackgroundTasks in FastAPI: scraping runs asynchronously, avoiding blocking the API.
- SQLite in-memory DB: lightweight, no external dependencies, suitable for testing and small-scale data.
- JSON for tags: allows flexible filtering on multiple tags without a separate table.

Trade-offs / Limitations
-----------------------
- SQLite in-memory DB does not persist between app restarts. For persistence, a file-based SQLite or another database would be needed.
- Scraping relies on the site structure; if it changes, the extractor will break.
- Aggregations (count per tag/author) are done in SQL using JSON functions — efficient for small datasets, but may not scale to very large datasets.
- Background scraping shares the same SQLite connection; careful threading management (`check_same_thread=False`) is necessary.

2. Running the System
--------------------

Start the API
-------------
```
uvicorn main:app --reload
```
- The app will automatically create the database table on startup.

Trigger Scraping
----------------
- Endpoint: `/collect-data/{first_page}/{last_page}`
- Example:
```
GET http://127.0.0.1:8000/collect-data/1/5
```
- This will start scraping pages 1–5 in the background. The response will immediately return:
```json
{"status": "scraping started"}
```

Retrieve Results
----------------
- All quotes: `/all-quotes`
```
GET http://127.0.0.1:8000/all-quotes
```
- Filter quotes: `/get-quotes?author=Jane Austen&tags=classic&tags=humor`
  - `author` is optional
  - `tags` is optional and can include multiple `tags=` query parameters
- Example:
```
GET http://127.0.0.1:8000/get-quotes?author=William+Shakespeare&tags=classic
```

3. Running Tests
----------------

Requirements
------------
- Install project requirements (which include `pytest`):
```
pip install -r requirements.txt
```
- `chromedriver` installed and compatible with your Chrome version.

Running Storage Tests
---------------------
```
pytest tests/test_storage.py -v -s
```
- Uses fixtures for an in-memory SQLite database.
- Tests cover insertion, filtering, counting, and aggregations.

Running Extractor Tests
-----------------------
```
pytest tests/test_extractor.py -v -s
```
- Uses headless Selenium fixture (`driver`) for scraping pages.
- Tests cover extraction of quotes, checking `Quote` objects, and basic field validation.

Notes
-----
- The tests are isolated: the database is in-memory and reset for each test session.
- The extractor tests reuse a single headless Chrome instance for efficiency using a custom
pytest fixture.

