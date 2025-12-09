from extractor import extract_quote_data_from_page_range


def test_extract_quote_data_from_page(driver):
    quotes = extract_quote_data_from_page_range(1,3, driver=driver)
    assert isinstance(quotes, list)
    assert len(quotes) > 0
    assert all(hasattr(q, "text") and hasattr(q, "author") and hasattr(q, "tags") for q in quotes)
