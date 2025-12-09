from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By

from internal_types.Quote import Quote
from utils import parse_quote_items


def extract_quote_data_from_page_range(first_page: int, last_page: int, driver: webdriver.Chrome = None) -> List[Quote]:
    """
    Extracts quotes from a range of pages on https://quotes.toscrape.com.

    This function iterates through the pages from `first_page` to `last_page` (inclusive),
    scraping all quotes on each page. Each quote is returned as a `Quote` object.

    If a `webdriver.Chrome` instance is provided via the `driver` parameter, it will be
    reused for scraping. Otherwise, a new headless Chrome instance will be created and closed
    after scraping.

    Args:
        first_page (int): The first page number to start scraping from (1-based).
        last_page (int): The last page number to scrape (inclusive).
        driver (webdriver.Chrome, optional): An optional Selenium Chrome driver to use for scraping.
            If None, a new headless driver is created.

    Returns:
        List[Quote]: A list of `Quote` objects containing the scraped quotes.
    """
    close_driver = False
    if driver is None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        close_driver = True

    all_quotes = []
    for page in range(first_page, last_page + 1):
        driver.get(f"https://quotes.toscrape.com/page/{page}")
        quotes_data = driver.find_elements(By.XPATH, "(//div[@class='quote'])")
        for quote_data in quotes_data:
            quote_data_parts = quote_data.text.split("\n")
            quote = parse_quote_items(quote_data_parts=quote_data_parts)
            all_quotes.append(quote)
    if close_driver:
        driver.quit()
    return all_quotes




