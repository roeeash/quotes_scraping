from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By

from internal_types.Quote import Quote
from utils import parse_quote_items


def extract_quote_data_from_page(page:int) -> List[Quote]:
    driver = webdriver.Chrome()
    driver.get(f"https://quotes.toscrape.com/page/{page}")
    quotes_data = driver.find_elements(By.XPATH, "(//div[@class='quote'])")
    quotes = []

    for quote_data in quotes_data:
        quote_data_text = quote_data.text
        quote_data_parts = quote_data_text.split("\n")
        quote = parse_quote_items(quote_data_parts=quote_data_parts)
        quotes.append(quote)

    return quotes


def extract_quote_data_from_page_range(first_page: int, last_page: int) -> List[Quote]:
    all_quotes = []

    for page in range(first_page, last_page + 1):
        quotes_from_page = extract_quote_data_from_page(page=page)
        for quotes in quotes_from_page:
            all_quotes.append(quotes)

    return all_quotes


