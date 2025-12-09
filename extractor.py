from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By

from internal_types.Quote import Quote
from utils import parse_quote_items


def extract_quote_data_from_page_range(first_page: int, last_page: int, driver: webdriver.Chrome = None) -> List[Quote]:
    """

    :param first_page:
    :param last_page:
    :return:
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




